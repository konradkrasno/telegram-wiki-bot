from django.test import TestCase, RequestFactory
from unittest.mock import Mock, patch

from wiki_bot.bot_logic import BotInteraction
from wiki_bot.models import Chat, Question, Answer, AnswerFeedback
from wiki_bot.custom_message import custom_messages


fake_data = {'update_id': 10000000,
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
                         'text': 'test text'
                         }
             }

fake_json_data = {
    "ok": True,
    "result":
        {"message_id": 1234,
         "from": {"id": 996463999,
                  "is_bot": True,
                  "first_name": "WikiBot",
                  "username": "kondzio_bot"},
         "chat": {"id": 100,
                  "first_name": "test_first_name",
                  "last_name": "test_last_name",
                  "type": "private"},
         "date": 1582900572,
         "text": "test message"
         }
}


class BotInteractionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bi = BotInteraction()

    def test_check_outcome(self):
        self.assertEqual(self.bi.check_outcome('/something'), 'external_command_outcome')
        self.assertEqual(self.bi.check_outcome('/start'), 'start_outcome')

    def test_request_message(self):
        request = self.factory.post('/wiki_bot', fake_data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        self.assertDictEqual(msg, fake_data["message"])

    def test_get_user_data_from_message(self):
        request = self.factory.post('/wiki_bot', fake_data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        (_id, username) = BotInteraction.get_user_data_from_message(msg)
        self.assertTupleEqual((_id, username), (100, 'test_first_name'))

    def test_get_text_from_message(self):
        request = self.factory.post('/wiki_bot', fake_data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        text = BotInteraction.get_text_from_message(msg)
        self.assertEqual(text, 'test text')

    def test_get_text_from_message_if_text_is_empty(self):
        fake_data["message"]["text"] = ''
        request = self.factory.post('/wiki_bot', fake_data, content_type='application/json')
        msg = BotInteraction.request_message(request)
        text = BotInteraction.get_text_from_message(msg)
        self.assertEqual(text, '')

    def test_send_message(self):
        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_response = BotInteraction.send_message(message="test message", chat_id=100)

        mock_get_patcher.stop()

        self.assertIsNotNone(mock_response)
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(mock_response.json(), fake_json_data)

    def test_start_message(self):
        fake_json_data["result"]["text"] = "Witaj TestUser. Jestem WikiBot, zapytaj mnie o jakąś informację" \
                                           " z Wikipedii, a dam Ci odpowiedź!"

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_response = self.bi.start_message(chat_id=100, username="TestUser")

        mock_get_patcher.stop()

        start_text = mock_response.json()["result"]["text"]
        start_message = "Witaj {}. Jestem WikiBot, zapytaj mnie o jakąś informację z Wikipedii, a dam Ci odpowiedź!"\
            .format("TestUser")

        self.assertEqual(start_text, start_message)

    def mock_context_and_answer(self, question_text, mock_context, mock_article_id, mock_answer_text):
        def fake_model(context, text):
            return mock_answer_text

        mock_post_patcher = patch('wiki_bot.bot_logic.requests.post')
        mock_search_text_patcher = patch('wiki_bot.bot_logic.search.search_text')
        mock_choose_model_patcher = patch.dict('wiki_bot.bot_logic.choose_model',
                                               {'first': fake_model, 'second': fake_model})

        mock_post = mock_post_patcher.start()
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = fake_json_data

        mock_search_text = mock_search_text_patcher.start()
        mock_search_text.return_value = mock_context, mock_article_id

        mock_choose_model = mock_choose_model_patcher.start()

        _, mock_question = self.bi.bot_answer(chat_id=100, text=question_text)

        mock_choose_model_patcher.stop()
        mock_search_text_patcher.stop()
        mock_post_patcher.stop()

        msg_text_1 = mock_question[0].json()["result"]["text_1"]
        msg_text_2 = mock_question[1].json()["result"]["text_2"]

        return msg_text_1, msg_text_2

    def test_bot_answer_if_bot_know_answer(self):
        context_text = "This is context text"
        question_text = "This is question text"
        answer_text = "This is answer text"
        fake_json_data["result"]["text_1"] = "This is answer text"
        fake_json_data["result"]["text_2"] = "Czy odpowiedziałem wyczerpująco na Twoje pytanie?"

        Chat(id=100, username='test_user').save()

        msg_text_1, msg_text_2 = self.mock_context_and_answer(question_text=question_text,
                                                              mock_context=context_text,
                                                              mock_article_id=100,
                                                              mock_answer_text=answer_text)

        test_content_question = {
            'chat': 100,
            'question_text': question_text
        }
        test_content_answer = {
            'chat': 100,
            'article_id': 100,
            'answer_text': answer_text
        }

        self.assertEqual(msg_text_1, answer_text)
        self.assertEqual(msg_text_2, "Czy odpowiedziałem wyczerpująco na Twoje pytanie?")
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content_question)
        self.assertDictEqual(Answer.objects.values('chat', 'article_id', 'answer_text')[0], test_content_answer)

    def test_bot_answer_if_bot_do_not_know_answer(self):
        context_text = "This is context text"
        question_text = "This is question text"
        answer_text = ""
        fake_json_data["result"]["text_1"] = "Nie rozumiem Cię :("
        fake_json_data["result"]["text_2"] = "Zadaj pytanie w innny sposób ;)"

        Chat(id=100, username='test_user').save()

        msg_text_1, msg_text_2 = self.mock_context_and_answer(question_text=question_text,
                                                              mock_context=context_text,
                                                              mock_article_id=100,
                                                              mock_answer_text=answer_text)

        test_content_question = {
            'chat': 100,
            'question_text': question_text
        }
        test_content_answer = {
            'chat': 100,
            'article_id': 100,
            'answer_text': ""
        }
        test_content_answer_feedback = {
            'chat': 100,
            'if_right': False,
        }

        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content_question)
        self.assertDictEqual(Answer.objects.values('chat', 'article_id', 'answer_text')[0],
                             test_content_answer)
        self.assertDictEqual(AnswerFeedback.objects.values('chat', 'if_right')[0],
                             test_content_answer_feedback)

    def test_bot_answer_if_bot_do_not_find_article_to_answer(self):
        context_text = None
        question_text = "This is question text"
        answer_text = None
        fake_json_data["result"]["text_1"] = "Nie rozumiem Cię :("
        fake_json_data["result"]["text_2"] = "Zadaj pytanie w innny sposób ;)"

        Chat(id=100, username='test_user').save()

        msg_text_1, msg_text_2 = self.mock_context_and_answer(question_text=question_text,
                                                              mock_context=context_text,
                                                              mock_article_id=None,
                                                              mock_answer_text=answer_text)

        test_content_question = {
            'chat': 100,
            'question_text': question_text
        }
        test_content_answer_feedback = {
            'chat': 100,
            'if_right': False,
        }

        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")
        self.assertDictEqual(Question.objects.values('chat', 'question_text').first(), test_content_question)
        self.assertDictEqual(AnswerFeedback.objects.values('chat', 'if_right').first(),
                             test_content_answer_feedback)

    def test_text_if_bot_do_not_know_answer(self):
        fake_json_data["result"]["text_1"] = "Nie rozumiem Cię :("
        fake_json_data["result"]["text_2"] = "Zadaj pytanie w innny sposób ;)"

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        bot_text = self.bi.text_if_bot_do_not_know_answer(chat_id=100)

        mock_get_patcher.stop()

        msg_text_1 = bot_text[0].json()["result"]["text_1"]
        msg_text_2 = bot_text[1].json()["result"]["text_2"]

        self.assertEqual(msg_text_1, "Nie rozumiem Cię :(")
        self.assertEqual(msg_text_2, "Zadaj pytanie w innny sposób ;)")

    def test_send_bot_answer(self):
        fake_json_data["result"]["text_1"] = "test answer"
        fake_json_data["result"]["text_2"] = "Czy odpowiedziałem wyczerpująco na Twoje pytanie?"

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        bot_answer = self.bi.send_bot_answer(answer='test answer', chat_id=100)

        mock_get_patcher.stop()

        msg_text_1 = bot_answer[0].json()["result"]["text_1"]
        msg_text_2 = bot_answer[1].json()["result"]["text_2"]

        self.assertEqual(msg_text_1, "test answer")
        self.assertEqual(msg_text_2, "Czy odpowiedziałem wyczerpująco na Twoje pytanie?")

    def test_save_answer_feedback_and_send_message_if_true(self):
        fake_json_data["result"]["text_1"] = 'Super!'
        fake_json_data["result"]["text_2"] = "Zadaj mi jeszcze jakieś pytanie ;)"

        feedback = True
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_check = self.bi.save_answer_feedback_and_send_message(feedback=feedback, chat_id=100)

        mock_get_patcher.stop()

        test_content = {
            'chat': 100,
            'if_right': feedback,
        }
        self.assertDictEqual(AnswerFeedback.objects.values('chat', 'if_right')[0],
                             test_content)

        msg_text_1 = mock_check[0].json()["result"]["text_1"]
        msg_text_2 = mock_check[1].json()["result"]["text_2"]
        self.assertIn(msg_text_1, custom_messages["output_answers"][feedback])
        self.assertIn(msg_text_2, custom_messages["next_questions"][feedback])

    def test_save_answer_feedback_and_send_message_if_false(self):
        fake_json_data["result"]["text_1"] = 'Szkoda ;('
        fake_json_data["result"]["text_2"] = "Zadaj pytanie w innny sposób ;)"

        feedback = False
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_check = self.bi.save_answer_feedback_and_send_message(feedback=feedback, chat_id=100)

        mock_get_patcher.stop()

        test_content = {
            'chat': 100,
            'if_right': feedback,
        }
        self.assertDictEqual(AnswerFeedback.objects.values('chat', 'if_right')[0],
                             test_content)

        msg_text_1 = mock_check[0].json()["result"]["text_1"]
        msg_text_2 = mock_check[1].json()["result"]["text_2"]
        self.assertIn(msg_text_1, custom_messages["output_answers"][feedback])
        self.assertIn(msg_text_2, custom_messages["next_questions"][feedback])

    def test_greet(self):
        fake_json_data["result"]["text"] = 'Witaj, w czym mogę Ci pomóc?'

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_greet = self.bi.greet_message(chat_id=100)

        mock_get_patcher.stop()

        msg_text = mock_greet.json()["result"]["text"]
        self.assertIn(msg_text, custom_messages["greet_answers"]["greet"])

    def test_sign_off(self):
        fake_json_data["result"]["text"] = 'Do zobaczenia ponownie'

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_sign_off = self.bi.sign_off_message(chat_id=100)

        mock_get_patcher.stop()

        msg_text = mock_sign_off.json()["result"]["text"]
        self.assertIn(msg_text, custom_messages["sign_off_answers"]["sign_off"])

    def test_remind_about_answer_feedback(self):
        fake_json_data["result"]["text"] = 'Nie powiedziałeś czy dobrze odpowiedzałem'

        mock_get_patcher = patch('wiki_bot.bot_logic.requests.post')

        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = fake_json_data

        mock_remind = self.bi.remind_about_answer_feedback_message(chat_id=100)

        mock_get_patcher.stop()

        msg_text = mock_remind.json()["result"]["text"]
        self.assertIn(msg_text, custom_messages["remind_about_answer_feedback"]["answer_feedback"])
