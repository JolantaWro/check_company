from django.contrib.auth.models import User
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client):
   response = client.get('')
   assert response.status_code == 200


@pytest.mark.django_db
def test_add_link_view(client):
   response = client.get('/file_add/')
   assert response.status_code == 200


@pytest.mark.django_db
def test_add_results_view(client):
   response = client.get('/ratios_add/')
   assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
   response = client.get('/user_logout/')
   assert response.status_code == 302

@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('test', 'test@test.com', 'test')

  assert User.objects.count() == 1


@pytest.mark.django_db
def test_auth_view(auto_login_user):
  client, user = auto_login_user()
  url = reverse('user_login')
  response = client.get(url)
  assert response.status_code == 200