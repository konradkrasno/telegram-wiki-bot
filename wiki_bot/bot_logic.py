import re
import requests

import json
from django.http import JsonResponse


from wiki_bot.models import Chat, Question, Answer, AnswerFeedback, State, Greeting
from wiki_bot.bot_settings import TELEGRAM_URL, WIKI_BOT_TOKEN
from wiki_bot import custom_message, search
from wiki_bot.model_handling import choose_model


class BotInteraction:

    @staticmethod
    def check_outcome(text):
        if re.search(r'\bnie\b|\bno\b|\b[ź|z]le\b|\bz[łl]a\b', text):
            return 'negative_answer_feedback_outcome'
        if re.search(r'\btak\b|\bdobrze\b|\bdobra\b|\bgood\b', text):
            return 'positive_answer_feedback_outcome'
        if re.search(r'\bdzie[ńn] dobry\b|\bwitam\b', text):
            return 'greet_outcome'
        if re.search(r'\bwidzenia\b|\bnara\b|\bna razie\b|\b[żz]egnam\b|\bnie chce\b', text):
            return 'sign_off_outcome'
        if re.search(r'\bcze[śs][ćc]\b|\belo\b|\bsiema\b|\bhej\b', text):
            return 'greet_or_sign_off_outcome'
        return 'question_outcome'

    @staticmethod
    def request_message(request):
        data = json.loads(request.body)
        message = data["message"]
        return message

    @staticmethod
    def get_user_data_from_message(message):
        chat_id = message["chat"]["id"]
        username = message["chat"]["first_name"]
        return chat_id, username

    @staticmethod
    def get_text_from_message(message):
        try:
            text = message["text"].strip().lower()
        except Exception as e:
            print("Error: {}".format(e))
            return JsonResponse({"ok": "POST request processed"})
        return text

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(f"{TELEGRAM_URL}{WIKI_BOT_TOKEN}/sendMessage", data=data)

        if response.status_code == 200:
            return response
        return None

    def start_message(self, chat_id, username):
        message_text = "Witaj {}. Jestem WikiBot, zapytaj mnie o jakąś informację z Wikipedii, a dam Ci odpowiedź!"\
            .format(username)

        return self.send_message(message=message_text, chat_id=chat_id)

    @staticmethod
    def get_article(chat_id, text):
        Question.save_question(chat_id, text)
        context, article_id = search.search_text(text)
        return article_id, context

    def bot_answer(self, chat_id, text):
        article_id, context = self.get_article(chat_id, text)

        if context:
            answer_text = choose_model['second'](context, text)

            print("Answer: ", answer_text)

            Answer.save_answer(chat_id, article_id, context, answer_text)

            if len(answer_text) == 0:
                AnswerFeedback.save_answer_feedback(chat_id, False)
                return False, self.text_if_bot_do_not_know_answer(chat_id)

            else:
                return True, self.send_bot_answer(answer_text, chat_id)

        else:
            AnswerFeedback.save_answer_feedback(chat_id, False)
            return False, self.text_if_bot_do_not_know_answer(chat_id)

    def text_if_bot_do_not_know_answer(self, chat_id):
        return (self.send_message("Nie rozumiem Cię :(", chat_id),
                self.send_message("Zadaj pytanie w innny sposób ;)", chat_id))

    def send_bot_answer(self, answer, chat_id):
        return (self.send_message(answer, chat_id),
                self.send_message("Czy odpowiedziałem wyczerpująco na Twoje pytanie?", chat_id))

    def save_answer_feedback_and_send_message(self, feedback, chat_id):
        AnswerFeedback.save_answer_feedback(chat_id, feedback)

        return (self.send_message(custom_message.prepare_custom_message('output_answers', feedback), chat_id),
                self.send_message(custom_message.prepare_custom_message('next_questions', feedback), chat_id))

    def greet_message(self, chat_id):
        return self.send_message(custom_message.prepare_custom_message('greet_answers', 'greet'), chat_id)

    def sign_off_message(self, chat_id):
        return self.send_message(custom_message.prepare_custom_message('sign_off_answers', 'sign_off'), chat_id)

    def remind_about_answer_feedback_message(self, chat_id):
        return self.send_message(custom_message.prepare_custom_message('remind_about_answer_feedback', 'answer_feedback'), chat_id)


class BotLogicHandling(BotInteraction):

    def __init__(self, request):
        self.request = request
        self._chat = Chat()
        self._state = State()
        self._greeting = Greeting()

        self.received_message = self.request_message(request)
        self.received_chat_id, self.received_chat_username = self.get_user_data_from_message(self.received_message)
        self.received_text = self.get_text_from_message(self.received_message)

        self._chat.add_user_data_to_db(chat_id=self.received_chat_id, username=self.received_chat_username)

        self.last_state = self._state.get_last_state(self.received_chat_id)
        self.last_greeting = self._greeting.get_last_greeting(self.received_chat_id)

        self.outcome = self.check_outcome(self.received_text)

    def __repr__(self):
        return """{0}(request={1})
                  receive_text: {2}
                  last state (chat_id: {3}): {4}
                  last greeting (chat_id: {3}): {5}
                  """.format(
            BotLogicHandling.__name__,
            self.request,
            self.received_text,
            self.received_chat_id,
            self.last_state,
            self.last_greeting
        )

    @property
    def outcome_options(self):
        outcome_options = {
            'question': {
                'first_greet': {
                    'greet_outcome': self.change_first_greet_status_to_greet,
                    'greet_or_sign_off_outcome': self.change_first_greet_status_to_greet,
                    'sign_off_outcome': self.change_greet_status_to_sign_off,
                    'question_outcome': self.check_answer_valid_and_change_state_status_to_answer_feedback
                },
                'greet': {
                    'greet_or_sign_off_outcome': self.change_greet_status_to_sign_off,
                    'sign_off_outcome': self.change_greet_status_to_sign_off,
                    'question_outcome': self.check_answer_valid_and_change_state_status_to_answer_feedback
                },
                'sign_off': {
                    'greet_outcome': self.change_sign_off_status_to_greet,
                    'greet_or_sign_off_outcome': self.change_sign_off_status_to_greet,
                    'question_outcome': self.check_answer_valid_and_change_state_status_to_answer_feedback
                },
            },
            'answer_feedback': {
                'first_greet': {
                    'positive_answer_feedback_outcome': self.save_positive_feedback_and_change_state_to_question,
                    'negative_answer_feedback_outcome': self.save_negative_feedback_and_change_state_to_question,
                    'greet_outcome': self.change_first_greet_status_to_greet,
                    'greet_or_sign_off_outcome': self.change_greet_status_to_sign_off,
                    'sign_off_outcome': self.change_greet_status_to_sign_off,
                    'question_outcome': self.remind_about_answer_feedback
                },
                'greet': {
                    'positive_answer_feedback_outcome': self.save_positive_feedback_and_change_state_to_question,
                    'negative_answer_feedback_outcome': self.save_negative_feedback_and_change_state_to_question,
                    'greet_or_sign_off_outcome': self.change_greet_status_to_sign_off_and_change_state_status_to_question,
                    'sign_off_outcome': self.change_greet_status_to_sign_off_and_change_state_status_to_question,
                    'question_outcome': self.remind_about_answer_feedback
                },
                'sign_off': {
                    'positive_answer_feedback_outcome': self.save_positive_feedback_and_change_state_to_question,
                    'negative_answer_feedback_outcome': self.save_negative_feedback_and_change_state_to_question,
                    'greet_outcome': self.change_sign_off_status_to_greet_and_change_state_status_to_question,
                    'greet_or_sign_off_outcome': self.change_sign_off_status_to_greet_and_change_state_status_to_question,
                    'question_outcome': self.remind_about_answer_feedback
                },
            }
        }
        return outcome_options

    @property
    def bot_status(self):
        bot_status = {
            '/start': self.start,
            'after_start': self.outcome_options,
        }
        return bot_status

    def start(self):
        self._state.change_state(chat_id=self.received_chat_id, state='question')
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='first_greet')
        self.start_message(chat_id=self.received_chat_id, username=self.received_chat_username)

    def save_positive_feedback_and_change_state_to_question(self):
        self._state.change_state(chat_id=self.received_chat_id, state='question')
        self.save_answer_feedback_and_send_message(feedback=True, chat_id=self.received_chat_id)

    def save_negative_feedback_and_change_state_to_question(self):
        self._state.change_state(chat_id=self.received_chat_id, state='question')
        self.save_answer_feedback_and_send_message(feedback=False, chat_id=self.received_chat_id)

    def change_sign_off_status_to_greet_and_change_state_status_to_question(self):
        self._state.change_state(chat_id=self.received_chat_id, state='question')
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='greet')
        self.greet_message(chat_id=self.received_chat_id)

    def change_sign_off_status_to_greet(self):
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='greet')
        self.greet_message(chat_id=self.received_chat_id)

    def change_greet_status_to_sign_off_and_change_state_status_to_question(self):
        self._state.change_state(chat_id=self.received_chat_id, state='question')
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='sign_off')
        self.sign_off_message(chat_id=self.received_chat_id)

    def change_greet_status_to_sign_off(self):
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='sign_off')
        self.sign_off_message(chat_id=self.received_chat_id)

    def change_first_greet_status_to_greet(self):
        self._greeting.change_greeting(chat_id=self.received_chat_id, greeting='greet')

    def check_answer_valid_and_change_state_status_to_answer_feedback(self):
        check_answer, _ = self.bot_answer(chat_id=self.received_chat_id, text=self.received_text)
        if check_answer:
            self._state.change_state(chat_id=self.received_chat_id, state='answer_feedback')

    def remind_about_answer_feedback(self):
        self.remind_about_answer_feedback_message(chat_id=self.received_chat_id)
