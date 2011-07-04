from django.db import models

# Create your models here.

class TodoList(models.Model):
    createdon = models.DateTimeField(auto_now_add=True)

class Todo(models.Model):
    todolist = models.ForeignKey(TodoList)
    order    = models.IntegerField()
    content  = models.CharField(max_length=256)
    done     = models.BooleanField()

    def toDict(self):
	todo = {
	    'id': self.id,
	    'order': self.order,
	    'content': self.content,
	    'done': self.done
	    }
	return todo
