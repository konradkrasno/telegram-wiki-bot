from django.test import TestCase

from wiki_bot.models import Chat, Question, Answer, CheckAnswer, State, Greeting

# Create your tests here.


class ChatModelTests(TestCase):
    def test_check_if_chat_id_already_exists_if_do_not_exists(self):
        self.assertIsNone(Chat.check_if_chat_id_already_exists(_id=1))

    def test_check_if_chat_id_already_exists_if_exists(self):
        Chat(id=100, username='test_user').save()
        self.assertEqual(getattr(Chat.check_if_chat_id_already_exists(_id=100), 'id'), 100)

    def test_add_user_data_to_db(self):
        Chat.add_user_data_to_db(chat_id=100, username='test_user')
        test_content = {
            'id': 100,
            'username': 'test_user'
        }
        self.assertDictEqual(Chat.objects.values('id', 'username')[0], test_content)


class QuestionModelTests(TestCase):
    def test_save_question(self):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_text')
        test_content = {
            'chat': 100,
            'question_text': 'test_text'
        }
        self.assertDictEqual(Question.objects.values('chat', 'question_text')[0], test_content)


class AnswerModelTests(TestCase):
    def test_save_answer(self):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question')
        Answer.save_answer(chat_id=100, article_id=1, input_text='test_text', answer_text='test_answer')
        test_content = {
            'chat': 100,
            'article_id': 1,
            'input_text': 'test_text',
            'answer_text': 'test_answer'
        }
        self.assertDictEqual(Answer.objects.values('chat', 'article_id', 'input_text', 'answer_text')[0],
                             test_content)


class CheckAnswerModelTests(TestCase):
    def test_save_check_answer(self):
        Chat(id=100, username='test_user').save()
        Question.save_question(chat_id=100, question='test_question_1')
        Question.save_question(chat_id=100, question='test_question_2')

        CheckAnswer.save_check_answer(chat_id=100, if_right=False)
        test_content = {
            'question': 2,
            'chat': 100,
            'if_right': False,
        }
        self.assertDictEqual(CheckAnswer.objects.values('question', 'chat', 'if_right')[0],
                             test_content)


class StateModelTests(TestCase):
    def test_change_state(self):
        Chat(id=100, username='test_user').save()
        State(chat=Chat.objects.get(id=100), state='test_state').save()
        State.change_state(chat_id=100, state='question')
        test_content = {
            'chat': 100,
            'state': 'question'
        }
        self.assertDictEqual(State.objects.values('chat', 'state')[0], test_content)

    def test_get_last_state_first_time(self):
        Chat(id=100, username='test_user').save()
        self.assertEqual(State.get_last_state(chat_id=100), 'question')

    def test_get_last_state_after_update(self):
        Chat(id=100, username='test_user').save()
        State.get_last_state(chat_id=100)
        State(chat=Chat.objects.get(id=100), state='test_state').save()
        self.assertEqual(State.get_last_state(chat_id=100), 'test_state')


class GreetingModelTests(TestCase):
    def test_change_greeting(self):
        Chat(id=100, username='test_user').save()
        Greeting(chat=Chat.objects.get(id=100), greeting='test_greet').save()
        Greeting.change_greeting(chat_id=100, greeting='sign_off')
        test_content = {
            'chat': 100,
            'greeting': 'sign_off'
        }
        self.assertDictEqual(Greeting.objects.values('chat', 'greeting')[0], test_content)

    def test_get_last_greeting_first_time(self):
        Chat(id=100, username='test_user').save()
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'first_greet')

    def test_get_last_greeting_second_time(self):
        Chat(id=100, username='test_user').save()
        Greeting.get_last_greeting(chat_id=100)
        Greeting(chat=Chat.objects.get(id=100), greeting='greet').save()
        self.assertEqual(Greeting.get_last_greeting(chat_id=100), 'greet')
