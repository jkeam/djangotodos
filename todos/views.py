from .models import Todo
from .forms import TodoForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class HorizonListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 100
    template_name_suffix = '_horizon_list'
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class HorizonDetailListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 100
    template_name_suffix = '_horizon_detail'
    def get_queryset(self):
        horizon = self.request.path.replace('/todos/horizons/', '')
        if not Todo.valid_horizon(horizon):
            horizon = 'AC'
        return Todo.objects.filter(owner=self.request.user, horizon=horizon)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horizon = self.request.path.replace('/todos/horizons/', '')
        if not Todo.valid_horizon(horizon):
            horizon = 'AC'
        context["horizon"] = horizon
        context["horizon_name"] = Todo.horizon_value_to_name(horizon)
        return context

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 100
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
