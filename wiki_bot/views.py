from django.views import View
from django.http import JsonResponse

from wiki_bot.bot_logic import BotLogicHandling


class BotInteractionView(View):

    def post(self, request):
        blh = BotLogicHandling(request)
        print(blh)

        if blh.received_text.startswith('/'):
            try:
                status = blh.bot_status[blh.received_text]
            except KeyError:
                print("Wrong command {}".format(blh.received_text))
            else:
                status()
        else:
            try:
                status = blh.bot_status['after_start'][blh.last_state][blh.last_greeting][blh.outcome]
            except KeyError as e:
                print("KeyError: {}".format(e))
            else:
                status()

        return JsonResponse({"ok": "POST request processed"})
