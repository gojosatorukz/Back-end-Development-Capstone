from unittest.mock import Mock, patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Concert, ConcertAttending

class ConcertTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test-attendee')
        self.concert = Concert.objects.create(concert_name='Capstone Live', city='Almaty', duration=90, date='2026-12-01')
    def test_public_pages_and_anonymous_access(self):
        for name in ['index', 'login', 'signup']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertRedirects(self.client.get(reverse('concerts')), reverse('login'))
        self.assertRedirects(self.client.post(reverse('concert_attendee'), {'concert_id': self.concert.pk, 'attendee_choice': 'Attending'}), reverse('login'))
    def test_authenticated_attendance_lifecycle(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse('concerts')), 'Capstone Live')
        self.assertContains(self.client.get(reverse('concert_detail', args=[self.concert.pk])), 'Capstone Live')
        for choice in ['Attending', 'Not Attending']:
            self.assertRedirects(self.client.post(reverse('concert_attendee'), {'concert_id': self.concert.pk, 'attendee_choice': choice}), reverse('concerts'))
            self.assertEqual(ConcertAttending.objects.get(user=self.user, concert=self.concert).attending, choice)
        self.assertEqual(ConcertAttending.objects.count(), 1)
        self.assertEqual(self.client.post(reverse('concert_attendee'), {'concert_id': self.concert.pk, 'attendee_choice': 'invalid'}).status_code, 400)
        self.assertEqual(self.client.get(reverse('concert_detail', args=[9999])).status_code, 404)
        self.assertRedirects(self.client.get(reverse('logout')), reverse('login'))
        self.assertRedirects(self.client.get(reverse('concerts')), reverse('login'))
    @patch('concert.views.requests.get')
    def test_microservice_rendering(self, get):
        get.return_value = Mock(json=lambda: {'songs': [{'id': 1, 'title': 'API song', 'lyrics': 'From service'}]})
        self.assertContains(self.client.get(reverse('songs')), 'API song')
        get.return_value = Mock(json=lambda: [{'id': 1, 'pic_url': 'https://example.com/photo.png', 'event_city': 'Almaty', 'event_state': 'Almaty', 'event_date': '2026-12-01'}])
        self.assertContains(self.client.get(reverse('photos')), 'Almaty')
