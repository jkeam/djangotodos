from django.test import TestCase
from django.urls import reverse
from .models import Todo
from django.contrib.auth import get_user_model
from django.test import Client

def create_user(user_dict:dict):
    """ Create user """
    UserModel = get_user_model()
    username = user_dict.get('username')
    if not UserModel.objects.filter(username=username).exists():
        user = UserModel.objects.create_user(username, password=user_dict.get('password'))
        user.email = user_dict.get('email')
        user.first_name = user_dict.get('first_name')
        user.last_name = user_dict.get('last_name')
        user.is_superuser = False
        user.is_staff = False
        user.save()

def create_test_user():
    """ Create Foo user """
    users = [{
        'username': 'foo',
        'password': 'bar',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@example.com',
        }]
    for user in users:
        create_user(user)

def create_second_test_user():
    users = [{
        'username': 'foo2',
        'password': 'bar2',
        'first_name': 'Foo2',
        'last_name': 'Bar2',
        'email': 'foo2@example.com',
        }]
    for user in users:
        create_user(user)

def get_user():
    """ Get user """
    UserModel = get_user_model()
    return UserModel.objects.filter(username='foo').first()

def create_todo_for_test_user(name):
    """ Creates a todo """
    UserModel = get_user_model()
    user = UserModel.objects.filter(username='foo').first()
    Todo.objects.all().delete()
    return Todo.objects.create(name=name, owner=user)

class TodoIndexViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-index')

    def test_index(self):
        response = self.client.get(reverse("todos:horizon-view-list"))
        self.assertEqual(response.status_code, 200)

class TodoDetailViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-detail')

    def test_detail_view(self):
        """
        The detail view
        """
        url = reverse("todos:todo-update", args=(self.todo.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        """
        Test update
        """
        self.assertEqual(Todo.objects.all().first().description, '')
        url = reverse("todos:todo-update", args=(self.todo.id,))
        redirect_url = reverse("todos:todo-view", kwargs={"pk": self.todo.id})
        self.assertEqual(self.todo.description, '')
        response = self.client.post(url, data={
            'horizon': self.todo.horizon,
            'name': self.todo.name,
            'progress': self.todo.progress,
            'description': 'some desc',
        })
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.description, 'some desc')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TodoDeleteViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-delete')

    def test_delete_view(self):
        """
        The delete view
        """
        url = reverse("todos:todo-delete", args=(self.todo.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """
        The delete
        """
        self.assertEqual(Todo.objects.all().count(), 1)
        url = reverse("todos:todo-delete", args=(self.todo.id,))
        redirect_url = reverse("todos:horizon-detail-list", kwargs={"pk": 'AC'})
        response = self.client.post(url)
        self.assertEqual(Todo.objects.all().count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TodoToggleViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-toggle')

    def test_toggle(self):
        """
        Toggle completion
        """
        self.assertEqual(Todo.objects.all().count(), 1)
        self.assertEqual(Todo.objects.all().first().completed, False)
        url = reverse("todos:todo-toggle-partial", args=(self.todo.id,))
        response = self.client.post(url)
        self.assertEqual(Todo.objects.all().first().completed, True)
        self.assertEqual(response.status_code, 200)

class TodoProgressViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-progress')

    def test_toggle(self):
        """
        Toggle completion
        """
        self.assertEqual(Todo.objects.all().count(), 1)
        self.assertEqual(Todo.objects.all().first().progress, 'BA')
        url = reverse("todos:todo-progress-partial", args=(self.todo.id, 'PL'))
        response = self.client.post(url)
        self.assertEqual(Todo.objects.all().first().progress, 'PL')
        self.assertEqual(response.status_code, 200)

class TodoOtherUserTodoViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.user2 = create_second_test_user()
        self.client.login(username='foo', password='bar')
        self.todo = create_todo_for_test_user('test-toggle')

    def test_other_view(self):
        """
        Toggle completion
        """
        url = reverse("todos:todo-update", args=(self.todo.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.login(username='foo2', password='bar2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
