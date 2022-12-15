# from calendar import calendar
# from datetime import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Company, CompanyRatios, Task, Trade


class AddFileForm(forms.Form):
   file_name = forms.FileField()


class RatiosAddForm(forms.Form):
    company_name = forms.CharField(max_length=255)
    number_NIP = forms.IntegerField()
    year_results = forms.IntegerField()
    assets_fixed = forms.FloatField()
    assets_current = forms.FloatField()
    stock = forms.FloatField()
    receivables_short_term = forms.FloatField()
    receivables_trade = forms.FloatField()
    receivables_tax = forms.FloatField()
    investments_short_term = forms.FloatField()
    assets_cash = forms.FloatField()
    capital_share = forms.FloatField()
    provision_and_accruals = forms.FloatField()
    liabilities_long_therm = forms.FloatField()
    liabilities_long_therm_financial = forms.FloatField()
    liabilities_short_therm = forms.FloatField()
    liabilities_short_therm_financial = forms.FloatField()
    liabilities_short_therm_trade = forms.FloatField()
    revenue = forms.FloatField()
    profit_operating = forms.FloatField()
    depreciation = forms.FloatField()
    profit_gross = forms.FloatField()
    tax_income = forms.FloatField()


def validate_nip(nip_int):
   nip_str = str(nip_int)
   nip_str.replace('-', '')
   if len(nip_str) != 10 or not nip_str.isdigit():
       raise ValidationError("Check you NIP")

   digits = [int(i) for i in nip_str]
   weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
   check_sum = sum(d * w for d, w in zip(digits, weights)) % 11
   if check_sum == digits[9]:
       return digits


class CompanyForm(forms.Form):
   company_name = forms.CharField(max_length=255)
   number_NIP = forms.IntegerField(validators=[validate_nip])
   active = forms.BooleanField()
   trade = forms.CharField(max_length=255)



class TradeForm(forms.Form):
   trade_name = forms.CharField(max_length=64, label='nr PKD')
   description = forms.Textarea()


class ResultForm(ModelForm):
   class Meta:
       model = CompanyRatios
       fields = ['liabilities_long_therm_financial', 'liabilities_short_therm_financial']

class LoginForm(forms.Form):
   login = forms.CharField(max_length=64)
   password = forms.CharField(widget=forms.PasswordInput)

class AddUserForm(forms.Form):
   login = forms.CharField(max_length=100)
   password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
   password_repeat = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput)
   first_name = forms.CharField(label='First name', max_length=100)
   last_name = forms.CharField(label='Last name', max_length=100)
   mail = forms.EmailField(max_length=100)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput)

class TaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new'}))
    deadline = forms.DateField(widget=forms.SelectDateWidget)
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    description = forms.Textarea()


class TaskEditForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    deadline = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea())

class SearchForm(forms.Form):
    name = forms.CharField(label="Search from PKD", max_length=64, required=True)
