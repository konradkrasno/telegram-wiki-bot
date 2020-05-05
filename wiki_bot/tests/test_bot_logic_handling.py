from django.test import TestCase, RequestFactory

from unittest.mock import patch

from wiki_bot.bot_logic import BotInteraction, BotLogicHandling
from wiki_bot.models import State, Greeting


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


class BotLogicHandlingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/wiki_bot', fake_data, content_type='application/json')
        self.blh = BotLogicHandling(self.request)

    # TODO finish all tests

    @patch.object(BotInteraction, 'start_message')
    @patch.object(Greeting, 'change_greeting')
    @patch.object(State, 'change_state')
    def test_start(self, mock_change_state, mock_change_greeting, mock_start_message):
        self.blh.start()

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_change_greeting.assert_called_with(chat_id=100, greeting='first_greet')
        mock_start_message.assert_called_with(chat_id=100, username='test_first_name')

    @patch.object(BotInteraction, 'save_answer_feedback_and_send_message')
    @patch.object(State, 'change_state')
    def test_save_positive_feedback_and_change_state_to_question(self,
                                                                 mock_change_state,
                                                                 mock_save_answer_feedback_and_send_message):

        self.blh.save_positive_feedback_and_change_state_to_question()

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_save_answer_feedback_and_send_message.assert_called_with(feedback=True, chat_id=100)

    @patch.object(BotInteraction, 'save_answer_feedback_and_send_message')
    @patch.object(State, 'change_state')
    def test_save_negative_feedback_and_change_state_to_question(self,
                                                                 mock_change_state,
                                                                 mock_save_answer_feedback_and_send_message):

        self.blh.save_negative_feedback_and_change_state_to_question()

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_save_answer_feedback_and_send_message.assert_called_with(feedback=False, chat_id=100)

    @patch.object(BotInteraction, 'greet_message')
    @patch.object(Greeting, 'change_greeting')
    @patch.object(State, 'change_state')
    def test_change_sign_off_status_to_greet_and_change_state_status_to_question(self,
                                                                                 mock_change_state,
                                                                                 mock_change_greeting,
                                                                                 mock_greet_message):

        self.blh.change_sign_off_status_to_greet_and_change_state_status_to_question()

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_change_greeting.assert_called_with(chat_id=100, greeting='greet')
        mock_greet_message.assert_called_with(chat_id=100)

    @patch.object(BotInteraction, 'greet_message')
    @patch.object(Greeting, 'change_greeting')
    def test_change_sign_off_status_to_greet(self,
                                             mock_change_greeting,
                                             mock_greet_message):

        self.blh.change_sign_off_status_to_greet()

        mock_change_greeting.assert_called_with(chat_id=100, greeting='greet')
        mock_greet_message.assert_called_with(chat_id=100)

    @patch.object(BotInteraction, 'sign_off_message')
    @patch.object(Greeting, 'change_greeting')
    @patch.object(State, 'change_state')
    def test_change_greet_status_to_sign_off_and_change_state_status_to_question(self,
                                                                                 mock_change_state,
                                                                                 mock_change_greeting,
                                                                                 mock_sign_off_message):

        self.blh.change_greet_status_to_sign_off_and_change_state_status_to_question()

        mock_change_state.assert_called_with(chat_id=100, state='question')
        mock_change_greeting.assert_called_with(chat_id=100, greeting='sign_off')
        mock_sign_off_message.assert_called_with(chat_id=100)

    @patch.object(BotInteraction, 'sign_off_message')
    @patch.object(Greeting, 'change_greeting')
    def test_change_greet_status_to_sign_off(self, mock_change_greeting, mock_sign_off_message):
        self.blh.change_greet_status_to_sign_off()

        mock_change_greeting.assert_called_with(chat_id=100, greeting='sign_off')
        mock_sign_off_message.assert_called_with(chat_id=100)

    @patch.object(Greeting, 'change_greeting')
    def test_change_first_greet_status_to_greet(self, mock_change_greeting):
        self.blh.change_first_greet_status_to_greet()

        mock_change_greeting.assert_called_with(chat_id=100, greeting='greet')

    @patch.object(State, 'change_state')
    @patch.object(BotInteraction, 'bot_answer', return_value=(False, None))
    def test_check_answer_valid_and_change_state_status_to_answer_feedback_if_check_answer_is_False(self,
                                                                                                   mock_bot_answer,
                                                                                                   mock_change_state):
        self.blh.check_answer_valid_and_change_state_status_to_answer_feedback()

        mock_bot_answer.assert_called_with(chat_id=100, text='test text')
        mock_change_state.assert_not_called()

    @patch.object(State, 'change_state')
    @patch.object(BotInteraction, 'bot_answer', return_value=(True, None))
    def test_check_answer_valid_and_change_state_status_to_answer_feedback_if_check_answer_is_True(self,
                                                                                                   mock_bot_answer,
                                                                                                   mock_change_state):
        self.blh.check_answer_valid_and_change_state_status_to_answer_feedback()

        mock_bot_answer.assert_called_with(chat_id=100, text='test text')
        mock_change_state.assert_called_with(chat_id=100, state='answer_feedback')

    @patch.object(BotInteraction, 'remind_about_answer_feedback_message')
    def test_remind_about_answer_feedback(self, mock_remind_about_answer_feedback_message):
        self.blh.remind_about_answer_feedback()

        mock_remind_about_answer_feedback_message.assert_called_with(chat_id=100)
