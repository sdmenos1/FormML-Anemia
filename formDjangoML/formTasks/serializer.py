from rest_framework import serializers
from .models import TaskForms
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskForms
        fields = '__all__'
