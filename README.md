# Djirection Band Website

Django application for the IBM Back-end Application Development Capstone. Provides registration, login/logout, administrator-managed concerts and attendance, plus Pictures and Songs microservice pages.

Set PICTURES_SERVICE_URL and SONGS_SERVICE_URL through environment variables. Install requirements.txt, run `python manage.py migrate`, create a superuser interactively, and run `python manage.py runserver 0.0.0.0:8000`.

The Docker entrypoint applies migrations and starts the server; it does not create a default password. Deployment reads service URLs from the band-services ConfigMap. This is a course development-server deployment.

Validation: Django system check and 3 integration tests passed; actual administrator login, concert creation, editing and attendance were verified in the browser.
