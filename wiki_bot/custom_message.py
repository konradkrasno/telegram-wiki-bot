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
        }
}

def prepare_custom_message(type,output):
    return choice(custom_messages[type][output])