from django.test import TestCase, RequestFactory

from unittest.mock import patch

from wiki_bot.views import BotInteractionView
from wiki_bot.bot_logic import BotInteraction, BotLogicHandling
from wiki_bot.models import State, Greeting

from wiki_bot.tests.method_matching import method_matching


# Create your tests here.


class BotInteractionViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.fake_text = [
            "/start",
            "/something",
            "This is answer text",
            "witam",
            "siema",
            "do widzenia",
            "tak",
            "nie"
        ]

        self.states = [
            'question',
            'answer_feedback'
        ]

        self.greetings = [
            "first_greet",
            "greet",
            "sign_off"
        ]

    @staticmethod
    def fake_data(text):
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
                                 'text': text
                                 }
                     }
        return fake_data

    def test_post(self):

        for state in self.states:
            for greeting in self.greetings:
                for text in self.fake_text:
                    try:
                        method = method_matching[state][greeting][text]
                    except KeyError:
                        with patch('builtins.print') as mock_print:
                            request = self.factory.post('/wiki_bot', self.fake_data(text),
                                                        content_type='application/json')
                            biv = BotInteractionView()
                            biv.post(request)

                            mock_print.assert_called_with('KeyError: {!r}'.
                                                          format(BotInteraction.check_outcome(text)))
                    else:
                        with self.subTest("{}, {}, {} -> {}".format(state, greeting, text, method)):
                            with patch.object(State, 'get_last_state', return_value=state) as mock_state:
                                with patch.object(Greeting, 'get_last_greeting', return_value=greeting) as mock_greeting:
                                    with patch.object(BotLogicHandling, method) as mock_method:
                                        request = self.factory.post('/wiki_bot', self.fake_data(text),
                                                                    content_type='application/json')
                                        biv = BotInteractionView()
                                        biv.post(request)
                                        mock_method.assert_called_with()
