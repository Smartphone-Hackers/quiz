from rest_framework import serializers
from quiz_app import models

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswerModel
        fields = ('correct_answer', 'options', 'clicked', 'click_data')
    
    def update(self, instance, validated_data):
        instance.correct_answer = validated_data.get('correct_answer')
        instance.options = validated_data.get('options')
        instance.clicked = validated_data.get('clicked')
        instance.click_data = validated_data.get('click_data')
        instance.save(update_fields=['correct_answer', 'options', 'clicked',
                                     'click_data'])
        return instance