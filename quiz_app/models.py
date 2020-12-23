from django.db import models

# Create your models here.
class QuestionAnswerModel(models.Model):
    username = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    question = models.TextField()
    correct_answer = models.CharField(max_length=100)
    options = models.CharField(max_length=255)
    clicked = models.IntegerField(default=0)
    click_data = models.CharField(max_length=100, null=True)

class TimeCalulate(models.Model):
    username = models.ForeignKey(QuestionAnswerModel, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class StudentQuizResult(models.Model):
    username = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    total_time = models.CharField(max_length=100)
    total_questions = models.CharField(max_length=100)
    right_answer = models.CharField(max_length=100)
    wrong_answer = models.CharField(max_length=100)