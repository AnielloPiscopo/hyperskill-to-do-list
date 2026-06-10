from django.views.generic import ListView, DetailView
from ..models import Todo

__all__ = ['TodoListView', 'TodoDetailView']

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'

class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todo/todo_detail.html'
    context_object_name = 'todo'