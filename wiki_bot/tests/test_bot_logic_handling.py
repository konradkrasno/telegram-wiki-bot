from django.test import TestCase, RequestFactory

from unittest.mock import patch

from wiki_bot.views import BotInteractionView
from wiki_bot.bot_interactions import BotInteraction
from wiki_bot.models import Chat, Question, State, Greeting

# Create your tests here.


class BotInteractionViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.biv = BotInteractionView()

    # @patch.object(BotInteraction, 'check_user_answer')
    # def test_check_outcome_for_feedback(self, mock_check_user_answer):
    #     Chat(id=100, username='test_user').save()
    #     Question.save_question(chat_id=100, question='test_question')
    #     State.get_last_state(chat_id=100)
    #
    #     self.biv.change_feedback_status(_id=100, outcome=True)
    #     mock_check_user_answer.assert_called_with(True, 100)
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #
    #     self.biv.change_feedback_status(_id=100, outcome=False)
    #     mock_check_user_answer.assert_called_with(False, 100)
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #
    # @patch.object(BotInteraction, 'sign_off')
    # @patch.object(BotInteraction, 'greet')
    # def test_check_outcome_for_greeting_if_first_greet_and_greet(self, mock_greet, mock_sign_off):
    #     Chat(id=100, username='test_user').save()
    #     Question.save_question(chat_id=100, question='test_question')
    #     State.get_last_state(chat_id=100)
    #     Greeting.get_last_greeting(chat_id=100)
    #
    #     self.biv.change_greeting_status(_id=100, last_greeting='first_greet', outcome='greet')
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'greet')
    #     self.assertFalse(mock_sign_off.called, "Function sign_off called")
    #     self.assertFalse(mock_greet.called, "Function greet called")
    #
    # @patch.object(BotInteraction, 'sign_off')
    # @patch.object(BotInteraction, 'greet')
    # def test_check_outcome_for_greeting_if_first_greet_and_sign_off(self, mock_greet, mock_sign_off):
    #     Chat(id=100, username='test_user').save()
    #     Question.save_question(chat_id=100, question='test_question')
    #     State.get_last_state(chat_id=100)
    #     Greeting.get_last_greeting(chat_id=100)
    #
    #     self.biv.change_greeting_status(_id=100, last_greeting='first_greet', outcome='sign_off')
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'sign_off')
    #     mock_sign_off.assert_called_with(100)
    #     self.assertFalse(mock_greet.called, "Function greet called")
    #
    # @patch.object(BotInteraction, 'sign_off')
    # @patch.object(BotInteraction, 'greet')
    # def test_check_outcome_for_greeting_if_greet_and_sign_off(self, mock_greet, mock_sign_off):
    #     Chat(id=100, username='test_user').save()
    #     Question.save_question(chat_id=100, question='test_question')
    #     State.get_last_state(chat_id=100)
    #     Greeting.get_last_greeting(chat_id=100)
    #
    #     self.biv.change_greeting_status(_id=100, last_greeting='greet', outcome='sign_off')
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'sign_off')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     mock_sign_off.assert_called_with(100)
    #     self.assertFalse(mock_greet.called, "Function greet called")
    #
    # @patch.object(BotInteraction, 'sign_off')
    # @patch.object(BotInteraction, 'greet')
    # def test_check_outcome_for_greeting_if_sign_off_and_greet(self, mock_greet, mock_sign_off):
    #     Chat(id=100, username='test_user').save()
    #     Question.save_question(chat_id=100, question='test_question')
    #     State.get_last_state(chat_id=100)
    #     Greeting.get_last_greeting(chat_id=100)
    #
    #     self.biv.change_greeting_status(_id=100, last_greeting='sign_off', outcome='greet')
    #     self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'greet')
    #     self.assertEqual(State.get_last_state(chat_id=100), 'question')
    #     self.assertFalse(mock_sign_off.called, "Function sign_off called")
    #     mock_greet.assert_called_with(100)
