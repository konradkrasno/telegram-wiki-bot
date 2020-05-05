from django.db import models
from datetime import datetime

# Create your models here.


class WikiData(models.Model):
    article_id = models.IntegerField()
    title = models.CharField(max_length=255)
    text = models.TextField()


class Chat(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    username = models.CharField(max_length=255, null=False)

    @classmethod
    def check_if_chat_id_already_exists(cls, _id):
        try:
            return cls.objects.get(id=_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def add_user_data_to_db(cls, chat_id, username):
        if not cls.check_if_chat_id_already_exists(chat_id):
            cls(
                id=chat_id,
                username=username
            ).save()


class Question(models.Model):
    id = models.AutoField
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    question_time = models.TimeField(default=datetime.now())

    @classmethod
    def save_question(cls, chat_id, question):
        Question(
            chat=Chat.objects.get(id=chat_id),
            question_text=question,
        ).save()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    article_id = models.IntegerField()
    input_text = models.TextField()
    answer_text = models.TextField()
    answer_time = models.TimeField(default=datetime.now())

    @classmethod
    def save_answer(cls, chat_id, article_id, input_text, answer_text):
        cls(
            question=Question.objects.filter(chat=chat_id).latest('id'),
            chat=Chat.objects.get(id=chat_id),
            article_id=article_id,
            input_text=input_text,
            answer_text=answer_text
        ).save()


class AnswerTime(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    interval = models.DurationField()


class AnswerFeedback(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    if_right = models.BooleanField()

    @classmethod
    def save_answer_feedback(cls, chat_id, if_right):
        cls(
            question=Question.objects.filter(chat=chat_id).latest('id'),
            chat=Chat.objects.get(id=chat_id),
            if_right=if_right
        ).save()


class State(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)

    @classmethod
    def change_state(cls, chat_id, state):
        cls.objects.filter(chat=chat_id).update(state=state)

    @classmethod
    def get_last_state(cls, chat_id):
        try:
            return getattr(cls.objects.filter(chat=chat_id).latest('id'), 'state')
        except cls.DoesNotExist:
            cls(
                chat=Chat.objects.get(id=chat_id),
                state='question',
            ).save()
            return 'question'


class Greeting(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    greeting = models.CharField(max_length=255)

    @classmethod
    def change_greeting(cls, chat_id, greeting):
        cls.objects.filter(chat=chat_id).update(greeting=greeting)

    @classmethod
    def get_last_greeting(cls, chat_id):
        try:
            return getattr(cls.objects.filter(chat=chat_id).latest('id'), 'greeting')
        except cls.DoesNotExist:
            cls(
                chat=Chat.objects.get(id=chat_id),
                greeting='first_greet'
            ).save()
            return 'first_greet'
