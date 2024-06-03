from .models import Todo
from .forms import TodoForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class HorizonListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 10
    template_name_suffix = '_horizon_list'
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

def horizon_detail(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'GET':
        horizon = 'AC'
        todos = []
        if Todo.valid_horizon(pk):
            horizon = pk
            todos = Todo.objects.filter(owner=request.user, horizon=horizon)
        context = {
            "page_obj": todos,
            "horizon": horizon,
            "horizon_name": Todo.horizon_value_to_name(horizon),
        }
    return render(request, "todos/todo_horizon_detail.html", context)

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 10
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    def get_success_url(self):
        return reverse('todos:horizon-detail-list', kwargs={"pk": self.object.horizon})
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def get_initial(self):
        initial = super(TodoCreateView, self).get_initial()
        horizon = self.request.GET.get('horizon', 'AC')
        if horizon not in ["AC", "PR", "FO", "GO", "VI", "PU"]:
            horizon = "AC"
        initial.update({ 'horizon': horizon })
        return initial

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    def get_success_url(self):
        return reverse('todos:horizon-detail-list', kwargs={"pk": self.object.horizon})
    def get_object(self, *args, **kwargs):
        obj = super(TodoUpdateView, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todos:todo-view-list')

def todo_toggle(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        todo = Todo.objects.get(pk=pk)
        if not todo.owner == request.user:
            raise Http404
        todo.completed = not todo.completed
        todo.save()
        return HttpResponseRedirect(reverse('todos:horizon-detail-list', kwargs={"pk": todo.horizon}))
    return HttpResponseRedirect(reverse('todos:horizon-view-list'))
