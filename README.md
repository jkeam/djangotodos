# Django Todo

Simple Django Todo app.  Below are the setup instructions for various environments.

## Dev Spaces

This is how to run the app within a Dev Space workspace.

### GitHub Access
1. Generate a PAT for your GitHub Repo.  Make sure to give access to commit and clone the repo
2. Navigate to `https://<openshift_dev_spaces_fqdn>/dashboard/#/user-preferences?tab=personal-access-tokens` and add the PAT

### Run/Debug App
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

### Run/Debug Tests
1. Run tests - cmd + shift + d -> Click dropdown where play button is and select Run Tests -> Click play button

### Database
If you didn't get the DB Client URL, no worries, you can open a terminal (control + shift + backtick) (backtick is the character to the left of the number 1) and then run the following:

```shell
echo "https://$(oc get $(oc get routes -o name | grep adminer) -o jsonpath={.spec.host})"
```

## OpenShift

This is how to deploy and run the app in OpenShift.
Make sure you are in the namespace/project you want this deployed to.

1. Use Kustomize to create the app

    ```shell
    oc apply -k ./openshift
    # wait for everything to come up
    ```

2. Migrate database

    ```shell
    oc exec pods/$(oc get pods | grep Running  | grep djangotodos | awk '{print $1}') -- python ./manage.py migrate
    ```

3. Create user for the app

    ```shell
    oc exec pods/$(oc get pods | grep Running  | grep djangotodos | awk '{print $1}') -- bash -c "DJANGO_SUPERUSER_PASSWORD=Rj2nia9S6s9i python3 manage.py createsuperuser --username admin --email admin@example.com --noinput"
    ```

4. Set allowed and csrf host

    ```shell
    oc set env deployments/djangotodos CSRF_TRUSTED_ORIGINS=$(oc get routes | grep djangotodos | awk '{print $2}')
    ```

5. Add annotations and labels

    ```shell
    # labels
    oc label deployments/djangotodos app.kubernetes.io/part-of=django-todo-app
    oc label deployments/djangotodos app.openshift.io/runtime=python
    oc label deployments/djangotodos app.openshift.io/runtime-version=3.12
    oc label deployments/djangotodos app.kubernetes.io/name=djangotodos
    oc label deployments/db app.kubernetes.io/part-of=django-todo-app
    oc label deployments/db app.openshift.io/runtime=postgresql
    oc label deployments/db app.openshift.io/runtime-version=15
    oc label deployments/db app.kubernetes.io/name=db
    # annotations
    oc annotate deployments/djangotodos app.openshift.io/connects-to='[{"apiVersion":"apps/v1","kind":"Deployment","name":"db"}]'
    oc annotate deployments/djangotodos app.openshift.io/vcs-uri='https://github.com/jkeam/djangotodos.git'
    oc annotate deployments/djangotodos app.openshift.io/vcs-ref='main'
    ```

6. Open URL to app

    ```shell
    echo "https://$(oc get routes/djangotodos -o jsonpath='{.spec.host}')"
    # login with username: admin and password: Rj2nia9S6s9i
    ```

## OpenShift Pipeline

```shell
# setup
oc new-project todo-pipeline
oc new-project todo-dev
oc policy add-role-to-user edit system:serviceaccount:todo-pipeline:pipeline -n todo-dev
oc policy add-role-to-user system:image-puller system:serviceaccount:todo-dev:default -n todo-pipeline

# db for pipeline
oc new-app --name db \
      --env POSTGRESQL_USER=todouser \
      --env POSTGRESQL_PASSWORD=todopassword \
      --env POSTGRESQL_ADMIN_PASSWORD=adminpassword \
      --env POSTGRESQL_DATABASE=todos \
      --image registry.redhat.io/rhel9/postgresql-15@sha256:802c7926383f9e4b31ac48dd42e5b7cce920c8ef09920abe2724e50a84fbea0b \
      --namespace todo-pipeline

# db for dev
oc new-app --name db \
      --env POSTGRESQL_USER=todouser \
      --env POSTGRESQL_PASSWORD=todopassword \
      --env POSTGRESQL_ADMIN_PASSWORD=adminpassword \
      --env POSTGRESQL_DATABASE=todos \
      --image registry.redhat.io/rhel9/postgresql-15@sha256:802c7926383f9e4b31ac48dd42e5b7cce920c8ef09920abe2724e50a84fbea0b \
      --namespace todo-dev

# pipeline secret, update values with real
# openshift/pipeline/email-server-secret.yaml

# pipeline
oc project todo-pipeline
oc apply -k ./openshift/pipeline
```

## Local

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

## Docs

1. [Django Packages](https://djangopackages.org)
2. [Class-Based View Docs](https://ccbv.co.uk/)
3. [Django Docs](https://docs.djangoproject.com/en/5.0/)
