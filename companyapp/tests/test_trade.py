import pytest
from django.urls import reverse
from companyapp.models import Trade


@pytest.mark.django_db
def test_trade_add(client, django_user_model, user):

   client.force_login(user)
   response = client.get('/trade_add/')
   assert response.status_code == 200

   response = client.post(reverse("trade_add"), {"trade_name": "1101Z", "slug": "1101z"})
   assert response.status_code == 302
   assert len(Trade.objects.all()) == 1

   trade = Trade.objects.first()

   assert trade.trade_name == "1101Z"
   assert trade.slug == "1101z"
