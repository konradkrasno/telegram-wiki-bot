from django.test import TestCase

from ..views import BotInteractionView
from ..bot_interactions import BotInteraction
from ..models import Chat, Question, Answer, CheckAnswer, State

import json

with open('secure.json', 'r') as file:
    secure = json.load(file)


# Create your tests here.


class BotInteractionViewTests(TestCase):
    def setUp(self):
        self.bi = BotInteraction()
        self.biv = BotInteractionView()

    def test_post(self):
        pass

    def test_check_outcome_for_feedback_if_true(self):
        outcome = True
        Chat(id=secure["TEST_CHAT_ID"], username='test_user').save()
        Question.save_question(chat_id=secure["TEST_CHAT_ID"], question='test_question')
        State.get_last_state(chat_id=secure["TEST_CHAT_ID"])

        self.biv.check_outcome_for_feedback(_id=secure["TEST_CHAT_ID"], outcome=True)

        test_content = {
            'chat': secure["TEST_CHAT_ID"],
            'if_right': outcome,
        }

        self.assertDictEqual(CheckAnswer.objects.values('chat', 'if_right')[0], test_content)
        self.assertEqual(State.get_last_state(chat_id=secure["TEST_CHAT_ID"]), 'question')

    def test_check_outcome_for_greeting(self, last_greeting, outcome):
        pass
