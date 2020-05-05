from django.views import View
from django.http import JsonResponse

from wiki_bot.bot_logic import BotLogicHandling


class BotInteractionView(View):

    def post(self, request):
        blh = BotLogicHandling(request)
        print(blh)

        try:
            status = blh.outcome_options[blh.last_state][blh.last_greeting][blh.outcome]
        except KeyError as e:
            print('KeyError: {}'.format(e))
        else:
            status()

        return JsonResponse({"ok": "POST request processed"})
