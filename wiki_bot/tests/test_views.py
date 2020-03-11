from django.test import TestCase, RequestFactory

from unittest.mock import patch

from ..views import BotInteractionView
from ..bot_interactions import BotInteraction
from ..models import Chat, Question, State, Greeting
from .test_data import (data,
                        data_if_start,
                        data_if_question_and_greet,
                        data_if_question_and_greet_sign_off,
                        data_if_question_and_sign_off,
                        data_if_check_answer_and_outcome_true)


# Create your tests here.


class BotInteractionViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.biv = BotInteractionView()

    @patch.object(BotInteraction, 'start_chat')
    @patch.object(BotInteraction, 'get_text_from_message', return_value=data_if_start["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_start["message"]["chat"]["id"],
            data_if_start["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_start["message"])
    def test_post_if_start(self,
                           mock_request_message,
                           mock_get_user_data_from_message,
                           mock_get_text_from_message,
                           mock_start_chat):

        request = self.factory.post('/wiki_bot', data_if_start, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_start["message"])
        mock_get_text_from_message.assert_called_with(data_if_start["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        mock_start_chat.assert_called_with(_id=100, username='test_first_name')

    @patch.object(BotInteraction, 'user_question', return_value=(True, 'bot_answer'))
    @patch.object(BotInteraction, 'get_text_from_message', return_value=data["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data["message"]["chat"]["id"],
            data["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data["message"])
    def test_post_if_last_state_question(self,
                                         mock_request_message,
                                         mock_get_user_data_from_message,
                                         mock_get_text_from_message,
                                         mock_user_question):

        request = self.factory.post('/wiki_bot', data, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data["message"])
        mock_get_text_from_message.assert_called_with(data["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        mock_user_question.assert_called_with(_id=100, text='test text')
        self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')

    @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    @patch.object(BotInteraction, 'get_text_from_message',
                  return_value=data_if_question_and_greet["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_question_and_greet["message"]["chat"]["id"],
            data_if_question_and_greet["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet["message"])
    def test_post_if_last_state_question_and_outcome_greet(self,
                                                           mock_request_message,
                                                           mock_get_user_data_from_message,
                                                           mock_get_text_from_message,
                                                           mock_check_outcome_for_greeting):

        request = self.factory.post('/wiki_bot', data_if_question_and_greet, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet["message"])
        mock_get_text_from_message.assert_called_with(data_if_question_and_greet["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet')

    @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    @patch.object(BotInteraction, 'get_text_from_message',
                  return_value=data_if_question_and_greet_sign_off["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_question_and_greet_sign_off["message"]["chat"]["id"],
            data_if_question_and_greet_sign_off["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet_sign_off["message"])
    def test_post_if_last_state_question_and_outcome_greet_sign_off(self,
                                                                    mock_request_message,
                                                                    mock_get_user_data_from_message,
                                                                    mock_get_text_from_message,
                                                                    mock_check_outcome_for_greeting):

        request = self.factory.post('/wiki_bot', data_if_question_and_greet_sign_off, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet_sign_off["message"])
        mock_get_text_from_message.assert_called_with(data_if_question_and_greet_sign_off["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet-sign_off')

    @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    @patch.object(BotInteraction, 'get_text_from_message',
                  return_value=data_if_question_and_sign_off["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_question_and_sign_off["message"]["chat"]["id"],
            data_if_question_and_sign_off["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_sign_off["message"])
    def test_post_if_last_state_question_and_outcome_sign_off(self,
                                                              mock_request_message,
                                                              mock_get_user_data_from_message,
                                                              mock_get_text_from_message,
                                                              mock_check_outcome_for_greeting):

        request = self.factory.post('/wiki_bot', data_if_question_and_sign_off, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_question_and_sign_off["message"])
        mock_get_text_from_message.assert_called_with(data_if_question_and_sign_off["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='sign_off')

    @patch.object(BotInteraction, 'remind_about_check_answer')
    @patch.object(BotInteraction, 'get_text_from_message', return_value=data["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data["message"]["chat"]["id"],
            data["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data["message"])
    def test_post_if_last_state_check_answer(self,
                                             mock_request_message,
                                             mock_get_user_data_from_message,
                                             mock_get_text_from_message,
                                             mock_remind_about_check_answer):

        Chat(id=100, username='test_first_name').save()
        State(chat=Chat.objects.get(id=100), state='test_first_name').save()
        State.change_state(chat_id=100, state='check_answer')

        request = self.factory.post('/wiki_bot', data, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data["message"])
        mock_get_text_from_message.assert_called_with(data["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
        mock_remind_about_check_answer.assert_called_with(_id=100)

    @patch.object(BotInteractionView, 'check_outcome_for_feedback')
    @patch.object(BotInteraction, 'get_text_from_message',
                  return_value=data_if_check_answer_and_outcome_true["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_check_answer_and_outcome_true["message"]["chat"]["id"],
            data_if_check_answer_and_outcome_true["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_check_answer_and_outcome_true["message"])
    def test_post_if_last_state_check_answer_and_outcome_true(self,
                                                              mock_request_message,
                                                              mock_get_user_data_from_message,
                                                              mock_get_text_from_message,
                                                              mock_check_outcome_for_feedback):

        Chat(id=100, username='test_first_name').save()
        State(chat=Chat.objects.get(id=100), state='test_first_name').save()
        State.change_state(chat_id=100, state='check_answer')

        request = self.factory.post('/wiki_bot', data_if_check_answer_and_outcome_true, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_check_answer_and_outcome_true["message"])
        mock_get_text_from_message.assert_called_with(data_if_check_answer_and_outcome_true["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
        mock_check_outcome_for_feedback.assert_called_with(_id=100, outcome=True)

    @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    @patch.object(BotInteraction, 'get_text_from_message',
                  return_value=data_if_question_and_greet["message"]["text"].strip().lower())
    @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
            data_if_question_and_greet["message"]["chat"]["id"],
            data_if_question_and_greet["message"]["chat"]["first_name"])
                  )
    @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet["message"])
    def test_post_if_last_state_check_answer_and_outcome_greet(self,
                                                               mock_request_message,
                                                               mock_get_user_data_from_message,
                                                               mock_get_text_from_message,
                                                               mock_check_outcome_for_greeting):

        Chat(id=100, username='test_first_name').save()
        State(chat=Chat.objects.get(id=100), state='test_first_name').save()
        State.change_state(chat_id=100, state='check_answer')

        request = self.factory.post('/wiki_bot', data_if_question_and_greet, content_type='application/json')

        self.biv.post(request=request)
        mock_request_message.assert_called_with(request)
        mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet["message"])
        mock_get_text_from_message.assert_called_with(data_if_question_and_greet["message"])

        test_content = {
            'id': 100,
            'username': "test_first_name"
        }

        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
        mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet')

    @patch.object(BotInteraction, 'check_answer')
    def test_check_outcome_for_feedback(self, mock_check_answer):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        State.get_last_state(chat_id=100)

        self.biv.check_outcome_for_feedback(_id=100, outcome=True)
        mock_check_answer.assert_called_with(True, 100)
        self.assertEqual(State.get_last_state(chat_id=100), 'question')

        self.biv.check_outcome_for_feedback(_id=100, outcome=False)
        mock_check_answer.assert_called_with(False, 100)
        self.assertEqual(State.get_last_state(chat_id=100), 'question')

    @patch.object(BotInteraction, 'sign_off')
    @patch.object(BotInteraction, 'greet')
    def test_check_outcome_for_greeting_if_first_greet_and_greet(self, mock_greet, mock_sign_off):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        State.get_last_state(chat_id=100)
        Greeting.get_last_greeting(chat_id=100)

        self.biv.check_outcome_for_greeting(_id=100, last_greeting='first_greet', outcome='greet')
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'greet')
        self.assertFalse(mock_sign_off.called, "Function sign_off called")
        self.assertFalse(mock_greet.called, "Function greet called")

    @patch.object(BotInteraction, 'sign_off')
    @patch.object(BotInteraction, 'greet')
    def test_check_outcome_for_greeting_if_first_greet_and_sign_off(self, mock_greet, mock_sign_off):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        State.get_last_state(chat_id=100)
        Greeting.get_last_greeting(chat_id=100)

        self.biv.check_outcome_for_greeting(_id=100, last_greeting='first_greet', outcome='sign_off')
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'sign_off')
        mock_sign_off.assert_called_with(100)
        self.assertFalse(mock_greet.called, "Function greet called")

    @patch.object(BotInteraction, 'sign_off')
    @patch.object(BotInteraction, 'greet')
    def test_check_outcome_for_greeting_if_greet_and_sign_off(self, mock_greet, mock_sign_off):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        State.get_last_state(chat_id=100)
        Greeting.get_last_greeting(chat_id=100)

        self.biv.check_outcome_for_greeting(_id=100, last_greeting='greet', outcome='sign_off')
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'sign_off')
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        mock_sign_off.assert_called_with(100)
        self.assertFalse(mock_greet.called, "Function greet called")

    @patch.object(BotInteraction, 'sign_off')
    @patch.object(BotInteraction, 'greet')
    def test_check_outcome_for_greeting_if_sign_off_and_greet(self, mock_greet, mock_sign_off):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        State.get_last_state(chat_id=100)
        Greeting.get_last_greeting(chat_id=100)

        self.biv.check_outcome_for_greeting(_id=100, last_greeting='sign_off', outcome='greet')
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'greet')
        self.assertEqual(State.get_last_state(chat_id=100), 'question')
        self.assertFalse(mock_sign_off.called, "Function sign_off called")
        mock_greet.assert_called_with(100)
