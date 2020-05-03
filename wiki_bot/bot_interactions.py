import requests

import json
from django.http import JsonResponse


from wiki_bot.models import Question, Answer, CheckAnswer
from wiki_bot.bot_settings import TELEGRAM_URL, WIKI_BOT_TOKEN
from wiki_bot import custom_message, search
# from wiki_bot.qa_models import qaClass
from wiki_bot import custom_message

# from deeppavlov import build_model, configs
# model_qa_ml = build_model(configs.squad.squad_bert_multilingual_freezed_emb, download=False)


class BotInteraction:
    @staticmethod
    def request_message(request):
        data = json.loads(request.body)
        message = data["message"]
        return message

    @staticmethod
    def get_user_data_from_message(message):
        _id = message["chat"]["id"]
        username = message["chat"]["first_name"]
        return _id, username

    @staticmethod
    def get_text_from_message(message):
        try:
            text = message["text"].strip().lower()
        except Exception as e:
            print(e)
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

    def start_chat(self, _id, username):
        message_text = "Witaj {}. Jestem WikiBot, zapytaj mnie o jakąś informację z Wikipedii, a dam Ci odpowiedź!"\
            .format(username)

        return self.send_message(message=message_text, chat_id=_id)

    @staticmethod
    def get_answer(_id, text):
        Question.save_question(_id, text)
        context, article_id = search.search_text(text)
        return article_id, context

    def bot_answer(self, _id, text):
        article_id, context = self.get_answer(_id, text)

        if context:
            # answer_text = model_qa_ml([context], [text])[0][0]
            # answer_text = qaClass.get_answer_from_text(text=context, question=text)
            answer_text = 'This is answer text'

            print("Answer: ", answer_text)

            Answer.save_answer(_id, article_id, context, answer_text)

            if len(answer_text) == 0:
                CheckAnswer.save_check_answer(_id, False)
                return False, self.text_if_bot_do_not_know_answer(_id)

            else:
                return True, self.send_bot_answer(answer_text, _id)

        else:
            CheckAnswer.save_check_answer(_id, False)
            return False, self.text_if_bot_do_not_know_answer(_id)

    def text_if_bot_do_not_know_answer(self, _id):
        return (self.send_message("Nie rozumiem Cię :(", _id),
                self.send_message("Zadaj pytanie w innny sposób ;)", _id))

    def send_bot_answer(self, answer, _id):
        return (self.send_message(answer, _id),
                self.send_message("Czy odpowiedziałem wyczerpująco na Twoje pytanie?", _id))

    def check_user_answer(self, outcome, _id):
        CheckAnswer.save_check_answer(_id, outcome)

        return (self.send_message(custom_message.prepare_custom_message('output_answers', outcome), _id),
                self.send_message(custom_message.prepare_custom_message('next_questions', outcome), _id))

    def greet(self, _id):
        return self.send_message(custom_message.prepare_custom_message('greet_answers', 'greet'), _id)

    def sign_off(self, _id):
        return self.send_message(custom_message.prepare_custom_message('sign_off_answers', 'sign_off'), _id)

    def remind_about_check_answer(self, _id):
        return self.send_message(custom_message.prepare_custom_message('remind_about_check_answer', 'check_answer'), _id)
