import pytest
from django.test import Client
from companyapp.models import Trade, Company
import uuid


@pytest.fixture
def client():
   client = Client()
   return client

@pytest.fixture
def user(django_user_model):
   username = "userA"
   password = "userApassword"
   user_test = django_user_model.objects.create_user(username=username, password=password)

   return user_test

@pytest.fixture
def trade():
   trade = Trade.objects.create(trade_name='3223Z', slug='3223z')

   return trade


@pytest.fixture
def test_password():
   return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)

   return make_user

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
  def make_auto_login(user=None):
      if user is None:
          user = create_user()
      client.login(username=user.username, password=test_password)
      return client, user
  return make_auto_login