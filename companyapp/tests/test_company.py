import pytest
from django.urls import reverse
from companyapp.models import Company


@pytest.mark.django_db
def test_add_company(auto_login_user, trade):
  client, user = auto_login_user()

  url = reverse('company_add')
  response = client.get(url)
  assert response.status_code == 200


  data = {
      'author': user,
      'name': 'Zywiec',
      'number_NIP': 5530016738,
      'active': True,
      'trade': trade,
  }
  response = client.post('/company_add/', data)
  assert response.status_code == 302


@pytest.mark.django_db
def test_company_details(auto_login_user, trade):
    client, user = auto_login_user()

    company = Company.objects.create(author=user, company_name="Zywiec", number_NIP=5530016738, active=True, trade=trade)

    url = reverse('company_detail', kwargs={'company_id': company.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "Zywiec" in str(response.content)



@pytest.mark.django_db
def test_company_details_404(auto_login_user, trade):
    client, user = auto_login_user()

    company = Company.objects.create(author=user, company_name="Zywiec", number_NIP=5530016738, active=True, trade=trade)
    url = reverse('company_detail', kwargs={'company_id': 100})
    response = client.get(url)

    assert response.status_code == 404
