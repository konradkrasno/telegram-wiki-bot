from random import choice

custom_messages = {
    'next_questions':
        {
        False:["Zadaj pytanie w innny sposób ;)", "Zadaj pytanie inaczej", "Spróbuj zadać pytanie używając innych słów"],
         True:["Zadaj mi jeszcze jakieś pytanie ;)", "Poproszę o następne pytania!"]
        },
    'output_answers':
        {
        False:['Szkoda ;(', 'Przepraszam, że Ci nie mogłem pomóc'],
        True:['Cieszę się!', 'Super!', 'Uff.. Udało się :)']
        },
    'greet_answers':
        {
        'greet': ['Siema, co tam?', 'Siema siema', 'Witaj, w czym mogę Ci pomóc?']
        },
    'sign_off_answers':
        {
        'sign_off': ['Dobranoc', 'Elo Ziom', 'Do zobaczenia ponownie', 'Siema siema']
        },
    'remind_about_check_answer':
        {
        'check_answer': ['Nie powiedziałeś czy dobrze odpowiedzałem', 'Daj znać czy dobrze odpowiedziałem']
        }
}

def prepare_custom_message(type,output):
    return choice(custom_messages[type][output])
