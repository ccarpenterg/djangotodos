# Create your views here.

from items.models import TodoList, Todo
from django.http import HttpResponse, QueryDict, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import loader, Context
import json, Cookie

from datetime import datetime

def get(request, item_id):
    id = request.COOKIES['todos']
    todos = []
    for todo in Todo.objects.filter(todolist=id):
	todos.append(todo.toDict())
    todos = json.dumps(todos)
    response = HttpResponse()
    #response['Content-Type'] = 'application/json'
    response.write(todos)
    return response

def post(request, item_id):
    id = request.COOKIES['todos']
    todolist = TodoList.objects.get(id=int(id))
    todo = json.loads(request.raw_post_data)
    todo = Todo(todolist = todolist,
		order    = int(todo['order']),
		content  = todo['content'],
		done     = todo['done'])
    todo.save()
    todo = json.dumps(todo.toDict())
    response = HttpResponse()
    response.write(todo)
    return response

def put(request, item_id):
    id = request.COOKIES['todos']
    todolist = TodoList.objects.get(id=id)
    todo = Todo.objects.get(id=item_id)
    if todo.todolist == todolist:
	tmp = json.loads(request.raw_post_data)
	todo.content = tmp['content']
	todo.done    = tmp['done']
	todo.save()
	todo = json.dumps(todo.toDict())
	response = HttpResponse()
	response.write(todo)
	return response
    else:
	return HttpResponseForbidden()

def delete(request, item_id):
    id = request.COOKIES['todos']
    todolist = TodoList.objects.get(id=id)
    todo = Todo.objects.get(id=item_id)
    if todo.todolist == todolist:
	todo.delete()
	return HttpResponse()
    else:
	return HttpResponseForbidden()

methods = {
	'GET': get,
	'POST': post,
	'PUT': put,
	'DELETE': delete
	}

def restful(request, item_id):
    return methods[request.method](request, item_id)

def index(request):
    response = HttpResponse()
    if 'todos' not in request.COOKIES:
	todolist = TodoList()
	todolist.save()
	cookie = Cookie.SimpleCookie()
	cookie['todos'] = todolist.id
	cookie['todos']['expires'] = datetime(2014, 1, 1).strftime('%a, %d %b %Y %H:%M:%S')
	cookie['todos']['path'] ='/'
	response['Set-Cookie'] = cookie['todos'].OutputString()
    template = loader.get_template('index.html')
    context = Context({'x': 'x'})
    response.write(template.render(context))
    return response
    #return render_to_response('index.html')
