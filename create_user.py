""" Creates users """
from django.contrib.auth import get_user_model

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

users = [{
    'username': 'foo',
    'password': 'bar',
    'first_name': 'Foo',
    'last_name': 'Bar',
    'email': 'foo@example.com',
    }]

for user in users:
    create_user(user)
