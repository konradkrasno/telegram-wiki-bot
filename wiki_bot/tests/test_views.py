from django.test import TestCase, RequestFactory

from unittest.mock import patch

from wiki_bot.views import BotInteractionView
from wiki_bot.bot_logic import BotInteraction, BotLogicHandling
from wiki_bot.models import Chat, Question, State, Greeting
from wiki_bot.tests.test_data import (data,
                                      data_if_start,
                                      data_if_question_and_greet,
                                      data_if_question_and_greet_sign_off,
                                      data_if_question_and_sign_off,
                                      data_if_check_answer_and_outcome_true)


# Create your tests here.


class BotInteractionViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/wiki_bot', data_if_start, content_type='application/json')

    @patch.object(BotLogicHandling, 'start_message')
    @patch.object(Greeting, 'change_greeting')
    @patch.object(State, 'change_state')
    def test_post_when_start(self, mock_change_state, mock_change_greeting, mock_start_message):
        biv = BotInteractionView()
        biv.post(self.request)

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_change_greeting.assert_called_with(chat_id=100, greeting='first_greet')
        mock_start_message.assert_called_with(chat_id=100, username="test_first_name")

    # TODO finish tests
    def test_post_after_start(self):
        pass





    # @patch.object(BotInteraction, 'start_message')
    # @patch.object(BotInteraction, 'get_text_from_message', return_value=data_if_start["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_start["message"]["chat"]["id"],
    #         data_if_start["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_start["message"])
    # def test_post_if_start(self,
    #                        mock_request_message,
    #                        mock_get_user_data_from_message,
    #                        mock_get_text_from_message,
    #                        mock_start_message
    #                        ):
    #
    #     biv = BotInteractionView(self.request)
    #     biv.post(request=self.request)
    #     mock_request_message.assert_called_with(self.request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_start["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_start["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     mock_start_message.assert_called_with(_id=100, username="test_first_name")

    # @patch.object(BotInteraction, 'user_question', return_value=(True, 'bot_answer'))
    # @patch.object(BotInteraction, 'get_text_from_message', return_value=data["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data["message"]["chat"]["id"],
    #         data["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data["message"])
    # def test_post_if_last_state_question(self,
    #                                      mock_request_message,
    #                                      mock_get_user_data_from_message,
    #                                      mock_get_text_from_message,
    #                                      mock_user_question):
    #
    #     request = self.factory.post('/wiki_bot', data, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data["message"])
    #     mock_get_text_from_message.assert_called_with(data["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     mock_user_question.assert_called_with(_id=100, text='test text')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
    #
    # @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    # @patch.object(BotInteraction, 'get_text_from_message',
    #               return_value=data_if_question_and_greet["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_question_and_greet["message"]["chat"]["id"],
    #         data_if_question_and_greet["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet["message"])
    # def test_post_if_last_state_question_and_outcome_greet(self,
    #                                                        mock_request_message,
    #                                                        mock_get_user_data_from_message,
    #                                                        mock_get_text_from_message,
    #                                                        mock_check_outcome_for_greeting):
    #
    #     request = self.factory.post('/wiki_bot', data_if_question_and_greet, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_question_and_greet["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet')
    #
    # @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    # @patch.object(BotInteraction, 'get_text_from_message',
    #               return_value=data_if_question_and_greet_sign_off["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_question_and_greet_sign_off["message"]["chat"]["id"],
    #         data_if_question_and_greet_sign_off["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet_sign_off["message"])
    # def test_post_if_last_state_question_and_outcome_greet_sign_off(self,
    #                                                                 mock_request_message,
    #                                                                 mock_get_user_data_from_message,
    #                                                                 mock_get_text_from_message,
    #                                                                 mock_check_outcome_for_greeting):
    #
    #     request = self.factory.post('/wiki_bot', data_if_question_and_greet_sign_off, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet_sign_off["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_question_and_greet_sign_off["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet-sign_off')
    #
    # @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    # @patch.object(BotInteraction, 'get_text_from_message',
    #               return_value=data_if_question_and_sign_off["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_question_and_sign_off["message"]["chat"]["id"],
    #         data_if_question_and_sign_off["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_sign_off["message"])
    # def test_post_if_last_state_question_and_outcome_sign_off(self,
    #                                                           mock_request_message,
    #                                                           mock_get_user_data_from_message,
    #                                                           mock_get_text_from_message,
    #                                                           mock_check_outcome_for_greeting):
    #
    #     request = self.factory.post('/wiki_bot', data_if_question_and_sign_off, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_question_and_sign_off["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_question_and_sign_off["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='sign_off')
    #
    # @patch.object(BotInteraction, 'remind_about_check_answer')
    # @patch.object(BotInteraction, 'get_text_from_message', return_value=data["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data["message"]["chat"]["id"],
    #         data["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data["message"])
    # def test_post_if_last_state_check_answer(self,
    #                                          mock_request_message,
    #                                          mock_get_user_data_from_message,
    #                                          mock_get_text_from_message,
    #                                          mock_remind_about_check_answer):
    #
    #     Chat(id=100, username='test_first_name').save()
    #     State(chat=Chat.objects.get(id=100), state='test_first_name').save()
    #     State.change_state(chat_id=100, state='check_answer')
    #
    #     request = self.factory.post('/wiki_bot', data, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data["message"])
    #     mock_get_text_from_message.assert_called_with(data["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
    #     mock_remind_about_check_answer.assert_called_with(_id=100)
    #
    # @patch.object(BotInteractionView, 'check_outcome_for_feedback')
    # @patch.object(BotInteraction, 'get_text_from_message',
    #               return_value=data_if_check_answer_and_outcome_true["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_check_answer_and_outcome_true["message"]["chat"]["id"],
    #         data_if_check_answer_and_outcome_true["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_check_answer_and_outcome_true["message"])
    # def test_post_if_last_state_check_answer_and_outcome_true(self,
    #                                                           mock_request_message,
    #                                                           mock_get_user_data_from_message,
    #                                                           mock_get_text_from_message,
    #                                                           mock_check_outcome_for_feedback):
    #
    #     Chat(id=100, username='test_first_name').save()
    #     State(chat=Chat.objects.get(id=100), state='test_first_name').save()
    #     State.change_state(chat_id=100, state='check_answer')
    #
    #     request = self.factory.post('/wiki_bot', data_if_check_answer_and_outcome_true, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_check_answer_and_outcome_true["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_check_answer_and_outcome_true["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
    #     mock_check_outcome_for_feedback.assert_called_with(_id=100, outcome=True)
    #
    # @patch.object(BotInteractionView, 'check_outcome_for_greeting')
    # @patch.object(BotInteraction, 'get_text_from_message',
    #               return_value=data_if_question_and_greet["message"]["text"].strip().lower())
    # @patch.object(BotInteraction, 'get_user_data_from_message', return_value=(
    #         data_if_question_and_greet["message"]["chat"]["id"],
    #         data_if_question_and_greet["message"]["chat"]["first_name"])
    #               )
    # @patch.object(BotInteraction, 'request_message', return_value=data_if_question_and_greet["message"])
    # def test_post_if_last_state_check_answer_and_outcome_greet(self,
    #                                                            mock_request_message,
    #                                                            mock_get_user_data_from_message,
    #                                                            mock_get_text_from_message,
    #                                                            mock_check_outcome_for_greeting):
    #
    #     Chat(id=100, username='test_first_name').save()
    #     State(chat=Chat.objects.get(id=100), state='test_first_name').save()
    #     State.change_state(chat_id=100, state='check_answer')
    #
    #     request = self.factory.post('/wiki_bot', data_if_question_and_greet, content_type='application/json')
    #
    #     self.biv.post(request=request)
    #     mock_request_message.assert_called_with(request)
    #     mock_get_user_data_from_message.assert_called_with(data_if_question_and_greet["message"])
    #     mock_get_text_from_message.assert_called_with(data_if_question_and_greet["message"])
    #
    #     test_content = {
    #         'id': 100,
    #         'username': "test_first_name"
    #     }
    #
    #     self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'check_answer')
    #     mock_check_outcome_for_greeting.assert_called_with(_id=100, last_greeting='first_greet', outcome='greet')
