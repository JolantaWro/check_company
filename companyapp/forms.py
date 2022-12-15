from calendar import calendar
from datetime import datetime

# from django import forms
# from django.contrib.admin.widgets import AdminDateWidget
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm
# from .models import Company, CompanyRatios, Task, Trade
#
#
# class AddLinkForm(forms.Form):
#    docfile = forms.FileField()
#
#
# class AddResultsForm(forms.Form):
#
#    company = forms.CharField(max_length=255)
#    number_NIP = forms.IntegerField()
#    year_results = forms.IntegerField()
#    # dodaj walidacje
#
#    aktywa_trwałe = forms.FloatField()
#    aktywa_obrotowe= forms.FloatField()
#    zapasy = forms.FloatField()
#    nalez_krotkoterminowe = forms.FloatField()
#    nalez_dost_uslug = forms.FloatField()
#    nalez_podatkowe = forms.FloatField()
#    inwest_krotkoterminowe = forms.FloatField()
#    pap_wartosciowe = forms.FloatField()
#    srodki_pieniez = forms.FloatField()
#    kap_podstawowy = forms.FloatField()
#    rez_rozli_okres = forms.FloatField()
#    zob_dlugo = forms.FloatField()
#    zob_dlugo_finansowe = forms.FloatField()
#    zob_krotko = forms.FloatField()
#    zob_krotko_finansowe = forms.FloatField()
#    przychody = forms.FloatField()
#    dzial_operacyjny = forms.FloatField()
#    amortyzacja = forms.FloatField()
#    brutto = forms.FloatField()
#    podatek = forms.FloatField()
#
# def validate_nip(nip_int):
#    nip_str = str(nip_int)
#    nip_str.replace('-', '')
#    if len(nip_str) != 10 or not nip_str.isdigit():
#        raise ValidationError("Check you NIP")
#
#    digits = [int(i) for i in nip_str]
#    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
#    check_sum = sum(d * w for d, w in zip(digits, weights)) % 11
#    if check_sum == digits[9]:
#        return digits
#
#
# class CompanyForm(forms.Form):
#    name = forms.CharField(max_length=255)
#    numberNip = forms.IntegerField(validators=[validate_nip])
#    active = forms.BooleanField()
#    trade = forms.CharField(max_length=255)
#
#
#
# class TradeForm(forms.Form):
#    trade_name = forms.CharField(max_length=64, label='nr PKD')
#    description = forms.Textarea()
#
#
# class ResultForm(ModelForm):
#    class Meta:
#        model = CompanyRatios
#        fields = ['dl_zobowiazania_finansowe', 'kr_zobowiazania_finansowe']
#
# class LoginFormP(forms.Form):
#    login = forms.CharField(max_length=64)
#    password = forms.CharField(widget=forms.PasswordInput)
#
# class AddUserForm(forms.Form):
#    login = forms.CharField(max_length=100)
#    password = forms.CharField(label='Hasło', max_length=100, widget=forms.PasswordInput)
#    password_repeat = forms.CharField(label='Powtórzone hasło', max_length=100, widget=forms.PasswordInput)
#    first_name = forms.CharField(label='Imię', max_length=100)
#    last_name = forms.CharField(label='Nazwisko', max_length=100)
#    mail = forms.EmailField(max_length=100)
#
# class ChangePasswordForm(forms.Form):
#    password = forms.CharField(label='Hasło', max_length=100, widget=forms.PasswordInput)
#    repeat_password = forms.CharField(label='Powtórzone hasło', max_length=100, widget=forms.PasswordInput)
#
# class TaskForm(forms.Form):
#    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new'}))
#    deadline = forms.DateField(widget=forms.SelectDateWidget)
#    company = forms.ModelChoiceField(queryset=Company.objects.all())
#    description = forms.Textarea()
#
#
# class TaskEditForm(forms.Form):
#    title = forms.CharField(widget=forms.TextInput())
#    deadline = forms.DateField(widget=forms.SelectDateWidget)
#    description = forms.CharField(widget=forms.Textarea())
#
# class SearchForm(forms.Form):
#    name = forms.CharField(label="Wyszukiwane po PKD", max_length=64, required=True)
