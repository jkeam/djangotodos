from .models import Todo
from .forms import TodoForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 10
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    success_url = '/todos/'
    form_class = TodoForm
    def form_valid(self, form):
        f = form.instance
        f.owner = self.request.user
        return super().form_valid(form)

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    def form_valid(self, form):
        f = form.instance
        f.owner = self.request.user
        return super().form_valid(form)

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todos:todo-view-list')

def todo_toggle(request, pk):
    if request.method == 'POST':
        todo = Todo.objects.get(pk=pk)
        todo.completed = not todo.completed
        todo.save()
    return HttpResponseRedirect("/todos/")
