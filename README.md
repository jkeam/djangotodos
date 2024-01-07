# Django Todo

## Setup

### Prerequisite
1. Python 3.12

### Environment
1. Clone this repo
2. `python3.12 -m venv venv && source ./venv/bin/activate`
3. `pip install -r ./requirements.txt`
4. `cp ./.env.template ./.env`
5. Update values in `./.env`

### Application
1. Migrate db
    ```shell
    python ./manage.py migrate
    ```

2. Create superuser
    ```shell
    DJANGO_SUPERUSER_PASSWORD=password1 python ./manage.py createsuperuser --username admin --email admin@example.com --noinput
    ```

3. Create regular users using /admin
    ```shell
    cat create_user.py | python ./manage.py shell
    ```
