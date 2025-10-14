from django.db import models  

class TaskForms(models.Model):
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    genero = models.CharField(max_length=10)
    peso = models.FloatField()
    talla = models.FloatField()
    distrito = models.CharField(max_length=100)
    cred = models.IntegerField()
    suplementacion = models.IntegerField()
    def __str__(self):
        return self.name

        
    