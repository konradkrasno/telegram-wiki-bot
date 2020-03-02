from django.test import TestCase
from unittest.mock import Mock

from ..bot_interactions import BotInteraction
from ..bot_settings import TELEGRAM_URL, WIKI_BOT_TOKEN


requests = Mock()


class SendMessageTest(TestCase):
    @classmethod
    def send_message(cls, message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        return requests.post("mocked_url/sendMessage", data=data)

    @classmethod
    def send_message_request(cls):
        data = {
            "chat_id": 100,
            "text": "test message",
            "parse_mode": "Markdown",
        }

        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.post("mocked_url/sendMessage", data=data)
        # response_mock.post("mocked_url/sendMessage", data=data).return_value = '<Response [200]>'
        # response_mock.post.return_value = "test message"
        # response_mock.json.return_value = "test message"

        # response_mock.json.return_value = {
        #     "ok": True,
        #     "result":
        #         {"message_id": 1234,
        #          "from": {"id": 996463999,
        #                   "is_bot": True,
        #                   "first_name": "WikiBot",
        #                   "username": "kondzio_bot"},
        #          "chat": {"id": 100,
        #                   "first_name": "test_first_name",
        #                   "last_name": "test_last_name",
        #                   "type": "private"},
        #          "date": 1582900572,
        #          "text": "test message"
        #          }
        # }
        return response_mock

    def test_send_message(self):
        data = {
            "chat_id": 100,
            "text": "test message",
            "parse_mode": "Markdown",
        }

        requests.post("mocked_url/sendMessage", data=data).side_effect = self.send_message_request

        msg = self.send_message(message="test_message", chat_id=100).status_code
        self.assertEqual(msg, 200)
