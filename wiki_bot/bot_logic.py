from telegram_wiki_bot.wiki_bot.views import BotInteractionView

bot_status = {
    '/start': BotInteractionView.start,
    '/': BotInteractionView.slash,
    'question': BotInteractionView.question,
    'check_answer': BotInteractionView.check_answer
}

# question_status = {
#     'greet':
# }