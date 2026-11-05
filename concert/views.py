import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending

def index(request):
    return render(request, 'index.html')

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username'].strip()
        password = form.cleaned_data['password']
        try:
            if not username or len(username) > 100:
                raise ValidationError('Enter a username of at most 100 characters.')
            validate_password(password, User(username=username))
            user = User.objects.create_user(username=username, password=password)
        except (ValidationError, IntegrityError):
            form.add_error(None, 'Choose an unused username and a strong password.')
        else:
            login(request, user)
            return redirect('index')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def _service_data(base, endpoint, key=None):
    response = requests.get(base.rstrip('/') + endpoint, timeout=8)
    response.raise_for_status()
    data = response.json()
    return data.get(key, []) if key else data

def songs(request):
    try:
        rows = _service_data(os.environ.get('SONGS_SERVICE_URL', 'http://127.0.0.1:5001'), '/song', 'songs')
    except (requests.RequestException, ValueError, AttributeError):
        return render(request, 'songs.html', {'songs': [], 'service_error': 'Songs service temporarily unavailable.'}, status=503)
    return render(request, 'songs.html', {'songs': rows})

def photos(request):
    try:
        rows = _service_data(os.environ.get('PICTURES_SERVICE_URL', 'http://127.0.0.1:5000'), '/picture')
    except (requests.RequestException, ValueError, AttributeError):
        return render(request, 'photos.html', {'photos': [], 'service_error': 'Pictures service temporarily unavailable.'}, status=503)
    return render(request, 'photos.html', {'photos': rows})

def concerts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    rows = []
    for concert in Concert.objects.all():
        attendance = concert.attendee.filter(user=request.user).first()
        rows.append({'concert': concert, 'status': attendance.attending if attendance else '-'})
    return render(request, 'concerts.html', {'concerts': rows})

def concert_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    concert = get_object_or_404(Concert, pk=id)
    attendance = concert.attendee.filter(user=request.user).first()
    return render(request, 'concert_detail.html', {
        'concert_details': concert,
        'status': attendance.attending if attendance else '-',
        'attending_choices': ConcertAttending.AttendingChoices.choices})

def concert_attendee(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method != 'POST':
        return redirect('concerts')
    concert = get_object_or_404(Concert, pk=request.POST.get('concert_id'))
    choice = request.POST.get('attendee_choice')
    if choice not in ConcertAttending.AttendingChoices.values:
        return HttpResponseBadRequest('Invalid attendance choice')
    ConcertAttending.objects.update_or_create(concert=concert, user=request.user, defaults={'attending': choice})
    return redirect('concerts')
