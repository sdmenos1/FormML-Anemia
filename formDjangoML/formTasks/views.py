from rest_framework import viewsets
from .models import TaskForms
from .serializer import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskForms.objects.all()
    serializer_class = TaskSerializer
