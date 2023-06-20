from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100) 
    description = models.TextField(blank=True)#Si no se pasa nada el campo queda en vacio
    created = models.DateTimeField(auto_now_add=True)#sino se le pasa lo añade
    datecompleted = models.DateTimeField(null =True)
    important = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '/' + self.user.username
