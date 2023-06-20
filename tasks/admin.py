from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    #Especificar cuales son los campos para solo lectura y que quieres ver en la pantalla
    readonly_fields = ("created" ,) 


# Register your models here.
admin.site.register(Task, TaskAdmin)