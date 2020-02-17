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


class Question(models.Model):
    id = models.AutoField
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    question_time = models.TimeField(default=datetime.now())


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    article_id = models.IntegerField()
    input_text = models.TextField()
    answer_text = models.TextField()
    answer_time = models.TimeField(default=datetime.now())


class AnswerTime(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    interval = models.DurationField()


class CheckAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    if_right = models.BooleanField()
