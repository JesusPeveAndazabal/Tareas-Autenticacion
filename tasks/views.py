from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

# Create your views here.
""" Request : parametro que django ofrece para obtener informacion del cliente que visito la pagina """

def home(request):
    """ Metodo render : espera el parametro request como 1 parametro y el segundo el que se va a enviar """
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form' : UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
          try:
            #Metodo : create_user - espera 2 cosas - usuario y contraseña
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            
            #Ejecutamos el login - se pasas 2 paremetros (request - 'usuario a guardar')
            login(request,user)

            #Redireccionado a la vista de tasks - Metodo redirect
            return redirect('tasks')     
          except IntegrityError:                                    
            return render(request, 'signup.html',{
                'form' : UserCreationForm,
                "error" : 'El usuario ya existe'
            })
        return render(request, 'signup.html',{
            'form' : UserCreationForm,
             "error" : 'Las contraseñas no coinciden'
        })


def tasks(request):
   #Devuelve todas las tareas en la bd
   tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
   return render(request, 'tasks.html', {'tasks' : tasks})


def create_task(request):
    if request.method == 'GET':
        return render (request , 'create_task.html' , {
            'form' : TaskForm
        })
    else:
        try:
          form = TaskForm(request.POST)
          new_task = form.save(commit=False)
          new_task.user = request.user
          new_task.save()
          return redirect('tasks')
        except ValueError:
          return render (request, 'create_task.html', {
             'form' : TaskForm,
             'error' : 'Porfavor provee datos validos'
          })

def task_detail(request, task_id):
   task = get_object_or_404(Task, pk=task_id)   
   return render(request, 'task_detail.html',{
      'task' : task
   })

def signout(request):
   logout(request)
   return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form' : AuthenticationForm
        })
    else:
      user = authenticate(
         request, username=request.POST['username'], password=request.POST['password'])
      if user is None:
         return render(request, 'signin.html',{
            'form' : AuthenticationForm,
            'error' : 'Nombre de usuario y contraseña incorrectas'
         })
      else:
        login(request,user)
        return redirect('tasks')
      