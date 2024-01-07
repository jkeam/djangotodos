# Django Todo

## Setup

### Dev Spaces

#### Run/Debug App
1. Open a Dev Space with url `https://github.com/jkeam/djangotodos.git`
2. Run Setup - cmd + shift + p -> Tasks: Run Task -> devfile -> Setup project
3. Run Install - cmd + shift + p -> Tasks: Run Task -> devfile -> Install dependencies
4. Run Migrate - cmd + shift + p -> Tasks: Run Task -> devfile -> Migrate
5. Run Create user - cmd + shift + p -> Tasks: Run Task -> devfile -> Create user
6. Run app - cmd + shift + d -> Click play button near 'RUN AND DEBUG'.  When prompted to open a new tab, click Open In New Tab -> Click Open
7. Log into app with 'admin' and 'password'
8. Click stop button near top when done

#### Run/Debug Tests
1. Run tests - cmd + shift + d -> Click dropdown where play button is and select Run Tests -> Click play button


### Local

#### Prerequisite
1. Python 3.12

#### Environment
1. Clone this repo
2. `python3.12 -m venv venv && source ./venv/bin/activate`
3. `pip install -r ./requirements.txt`
4. `cp ./.env.template ./.env`
5. Update values in `./.env`

#### Application
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
