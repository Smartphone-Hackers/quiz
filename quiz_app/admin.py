from django.contrib import admin
from quiz_app import models

# Register your models here.
class ShowQuestionAnswerModel(admin.ModelAdmin):
    list_display =('id', 'username', 'category', 'difficulty', 'question', 'correct_answer', 
                'options', 'clicked', 'click_data',)

class ShowTimeCalculate(admin.ModelAdmin):
    list_display =('id', 'username', 'start_time', 'end_time')

class ShowStudentQuizResult(admin.ModelAdmin):
    list_display = ('id', 'username', 'topic', 'total_time', 'total_questions', 
                    'right_answer', 'wrong_answer',)

admin.site.register(models.QuestionAnswerModel, ShowQuestionAnswerModel)
admin.site.register(models.TimeCalulate, ShowTimeCalculate)
admin.site.register(models.StudentQuizResult, ShowStudentQuizResult)