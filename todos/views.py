from .models import Todo, TodoComment
from .forms import TodoForm, TodoChildrenForm, UserForm, TodoCommentForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render

def tree_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    horizons: list[Todo.Horizon] = [
            Todo.Horizon.PURPOSE,
            Todo.Horizon.VISIONS,
            Todo.Horizon.GOALS,
            Todo.Horizon.FOCUS,
            Todo.Horizon.PROJECTS,
            Todo.Horizon.ACTIONS
    ]
    hor:int = 0
    todos = Todo.objects.filter(owner=request.user, horizon=horizons[hor])
    while len(todos) == 0:
        hor += 1
        todos = Todo.objects.filter(owner=request.user, horizon=horizons[hor])
    return render(request, "todos/todo_tree.html", { "todos": todos })

def tree_view_partial(request, pk:int):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    todo:Todo = Todo.objects.get(pk=pk)
    if not todo.owner == request.user:
        raise Http404
    context = {
        "todos": todo.children.all()
    }
    return render(request, "todos/todo_tree_partial.html", context)

def goto_horizon(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return HttpResponseRedirect(reverse('todos:horizon-view-list'))

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

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('todos:profile-detail')
    def get_object(self, *args, **kwargs):
        obj = self.request.user
        if not obj == self.request.user:
            raise Http404
        return obj

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

class TodoView(LoginRequiredMixin, DetailView):
    model = Todo

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

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    def get_success_url(self):
        return reverse('todos:horizon-detail-list', kwargs={"pk": self.object.horizon})
    def get_object(self, qs=None):
        obj = super(TodoDeleteView, self).get_object(qs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

class TodoUpdateChildren(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoChildrenForm
    template_name_suffix = "_children_form"
    def get_success_url(self):
        return reverse('todos:todo-view', kwargs={"pk": self.object.pk})
    def get_object(self, *args, **kwargs):
        obj = super(TodoUpdateChildren, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(TodoUpdateChildren, self).get_form_kwargs()
        kwargs['horizon'] = self.object.horizon
        kwargs['request'] = self.request
        return kwargs

class TodoComments(LoginRequiredMixin, ListView):
    model = TodoComment
    paginate_by = 100
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.path
        todo_id = path.replace("/todos/", "").replace("/comments/", "")
        context["todo"] = Todo.objects.get(pk=todo_id)
        return context
    def get_queryset(self):
        path = self.request.path
        todo_id = path.replace("/todos/", "").replace("/comments/", "")
        todo = Todo.objects.get(pk=todo_id)
        return TodoComment.objects.filter(owner=self.request.user, todo=todo)

def create_comment(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        user = request.user
        todo = Todo.objects.get(pk=pk)
        if not todo.owner == user:
            raise Http404
        form = TodoCommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.todo = todo
            comment.owner = user
            comment.save()
        return HttpResponseRedirect(reverse('todos:todo-comments', kwargs={"pk": todo.pk}))
    return HttpResponseRedirect(reverse('todos:horizon-view-list'))

class TodoCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoComment
    def get_success_url(self):
        return reverse('todos:todo-comments', kwargs={"pk": self.object.todo.pk})
    def get_object(self, qs=None):
        obj = super(TodoCommentDeleteView, self).get_object(qs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

class TodoCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoComment
    form_class = TodoCommentForm
    def get_success_url(self):
        return reverse('todos:todo-comments', kwargs={"pk": self.object.todo.pk})
    def get_object(self, qs=None):
        obj = super(TodoCommentUpdateView, self).get_object(qs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj
