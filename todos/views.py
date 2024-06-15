from .models import Todo, TodoComment
from .forms import TodoForm, UserForm, PasswordForm, TodoCommentForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse_lazy, reverse
from django.forms.utils import ErrorList
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.shortcuts import render
import csv

# Helper methods
def get_todo_tree(owner) -> list[Todo]:
    horizons: list[Todo.Horizon] = [
            Todo.Horizon.PURPOSE,
            Todo.Horizon.VISIONS,
            Todo.Horizon.GOALS,
            Todo.Horizon.FOCUS,
            Todo.Horizon.PROJECTS,
            Todo.Horizon.ACTIONS
    ]
    hor:int = 0
    todos = Todo.objects.filter(owner=owner, horizon=horizons[hor])
    while len(todos) == 0:
        hor += 1
        todos = Todo.objects.filter(owner=owner, horizon=horizons[hor])
    return todos

def update_relationship(form, existing, chosen, owner, remove_association, add_association) -> None:
    todo:Todo = form.instance
    # remove if not chosen
    for parent in existing:
        if parent not in chosen:
            remove_association(parent, todo)
            parent.save()
            todo.save()
    # add if not in chosen
    for parent in chosen:
        if parent not in existing:
            add_association(parent, todo)
            parent.save()
            todo.save()

# Views
def export_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="todos.csv"'},
        )
        writer = csv.writer(response)
        count:int = 0
        for todo in Todo.objects.filter(owner=request.user):
            todo.write_to_csv(writer, count == 0)
            count += 1
        return response
    return render(request, "todos/todo_export.html")

def tree_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    user = request.user
    todos = get_todo_tree(user)
    orphaned = Todo.objects.filter(owner=user, parents=None) \
        .exclude(horizon=Todo.Horizon.PURPOSE)
    return render(request, "todos/todo_tree.html", { "todos": todos, "orphaned":orphaned })

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
        horizon:str = self.kwargs['pk']
        if not Todo.valid_horizon(horizon):
            horizon = 'AC'
        return Todo.objects.filter(owner=self.request.user, horizon=horizon, completed=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horizon:str = self.kwargs['pk']
        if not Todo.valid_horizon(horizon):
            horizon = 'AC'
        context["horizon"] = horizon
        context["horizon_name"] = Todo.horizon_value_to_name(horizon)
        return context

class HorizonDetailListPartialView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 100
    template_name_suffix = '_horizon_detail_partial'
    def get_queryset(self):
        horizon:str = self.kwargs['pk']
        if not Todo.valid_horizon(horizon):
            horizon:str = 'AC'
        if self.request.GET.get('hidden') == 'true':
            return Todo.objects.filter(owner=self.request.user, horizon=horizon)
        else:
            return Todo.objects.filter(owner=self.request.user, horizon=horizon, completed=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hidden"] = self.request.GET.get('hidden') == 'true'
        return context

class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordForm
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('todos:profile-password')

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    success_message = "Successfully Updated Your Profile"
    success_url = reverse_lazy('todos:profile-detail')
    def get_object(self, *args, **kwargs):
        return self.request.user

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    def get_form_kwargs(self):
        kwargs = super(TodoCreateView, self).get_form_kwargs()
        horizon:Todo.Horizon = Todo.horizon_value_to_horizon(self.request.GET.get('horizon', 'AC'))
        todo:Todo = Todo(horizon=horizon)
        horizon_enum:Todo.Horizon = todo.horizon_above()
        below:Todo.Horizon = todo.horizon_below()
        kwargs['parents'] = Todo.objects.filter(
            owner=self.request.user,
            horizon=horizon_enum,
        )
        kwargs['children'] = Todo.objects.filter(
            owner=self.request.user,
            horizon=below,
        )
        if horizon_enum:
            kwargs['parent_label'] = horizon_enum.label
            kwargs['initial_parents'] = None
        else:
            kwargs['parent_label'] = None
            kwargs['initial_parents'] = None
        if below:
            kwargs['children_label'] = below.label
            kwargs['initial_children'] = None
        else:
            kwargs['children_label'] = None
            kwargs['initial_children'] = None
        return kwargs
    def get_success_url(self):
        return reverse('todos:horizon-detail-list', kwargs={"pk": self.object.horizon})
    def get_initial(self):
        initial = super(TodoCreateView, self).get_initial()
        horizon = self.request.GET.get('horizon', 'AC')
        if horizon not in ["AC", "PR", "FO", "GO", "VI", "PU"]:
            horizon = "AC"
        initial.update({ 'horizon': horizon })
        return initial
    def form_valid(self, form):
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = self.request.user
            todo.save()
            update_relationship(
                    form,
                    todo.parents.all(),
                    form.cleaned_data.get('parents', []),
                    self.request.user,
                    lambda parent, todo: parent.children.remove(todo),
                    lambda parent, todo: parent.children.add(todo),
            )
            update_relationship(
                    form,
                    todo.children.all(),
                    form.cleaned_data.get('children', []),
                    self.request.user,
                    lambda parent, todo: todo.children.remove(parent),
                    lambda parent, todo: todo.children.add(parent),
            )
        return super().form_valid(form)

class TodoView(LoginRequiredMixin, DetailView):
    model = Todo

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    def get_form_kwargs(self):
        kwargs = super(TodoUpdateView, self).get_form_kwargs()
        horizon_enum:Todo.Horizon = self.object.horizon_above()
        below:Todo.Horizon = self.object.horizon_below()
        kwargs['parents'] = Todo.objects.filter(
            owner=self.request.user,
            horizon=horizon_enum,
        )
        kwargs['children'] = Todo.objects.filter(
            owner=self.request.user,
            horizon=below,
        )
        if horizon_enum:
            kwargs['parent_label'] = horizon_enum.label
            kwargs['initial_parents'] = self.object.parents.all()
        else:
            kwargs['parent_label'] = None
            kwargs['initial_parents'] = None
        if below:
            kwargs['children_label'] = below.label
            kwargs['initial_children'] = self.object.children.all()
        else:
            kwargs['children_label'] = None
            kwargs['initial_children'] = None
        return kwargs
    def get_success_url(self):
        return reverse('todos:todo-view', kwargs={"pk": self.object.pk})
    def get_object(self, *args, **kwargs):
        obj = super(TodoUpdateView, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj
    def form_valid(self, form):
        todo = form.instance
        if not todo.owner == self.request.user:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["You do not own this"])
            return self.form_invalid(form)
        if form.is_valid():
            update_relationship(
                    form,
                    todo.parents.all(),
                    form.cleaned_data.get('parents', []),
                    self.request.user,
                    lambda parent, todo: parent.children.remove(todo),
                    lambda parent, todo: parent.children.add(todo),
            )
            update_relationship(
                    form,
                    todo.children.all(),
                    form.cleaned_data.get('children', []),
                    self.request.user,
                    lambda parent, todo: todo.children.remove(parent),
                    lambda parent, todo: todo.children.add(parent),
            )
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
        context = {
            "todo": todo,
            "hidden": request.POST.get('hidden', True)
        }
        return render(request, "todos/todo_horizon_detail_row_partial.html", context)
    return HttpResponseRedirect(reverse('todos:horizon-view-list'))

def todo_blocked(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        todo = Todo.objects.get(pk=pk)
        if not todo.owner == request.user:
            raise Http404
        todo.blocked = not todo.blocked
        todo.save()
        context = {
            "todo": todo,
            "hidden": request.POST.get('hidden', True)
        }
        return render(request, "todos/todo_horizon_detail_row_partial.html", context)
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

class TodoComments(LoginRequiredMixin, ListView):
    model = TodoComment
    paginate_by = 100
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = Todo.objects.get(pk=self.kwargs['pk'])
        if not self.request.user == todo.owner:
            todo = None
        context["todo"] = todo
        return context
    def get_queryset(self):
        todo = Todo.objects.get(pk=self.kwargs['pk'])
        if not self.request.user == todo.owner:
            return []
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
