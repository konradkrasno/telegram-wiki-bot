fake_text = [
    "/start",
    "/something",
    "This is answer text",
    "witam",
    "siema",
    "do widzenia",
    "tak",
    "nie"
]

states = [
    'question',
    'answer_feedback'
]

greetings = [
    "first_greet",
    "greet",
    "sign_off"
]

method_matching = {
    'question': {
        'first_greet': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'change_first_greet_status_to_greet',
            'siema': 'change_first_greet_status_to_greet',
            'do widzenia': 'change_greet_status_to_sign_off',
            'tak': 'do_nothing',
            'nie': 'do_nothing',
            'This is answer text': 'check_answer_valid_and_change_state_status_to_answer_feedback'
        },
        'greet': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'do_nothing',
            'siema': 'change_greet_status_to_sign_off',
            'do widzenia': 'change_greet_status_to_sign_off',
            'tak': 'do_nothing',
            'nie': 'do_nothing',
            'This is answer text': 'check_answer_valid_and_change_state_status_to_answer_feedback'
        },
        'sign_off': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'change_sign_off_status_to_greet',
            'siema': 'change_sign_off_status_to_greet',
            'do widzenia': 'do_nothing',
            'tak': 'do_nothing',
            'nie': 'do_nothing',
            'This is answer text': 'check_answer_valid_and_change_state_status_to_answer_feedback'
        }
    },
    'answer_feedback': {
        'first_greet': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'change_first_greet_status_to_greet',
            'siema': 'change_greet_status_to_sign_off',
            'do widzenia': 'change_greet_status_to_sign_off',
            'tak': 'save_positive_feedback_and_change_state_to_question',
            'nie': 'save_negative_feedback_and_change_state_to_question',
            'This is answer text': 'remind_about_answer_feedback'
        },
        'greet': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'do_nothing',
            'siema': 'change_greet_status_to_sign_off_and_change_state_status_to_question',
            'do widzenia': 'change_greet_status_to_sign_off_and_change_state_status_to_question',
            'tak': 'save_positive_feedback_and_change_state_to_question',
            'nie': 'save_negative_feedback_and_change_state_to_question',
            'This is answer text': 'remind_about_answer_feedback'
        },
        'sign_off': {
            '/start': 'start',
            '/something': 'external_command',
            'witam': 'change_sign_off_status_to_greet_and_change_state_status_to_question',
            'siema': 'change_sign_off_status_to_greet_and_change_state_status_to_question',
            'do widzenia': 'do_nothing',
            'tak': 'save_positive_feedback_and_change_state_to_question',
            'nie': 'save_negative_feedback_and_change_state_to_question',
            'This is answer text': 'remind_about_answer_feedback'
        }
    }
}
