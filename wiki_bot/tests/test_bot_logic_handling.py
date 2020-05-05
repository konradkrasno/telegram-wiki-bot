from django.test import TestCase, RequestFactory

from unittest.mock import patch

from wiki_bot.bot_logic import BotLogicHandling

# Create your tests here.


class BotLogicHandlingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # TODO finish all tests
    def test_init(self):
        pass

    def test_start(self):
        pass

    def test_save_positive_feedback_and_change_state_to_question(self):
        pass

    def test_save_negative_feedback_and_change_state_to_question(self):
        pass

    def test_change_sign_off_status_to_greet_and_change_state_status_to_question(self):
        pass

    def test_change_sign_off_status_to_greet(self):
        pass

    def test_change_greet_status_to_sign_off_and_change_state_status_to_question(self):
        pass

    def test_change_greet_status_to_sign_off(self):
        pass

    def test_change_first_greet_status_to_greet(self):
        pass

    def test_check_answer_valid_and_change_state_status_to_answer_feedback(self):
        pass

    def test_remind_about_answer_feedback(self):
        pass
