from django.views import View
from django.http import JsonResponse

from .bot_interactions import BotInteraction
from .models import State, Greeting
from .search import check_outcome


class BotInteractionView(BotInteraction, View):
    def post(self, request):
        receive_message = self.request_message(request)
        receive_chat_id, receive_chat_username = self.get_user_data_from_message(receive_message)
        receive_text = self.get_text_from_message(receive_message)
        print(receive_text)

        state = State()
        greeting = Greeting()
        last_state = state.get_last_state(receive_chat_id)
        last_greeting = greeting.get_last_greeting(receive_chat_id)
        print("last state (chat_id: {0}): {1}: ".format(receive_chat_id, last_state))
        print("last greeting (chat_id: {0}): {1}: ".format(receive_chat_id, last_greeting))

        if receive_text == '/start':
            self.start_chat(receive_chat_id, receive_chat_username)
            greeting.change_greeting(receive_chat_id, greeting='first_greet')

        elif receive_text.startswith('/'):
            pass

        elif last_state == 'question':
            outcome = check_outcome(receive_text)
            if outcome == 'greet':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            elif outcome == 'sign_off':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            elif outcome == 'greet-sign_off':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            else:
                answer = self.user_question(receive_chat_id, receive_text)

                if answer:
                    state.change_state(receive_chat_id, state='check_answer')

        elif last_state == 'check_answer':
            outcome = check_outcome(receive_text)
            if outcome is True or outcome is False:
                self.check_outcome_for_feedback(receive_chat_id, outcome)
            elif outcome == 'greet':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            elif outcome == 'sign_off':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            elif outcome == 'greet-sign_off':
                self.check_outcome_for_greeting(receive_chat_id, last_greeting, outcome)
            else:
                self.remind_about_check_answer(receive_chat_id)

        return JsonResponse({"ok": "POST request processed"})

    def check_outcome_for_feedback(self, _id, outcome):
        state = State()

        self.check_answer(outcome, _id)
        state.change_state(_id, state='question')

    def check_outcome_for_greeting(self, _id, last_greeting, outcome):
        state = State()
        greeting = Greeting()

        if last_greeting == 'first_greet' and outcome in ['greet', 'greet-sign_off']:
            greeting.change_greeting(_id, greeting='greet')
        elif last_greeting == 'first_greet' and outcome in ['sign_off']:
            self.sign_off(_id)
            greeting.change_greeting(_id, greeting='sign_off')
        elif last_greeting == 'greet' and outcome in ['sign_off', 'greet-sign_off']:
            self.sign_off(_id)
            greeting.change_greeting(_id, greeting='sign_off')
            state.change_state(_id, state='question')
        elif last_greeting == 'sign_off' and outcome in ['greet', 'greet-sign_off']:
            self.greet(_id)
            greeting.change_greeting(_id, greeting='greet')
            state.change_state(_id, state='question')
