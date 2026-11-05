# Djirection Band Website


Django application for the IBM Back-end Application Development Capstone. Provides registration, login/logout, administrator-managed concerts and attendance, plus Pictures and Songs microservice pages.


Set PICTURES_SERVICE_URL and SONGS_SERVICE_URL through environment variables. Install requirements.txt, run `python manage.py migrate`, create a superuser interactively, and run `python manage.py runserver 0.0.0.0:8000`.


The Docker entrypoint applies migrations and starts the server; it does not create a default password. Deployment reads service URLs from the band-services ConfigMap. This is a course development-server deployment.


Validation: Django system check and 3 integration tests passed; actual administrator login, concert creation, editing and attendance were verified in the browser.



## Environment Setup

Created from the IBM Skills Network sfvih-Back-end-Development-Capstone template. Use Python 3.9.x and an isolated virtual environment.

```bash
python3.9 -m venv ~/backend-django-venv
source ~/backend-django-venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Set PICTURES_SERVICE_URL to the Pictures service base URL and SONGS_SERVICE_URL to the Songs service base URL before starting the application.

## Administrator Access

Open http://127.0.0.1:8000/admin/ (or the deployed application URL followed by /admin/). The Django administration login page contains Username, Password and Log in. Sign in with the superuser created using createsuperuser; there is no default password. In the admin dashboard select Concerts, then Add concert. Enter its name, duration, city and date, and save. Existing concerts can be edited from this dashboard.

## Application Usage

- Home displays the Djirection band introduction.
- Songs loads the song list from the Flask service. Click a song title to open its Lyrics modal, then use Close to dismiss it.
- Photos loads the picture cards from the Pictures service, with date and location.
- Signup creates an account; Login authenticates it and Logout ends its session. Enter and keep your own strong password.
- Concerts is available after sign-in. Open a concert to view details and select an attendance choice, then save. The concert list displays the saved status.

## Verification

Three Django integration tests passed. Browser checks verified registration, login/logout, administrator access, concert creation/editing, attendance, song lyrics and photos. The deployed application was also checked in Kubernetes.
