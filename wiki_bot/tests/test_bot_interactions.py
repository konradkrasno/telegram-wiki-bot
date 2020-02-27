from django.test import TestCase, RequestFactory

from wiki_bot.bot_interactions import BotInteraction
from wiki_bot.models import Chat, Question, Answer, CheckAnswer
from wiki_bot.custom_message import custom_messages

import json

with open('secure.json', 'r') as file:
    secure = json.load(file)


# Create your tests here.


class BotInteractionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.data = {'update_id': 10000000,
                     'message': {'message_id': 1234,
                                 'from': {'id': 100,
                                          'is_bot': False,
                                          'first_name': 'test_first_name',
                                          'last_name': 'test_last_name',
                                          'language_code': 'pl'},
                                 'chat': {'id': 100,
                                          'first_name': 'test_first_name',
                                          'last_name': 'test_last_name',
                                          'type': 'private'},
                                 'date': 1582723459,
                                 'text': 'test text'}}
        self.bi = BotInteraction()

    def test_request_message(self):
        request = self.factory.post('/wiki_bot', self.data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        self.assertDictEqual(msg, self.data["message"])

    def test_get_user_data_from_message(self):
        request = self.factory.post('/wiki_bot', self.data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        (_id, username) = BotInteraction.get_user_data_from_message(msg)
        self.assertTupleEqual((_id, username), (100, 'test_first_name'))

    def test_get_text_from_message(self):
        request = self.factory.post('/wiki_bot', self.data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        text = BotInteraction.get_text_from_message(msg)
        self.assertEqual(text, 'test text')

    def test_get_text_from_message_if_text_is_empty(self):
        self.data["message"]["text"] = ''
        request = self.factory.post('/wiki_bot', self.data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        text = BotInteraction.get_text_from_message(msg)
        self.assertEqual(text, '')

    def test_send_message(self):
        msg = BotInteraction.send_message(message='test message', chat_id=secure["TEST_CHAT_ID"])
        msg_text = json.loads(msg.content)["result"]["text"]
        self.assertEqual(msg_text, "test message")

    def test_start_chat(self):
        start = self.bi.start_chat(_id=secure["TEST_CHAT_ID"], username="test")

        start_text = json.loads(start.content)["result"]["text"]

        start_message = "Witaj {}. Jestem WikiBot, zapytaj mnie o jakąś informację z Wikipedii, a dam Ci odpowiedź!"\
            .format("test")

        test_content = {
            'id': secure["TEST_CHAT_ID"],
            'username': "test"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(start_text, start_message)

    def test_user_question_if_bot_know_answer(self):
        question_text = "Kto to był Adam Mickiewicz?"
        answer_text = "dowódca wojskowy"
        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()

        _, user_question = self.bi.user_question(_id=secure["TEST_CHAT_ID"], text=question_text)
        msg_text_1 = json.loads(user_question[0].content)["result"]["text"]
        msg_text_2 = json.loads(user_question[1].content)["result"]["text"]

        test_content_question = {
            'chat': secure["TEST_CHAT_ID"],
            'question_text': question_text
        }
        test_content_answer = {
            'chat': secure["TEST_CHAT_ID"],
            'article_id': 293,
            'answer_text': answer_text
        }

        self.assertEqual(msg_text_1, answer_text)
        self.assertEqual(msg_text_2, "Czy odpowiedziałem wyczerpująco na Twoje pytanie?")
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content_question)
        self.assertDictEqual(Answer.objects.values('chat', 'article_id', 'answer_text')[0], test_content_answer)

    def test_user_question_if_bot_do_not_know_answer(self):
        question_text = "Kto jest prezydentem Polski?"
        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()

        _, user_question = self.bi.user_question(_id=secure["TEST_CHAT_ID"], text=question_text)
        msg_text_1 = json.loads(user_question[0].content)["result"]["text"]
        msg_text_2 = json.loads(user_question[1].content)["result"]["text"]

        test_content_question = {
            'chat': secure["TEST_CHAT_ID"],
            'question_text': question_text
        }
        test_content_answer = {
            'chat': secure["TEST_CHAT_ID"],
            'article_id': 4681,
            'answer_text': ""
        }
        test_content_check_answer = {
            'question': 1,
            'chat': secure["TEST_CHAT_ID"],
            'if_right': False,
        }

        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content_question)
        self.assertDictEqual(Answer.objects.values('chat', 'article_id', 'answer_text')[0],
                             test_content_answer)
        self.assertDictEqual(CheckAnswer.objects.values('question', 'chat', 'if_right')[0],
                             test_content_check_answer)

    def test_user_question_if_bot_do_not_find_article_to_answer(self):
        question_text = ""

        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()

        _, user_question = self.bi.user_question(_id=secure["TEST_CHAT_ID"], text=question_text)
        msg_text_1 = json.loads(user_question[0].content)["result"]["text"]
        msg_text_2 = json.loads(user_question[1].content)["result"]["text"]

        test_content_question = {
            'chat': secure["TEST_CHAT_ID"],
            'question_text': question_text
        }
        test_content_check_answer = {
            'question': 1,
            'chat': secure["TEST_CHAT_ID"],
            'if_right': False,
        }

        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content_question)
        self.assertDictEqual(CheckAnswer.objects.values('question', 'chat', 'if_right')[0],
                             test_content_check_answer)

    def test_text_if_bot_do_not_know_answer(self):
        bot_text = self.bi.text_if_bot_do_not_know_answer(_id=secure["TEST_CHAT_ID"])
        msg_text_1 = json.loads(bot_text[0].content)["result"]["text"]
        msg_text_2 = json.loads(bot_text[1].content)["result"]["text"]
        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")

    def test_send_bot_answer(self):
        bot_answer = self.bi.send_bot_answer(answer='test answer', _id=secure["TEST_CHAT_ID"])
        msg_text_1 = json.loads(bot_answer[0].content)["result"]["text"]
        msg_text_2 = json.loads(bot_answer[1].content)["result"]["text"]
        self.assertEqual(msg_text_1, "test answer")
        self.assertEqual(msg_text_2, "Czy odpowiedziałem wyczerpująco na Twoje pytanie?")

    def test_check_answer_if_true(self):
        outcome = True
        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()
        Question.save_question(chat_id=secure["TEST_CHAT_ID"], question='test_question')
        check = self.bi.check_answer(outcome=outcome, _id=secure["TEST_CHAT_ID"])

        test_content = {
            'chat': secure["TEST_CHAT_ID"],
            'if_right': outcome,
        }
        self.assertDictEqual(CheckAnswer.objects.values('chat', 'if_right')[0],
                             test_content)

        msg_text_1 = json.loads(check[0].content)["result"]["text"]
        msg_text_2 = json.loads(check[1].content)["result"]["text"]
        self.assertIn(msg_text_1, custom_messages["output_answers"][outcome])
        self.assertIn(msg_text_2, custom_messages["next_questions"][outcome])

    def test_check_answer_if_false(self):
        outcome = False
        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()
        Question.save_question(chat_id=secure["TEST_CHAT_ID"], question='test_question')
        check = self.bi.check_answer(outcome=outcome, _id=secure["TEST_CHAT_ID"])

        test_content = {
            'chat': secure["TEST_CHAT_ID"],
            'if_right': outcome,
        }
        self.assertDictEqual(CheckAnswer.objects.values('chat', 'if_right')[0],
                             test_content)

        msg_text_1 = json.loads(check[0].content)["result"]["text"]
        msg_text_2 = json.loads(check[1].content)["result"]["text"]
        self.assertIn(msg_text_1, custom_messages["output_answers"][outcome])
        self.assertIn(msg_text_2, custom_messages["next_questions"][outcome])

    def test_greet(self):
        greet = self.bi.greet(_id=secure["TEST_CHAT_ID"])
        msg_text = json.loads(greet.content)["result"]["text"]
        self.assertIn(msg_text, custom_messages["greet_answers"]["greet"])

    def test_sign_off(self):
        sign_off = self.bi.sign_off(_id=secure["TEST_CHAT_ID"])
        msg_text = json.loads(sign_off.content)["result"]["text"]
        self.assertIn(msg_text, custom_messages["sign_off_answers"]["sign_off"])

    def test_remind_about_check_answer(self):
        remind = self.bi.remind_about_check_answer(_id=secure["TEST_CHAT_ID"])
        msg_text = json.loads(remind.content)["result"]["text"]
        self.assertIn(msg_text, custom_messages["remind_about_check_answer"]["check_answer"])
