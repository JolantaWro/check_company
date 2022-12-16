import pytest
from django.urls import reverse
from companyapp.models import Task, Company


@pytest.mark.django_db
def test_add_task(auto_login_user, trade):
  client, user = auto_login_user()
  company = Company.objects.create(author=user, company_name="Zywiec", number_NIP=5530016738, active=True, trade=trade)

  url = reverse('task_add')
  response = client.get(url)
  assert response.status_code == 200


  data = {
      'author': user,
      'title': 'Faktura za Gaz',
      'deadline': '2022, 12, 30',
      'company': company,
      'description': 'Czas do końca miesiąca',
  }
  response = client.post('/task_add/', data)
  assert response.status_code == 302

@pytest.mark.django_db
def test_task_details(auto_login_user, trade):
    client, user = auto_login_user()
    company = Company.objects.create(author=user, company_name="Zywiec", number_NIP=5530016738, active=True, trade=trade)

    task = Task.objects.create(author=user, title='Faktura', deadline='2022-12-31', company=company, description='Czas do końca miesiąca')

    url = reverse('task_detail', kwargs={'task_id': task.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "Faktura" in str(response.content)


@pytest.mark.django_db
def test_task_details(auto_login_user, trade):
    client, user = auto_login_user()
    company = Company.objects.create(author=user, company_name="Zywiec", number_NIP=5530016738, active=True, trade=trade)

    task = Task.objects.create(author=user, title='Faktura', deadline='2022-12-31', company=company, description='Czas do końca miesiąca')

    url = reverse('task_detail', kwargs={'task_id': 100})
    response = client.get(url)
    assert response.status_code == 404