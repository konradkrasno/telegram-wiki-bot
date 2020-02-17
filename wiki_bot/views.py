import time
from django.http import JsonResponse
from django.views import View

import json
import os

import requests

from .models import Chat, Question, Answer, AnswerTime, CheckAnswer

from . import search
from . import custom_message
from deeppavlov import build_model, configs

model_qa_ml = build_model(configs.squad.squad_bert_multilingual_freezed_emb, download=False)

TELEGRAM_URL = "https://api.telegram.org/bot"
WIKI_BOT_TOKEN = os.getenv("WIKI_BOT_TOKEN", "error_token")


class WikiBotView(View):
    def post(self, request):
        chat = Chat()

        data = json.loads(request.body)
        message = data["message"]
        receive_chat_id = message["chat"]["id"]
        receive_chat_username = message["chat"]["first_name"]

        if not chat.check_if_chat_id_already_exists(receive_chat_id):
            Chat(
                id=receive_chat_id,
                username=receive_chat_username
            ).save()

        try:
            receive_text = message["text"].strip().lower()
        except Exception as e:
            print(e)
            return JsonResponse({"ok": "POST request processed"})

        if receive_text == '/start':
            self.send_message("Witaj {}. Jestem WikiBot, zapytaj mnie o jakąś informację z Wikipedii,"
                              " a dam Ci odpowiedź!"
                              .format(receive_chat_username), receive_chat_id)

        elif receive_text.startswith('/'):
            pass

        else:
            outcome = search.check_outcome(receive_text)

            if outcome is not None:
                self.send_message(custom_message.prepare_custom_message('output_answers',outcome), receive_chat_id)

                CheckAnswer(
                    question=Question.objects.latest('id'),
                    chat=Chat.objects.get(id=receive_chat_id),
                    if_right=outcome
                ).save()

                time.sleep(0.5)
                self.send_message(custom_message.prepare_custom_message('next_questions',outcome), receive_chat_id)

            else:
                Question(
                    chat=Chat.objects.get(id=receive_chat_id),
                    question_text=receive_text,
                ).save()

                context, article_id = search.search_text(receive_text)

                if context:
                    answer_text = model_qa_ml([context], [receive_text])[0][0]
                    print("Answer: ", answer_text)

                    Answer(
                        question=Question.objects.latest('id'),
                        chat=Chat.objects.get(id=receive_chat_id),
                        article_id=article_id,
                        input_text=context,
                        answer_text=answer_text
                    ).save()

                    if len(answer_text) == 0:
                        self.send_message("Nie rozumiem Cię :(", receive_chat_id)
                        time.sleep(0.5)
                        self.send_message("Zadaj pytanie w innny sposób ;)", receive_chat_id)

                    else:
                        self.send_message(answer_text, receive_chat_id)
                        time.sleep(0.5)
                        self.send_message("Czy odpowiedziałem wyczerpująco na Twoje pytanie?", receive_chat_id)

                else:
                    self.send_message("Nie rozumiem Cię :(", receive_chat_id)

                    CheckAnswer(
                        question=Question.objects.latest('id'),
                        chat=Chat.objects.get(id=receive_chat_id),
                        if_right=False
                    ).save()

                    time.sleep(0.5)
                    self.send_message("Zadaj pytanie w innny sposób ;)", receive_chat_id)

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        return requests.post(f"{TELEGRAM_URL}{WIKI_BOT_TOKEN}/sendMessage", data=data)
