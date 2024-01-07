# Django Todo

## Setup

### Dev Spaces

#### Run/Debug App
1. Open a Dev Space with url `https://github.com/jkeam/djangotodos.git`
2. Install extensions - cmd + shift + x -> Open the RECOMMENDED section and install all extensions
3. Run Setup - cmd + shift + p -> Tasks: Run Task -> devfile -> Setup project
4. Step above will print the DB Client URL to the terminal.  cmd + click the URL to open it in a new tab -> Open
5. In tab with DB Client, enter the following to login.  After logging in, switch back to your Dev Spaces tab.
    ```shell
    System: PostgreSQL
    Server: localhost
    Username: postgres
    Password: adminpassword
    Database: todos
    ```
6. Run Install - cmd + shift + p -> Tasks: Run Task -> devfile -> Install dependencies
7. Run Migrate - cmd + shift + p -> Tasks: Run Task -> devfile -> Migrate
8. Run Create user - cmd + shift + p -> Tasks: Run Task -> devfile -> Create user
9. Run app - cmd + shift + d -> Click play button near 'RUN AND DEBUG'.  When prompted to open a new tab, click Open In New Tab -> Click Open.  If you get an error page, wait a second and refresh your browser -- the app is probably not ready yet.
10. Log into app with 'admin' and 'password1'
11. Click stop button near top when done

#### Run/Debug Tests
1. Run tests - cmd + shift + d -> Click dropdown where play button is and select Run Tests -> Click play button

#### Database
If you didn't get the DB Client URL, no worries, you can open a terminal (control + shift + backtick) (backtick is the character to the left of the number 1) and then run the following:

```shell
echo "https://$(oc get $(oc get routes -o name | grep adminer) -o jsonpath={.spec.host})"
```


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
