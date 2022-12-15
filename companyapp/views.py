
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# from .forms import AddResultsForm, CompanyForm, AddLinkForm, LoginFormP, AddUserForm, ChangePasswordForm, TradeForm, \
#    SearchForm, TaskForm, ResultForm, TaskEditForm
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from .models import Company, CompanyRatios, Category, Document, Trade, Task
from django.contrib.auth.models import Group, Permission

# class LoginUser(View):
#
#   def get(self, request):
#       form = LoginFormP()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = LoginFormP(request.POST)
#       if form.is_valid():
#           username = form.cleaned_data.get('login')
#           password = form.cleaned_data.get('password')
#           user = authenticate(username=username, password=password)
#           if user:
#               login(request, user)
#           else:
#               form.add_error(None, 'Zły login lub hasło')
#       return redirect('accounts')
#
# class LogoutUser(LoginRequiredMixin,View):
#   def get(self, request):
#       logout(request)
#       return redirect('index')
#
#
# class AddUser(View):
#   def get(self, request):
#       form = AddUserForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = AddUserForm(request.POST)
#       if form.is_valid():
#           username = form.cleaned_data.get('login')
#           password = form.cleaned_data.get('password')
#           repeat_password = form.cleaned_data.get('password_repeat')
#           first_name = form.cleaned_data.get('first_name')
#           last_name = form.cleaned_data.get('last_name')
#           mail = form.cleaned_data.get('mail')
#           if User.objects.filter(username=username).exists():
#               raise ValidationError('Ten login jest już zajęty')
#
#           if password != repeat_password:
#               form.add_error(None, 'Błąd dot. hasła')
#
#
#           new_user = User.objects.create_user(username=username, password=password, email=mail)
#           add_company = Permission.objects.get(codename='add_company')
#           view_company = Permission.objects.get(codename='view_company')
#           change_company = Permission.objects.get(codename='change_company')
#           delete_company = Permission.objects.get(codename='delete_company')
#           add_document = Permission.objects.get(codename='add_document')
#           view_document = Permission.objects.get(codename='view_document')
#           add_category = Permission.objects.get(codename='add_category')
#           view_category = Permission.objects.get(codename='view_category')
#           change_category = Permission.objects.get(codename='change_category')
#           delete_category = Permission.objects.get(codename='delete_category')
#
#           add_companyratios = Permission.objects.get(codename='add_companyratios')
#           view_companyratios = Permission.objects.get(codename='view_companyratios')
#           change_companyratios = Permission.objects.get(codename='change_companyratios')
#           delete_companyratios = Permission.objects.get(codename='delete_companyratios')
#
#           add_trade = Permission.objects.get(codename='add_trade')
#           view_trade = Permission.objects.get(codename='view_trade')
#           change_trade = Permission.objects.get(codename='change_trade')
#           delete_trade = Permission.objects.get(codename='delete_trade')
#
#           add_task = Permission.objects.get(codename='add_task')
#           view_task = Permission.objects.get(codename='view_task')
#           change_task = Permission.objects.get(codename='change_task')
#           delete_task = Permission.objects.get(codename='delete_task')
#
#           new_user.user_permissions.add(add_company, view_company, change_company, delete_company, add_document \
#                                         , view_document, add_category, view_category, change_category, delete_category \
#                                         , add_companyratios, view_companyratios, change_companyratios \
#                                         , delete_companyratios, add_trade, view_trade, change_trade, delete_trade
#                                         , add_task, view_task, change_task, delete_task)
#
#
#           new_user.save()
#           return redirect('accounts')
#
#       return redirect('accounts')
#
#
#
# class ChangePasswordView(PermissionRequiredMixin, View):
#   permission_required = 'auth.change_user'
#
#   def get(self, request, user_id):
#       form = ChangePasswordForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request, user_id):
#       form = ChangePasswordForm(request.POST)
#       if form.is_valid():
#           user = get_object_or_404(User, pk=user_id)
#           password = form.cleaned_data.get('password')
#           repeat_password = form.cleaned_data.get('repeat_password')
#           if password != repeat_password:
#               form.add_error('Wprowadzone dane różnią się')
#
#           user.set_password(form.cleaned_data.get('password'))
#           user.save()
#           return redirect('accounts')
#       return redirect('accounts')
#
#
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
#
#
class MyAccount(View):
    pass
#
#   def get(self, request):
#       user = request.user
#       if user.is_authenticated:
#           amount_of_company = Company.objects.filter(author=request.user).count()
#           company_all = Company.objects.filter(author=request.user)
#           task_all = Task.objects.filter(author=request.user).order_by("deadline")
#           cnx = {
#               "amount_of_company": amount_of_company,
#               "company_all": company_all,
#               "task_all": task_all
#           }
#           return render(request, 'accounts.html', cnx)
#       else:
#           message = f"Częśc tylko dla zalogowanych. W celu skorzystania zaloguj się bądź zarejestruj"
#           return render(request, 'accounts.html',
#                         context={'message': message})
#
#
# class NewCompany(LoginRequiredMixin,View):
#
#   def get(self, request):
#       form = CompanyForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = CompanyForm(request.POST)
#       if form.is_valid():
#           name = form.cleaned_data.get('company_name')
#           numberNIP = form.cleaned_data.get('numberNip')
#           active = form.cleaned_data.get('active')
#           trade = form.cleaned_data.get('trade')
#
#
#           trade, _ = Trade.objects.get_or_create(
#               trade_name=trade
#           )
#           trade.save()
#
#           company, _ = Company.objects.get_or_create(
#               number_NIP=numberNIP,
#               defaults={'company_name': name, 'author': request.user, 'active': active, 'trade':trade}
#           )
#           company.save()
#           return redirect('accounts')
#       return redirect('accounts')
#
#
# # class CompanyView(View):
# #    def get(self, request):
# #        company_all = Company.objects.filter(author=request.user)
# #
# #        return render(request, 'company.html', {'company_all': company_all})
#
# class ShowCompany(LoginRequiredMixin,View):
#
#   def get(self, request, company_id):
#       company = get_object_or_404(Company, pk=company_id)
#       result = CompanyRatios.objects.filter(author=request.user).filter(company=company_id)
#       result = list(result)
#       task = Task.objects.filter(author=request.user).filter(company=company_id).count()
#       if not task > 0:
#           msg = "Brak zdarzeń"
#           return render(request, 'show_detail.html', {'company': company, 'result': result, 'msg': msg})
#       task = Task.objects.filter(author=request.user).filter(company=company_id).order_by("deadline")
#       # task = list(task)
#
#       return render(request, 'show_detail.html', {'company': company, 'result': result, 'task': task})
#
#
#
# class EditCompany(LoginRequiredMixin,View):
#   # permission_required = 'homework_app.change_category'
#
#   def get(self, request, company_id):
#       company = get_object_or_404(Company, pk=company_id)
#       form = CompanyForm(initial={'name': company.name, 'numberNip': company.number_NIP, 'trade': company.trade})
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request, company_id):
#       company = get_object_or_404(Company, pk=company_id)
#       form = CompanyForm(request.POST, initial={'name': company.name, 'numberNip': company.number_NIP})
#       if form.is_valid():
#           trade = form.cleaned_data.get('trade')
#
#           trade, _ = Trade.objects.get_or_create(
#               trade_name=trade
#           )
#           trade.save()
#
#           edit_company, _ = Company.objects.update_or_create(pk=company_id)
#           edit_company.name = form.cleaned_data.get('company_name')
#           edit_company.number_NIP = form.cleaned_data.get('numberNip')
#           edit_company.active = form.cleaned_data.get('active')
#           edit_company.trade = trade
#           edit_company.save()
#
#           return redirect('accounts')
#       return redirect('accounts')
#
# class DeleteCompany(LoginRequiredMixin,View):
#
#   def get(self, request, company_id):
#       company = get_object_or_404(Company, pk=company_id)
#       return render(request, 'delete_company.html', {'company': company})
#
#   def post(self, request, company_id):
#       company = get_object_or_404(Company, pk=company_id)
#       company.delete()
#       return redirect('accounts')
#
#
# class NewTrade(LoginRequiredMixin,View):
#
#   def get(self, request):
#       form = TradeForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = TradeForm(request.POST)
#       if form.is_valid():
#           name = form.cleaned_data.get('trade_name')
#           description = form.cleaned_data.get('description')
#
#           trade, _ = Trade.objects.get_or_create(
#               trade_name=name,
#               defaults={'description': description}
#           )
#           trade.save()
#           return redirect('accounts')
#       return redirect('accounts')
#
#
# class TradeSearchCompany(LoginRequiredMixin,View):
#
#   def get(self, request):
#       form = SearchForm()
#       return render(request, 'search.html', {'form': form})
#
#   def post(self, request):
#       form = SearchForm(request.POST or None)
#
#       if form.is_valid():
#           name = form.cleaned_data.get('company_name')
#           company_all = Company.objects.filter(trade__trade_name__icontains=name)
#           return render(request, 'search.html', {'company_all': company_all, 'form': SearchForm()})
#
#       return render(request, 'search.html', {'form': form})
#
#
#
# class NewRatios(View):
#
#   def get(self, request):
#       form = AddResultsForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = AddResultsForm(request.POST)
#       if form.is_valid():
#           company_results = form.cleaned_data.get('company')
#           number_company = form.cleaned_data.get('number_NIP')
#           number_company = int(number_company)
#           year_result = form.cleaned_data.get('year_results')
#           aktywa_trwałe = form.cleaned_data.get('aktywa_trwałe')
#           aktywa_obrotowe = form.cleaned_data.get('aktywa_obrotowe')
#           zapasy = form.cleaned_data.get('zapasy')
#           nalez_krotkoterminowe = form.cleaned_data.get('nalez_krotkoterminowe')
#           nalez_dost_uslug = form.cleaned_data.get('nalez_dost_uslug')
#           nalez_podatkowe = form.cleaned_data.get('nalez_podatkowe')
#           inwest_krotkoterminowe = form.cleaned_data.get('inwest_krotkoterminowe')
#           pap_wartosciowe = form.cleaned_data.get('pap_wartosciowe')
#           srodki_pieniez = form.cleaned_data.get('srodki_pieniez')
#           kap_podstawowy = form.cleaned_data.get('kap_podstawowy')
#           rez_rozli_okres = form.cleaned_data.get('rez_rozli_okres')
#           zob_dlugo = form.cleaned_data.get('zob_dlugo')
#           zob_dlugo_finansowe = form.cleaned_data.get('zob_dlugo_finansowe')
#           zob_krotko = form.cleaned_data.get('zob_krotko')
#           zob_krotko_finansowe = form.cleaned_data.get('zob_krotko_finansowe')
#           przychody = form.cleaned_data.get('przychody')
#           dzial_operacyjny = form.cleaned_data.get('dzial_operacyjny')
#           amortyzacja = form.cleaned_data.get('amortyzacja')
#           brutto = form.cleaned_data.get('brutto')
#           podatek = form.cleaned_data.get('podatek')
#           suma_aktywow = aktywa_trwałe + aktywa_obrotowe
#           kapitl_wlasny = suma_aktywow - rez_rozli_okres - zob_dlugo - zob_krotko
#           suma_pasywow = zob_dlugo + rez_rozli_okres + kapitl_wlasny + zob_krotko
#           zysk_netto = brutto - podatek
#
#           kapitalizacja = round(kapitl_wlasny / suma_pasywow * 100, 1)
#           plynnosc = round(aktywa_obrotowe / zob_krotko, 2)
#           zobowiazania = round(zob_krotko + zob_dlugo + rez_rozli_okres, 0)
#           zobowiazania_kapitale = round(zobowiazania / kapitl_wlasny * 100, 1)
#           obrot_naleznosciami = round(nalez_dost_uslug / przychody * 360 * 1, 0)
#           marza_operacyjna = round(dzial_operacyjny / przychody * 100, 1)
#           marza_netto = round(zysk_netto / przychody * 100, 1)
#           zadl_finansowe_netto = round(zob_dlugo_finansowe + zob_krotko_finansowe - srodki_pieniez, 0)
#           ebitda = round(dzial_operacyjny + amortyzacja, 0)
#
#
#           user = request.user
#           if user.is_authenticated:
#               company, _ = Company.objects.get_or_create(
#                   number_NIP=number_company,
#                   defaults={'company_name': company_results, 'author': request.user})
#               company.save()
#
#               if kapitalizacja > 20 and plynnosc > 1 and zobowiazania_kapitale < 300:
#                   add_category = Category()
#                   add_category.id = 1
#                   add_category.rating_name = 1
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = year_result
#                   new_add.aktywa_trwale = aktywa_trwałe
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = nalez_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = nalez_dost_uslug
#                   new_add.naleznosci_podatkowe = nalez_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwest_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniez
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapitl_wlasny
#                   new_add.kapital_podstawowy = kap_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rez_rozli_okres
#                   new_add.zobowiazania_dlugoterminowe = zob_dlugo
#                   new_add.dl_zobowiazania_finansowe = zob_dlugo_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zob_krotko
#                   new_add.kr_zobowiazania_finansowe = zob_krotko_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = dzial_operacyjny
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = brutto
#                   new_add.podatek_dochodowy = podatek
#                   new_add.zysk_strata_netto = zysk_netto
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#               if kapitalizacja < 20 and plynnosc < 1 and zobowiazania_kapitale > 300:
#                   add_category = Category()
#                   add_category.id = 2
#                   add_category.rating_name = 2
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = year_result
#                   new_add.aktywa_trwale = aktywa_trwałe
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = nalez_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = nalez_dost_uslug
#                   new_add.naleznosci_podatkowe = nalez_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwest_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniez
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapitl_wlasny
#                   new_add.kapital_podstawowy = kap_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rez_rozli_okres
#                   new_add.zobowiazania_dlugoterminowe = zob_dlugo
#                   new_add.dl_zobowiazania_finansowe = zob_dlugo_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zob_krotko
#                   new_add.kr_zobowiazania_finansowe = zob_krotko_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = dzial_operacyjny
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = brutto
#                   new_add.podatek_dochodowy = podatek
#                   new_add.zysk_strata_netto = zysk_netto
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#               else:
#                   add_category = Category()
#                   add_category.id = 3
#                   add_category.rating_name = 3
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = year_result
#                   new_add.aktywa_trwale = aktywa_trwałe
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = nalez_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = nalez_dost_uslug
#                   new_add.naleznosci_podatkowe = nalez_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwest_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniez
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapitl_wlasny
#                   new_add.kapital_podstawowy = kap_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rez_rozli_okres
#                   new_add.zobowiazania_dlugoterminowe = zob_dlugo
#                   new_add.dl_zobowiazania_finansowe = zob_dlugo_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zob_krotko
#                   new_add.kr_zobowiazania_finansowe = zob_krotko_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = dzial_operacyjny
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = brutto
#                   new_add.podatek_dochodowy = podatek
#                   new_add.zysk_strata_netto = zysk_netto
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#           else:
#               if kapitalizacja > 20 and plynnosc > 1 and zobowiazania_kapitale < 300:
#                   category = "Niskie ryzyko niewypłacalności"
#               elif kapitalizacja < 20 and plynnosc < 1 and zobowiazania_kapitale > 300:
#                   category = "Wysokie ryzyko niewypłacalności"
#               else:
#                   category = "Umiarkowane ryzyko niewypłacalności, wymagana pogłębiona analiza"
#
#               return render(request, 'bezLogowaniaReczne.html', locals())
#
#
# def convert_to_float(root, value):
#   element = root.find(value)
#   if element:
#       element_value = element.find('.//{*}KwotaA').text
#       element_value = round(float(element_value)/1000, 2)
#   else:
#       element_value = 0.00
#   return element_value
#
#
# def give_depreciation(root, value_first, value_second):
#   depreciation = root.find(value_first)
#   if depreciation:
#       depreciation = depreciation.find('.//{*}KwotaA').text
#       depreciation = round(float(depreciation) / 1000, 2)
#   else:
#       depreciation = root.find(value_second)
#       depreciation = depreciation.find('.//{*}KwotaA').text
#       depreciation = round(float(depreciation) / 1000, 2)
#   return depreciation
#
#
#
# class NewRatiosLink(View):
#
#   def get(self, request):
#       form = AddLinkForm()
#       return render(request, 'to_result_form.html', {'form': form})
#
#   def post(self, request):
#       form = AddLinkForm(request.POST, request.FILES)
#       if form.is_valid():
#           instance = Document(docfile=request.FILES['docfile'])
#           instance.save()
#
#           tree = ET.parse(instance.docfile)
#           root = tree.getroot()
#           ET.register_namespace("", "http://www.mf.gov.pl/schematy/SF/DefinicjeTypySprawozdaniaFinansowe/2018/07/09/JednostkaInnaWZlotych")
#
#           element_rok = root.find('.//{*}Naglowek')
#           rok = element_rok.find('.//{*}OkresDo')
#           wartrosc_rok = rok.text
#           wartrosc_rok = wartrosc_rok[0:4]
#           wartrosc_rok = int(wartrosc_rok)
#
#           nazwa_firmy = root.find('.//{*}NazwaFirmy')
#           nazwa_firmy = nazwa_firmy.text
#
#           number_NIP = root.find('.//{*}P_1D')
#           number_NIP = number_NIP.text
#           number_NIP = int(number_NIP)
#
#           pkd_firmy = root.find('.//{*}KodPKD')
#           pkd_firmy = pkd_firmy.text
#
#           aktywa_trwale = './/{*}Aktywa_A'
#           aktywa_trwale = convert_to_float(root, aktywa_trwale)
#
#           aktywa_obrotowe = './/{*}Aktywa_B'
#           aktywa_obrotowe = convert_to_float(root, aktywa_obrotowe)
#
#           element_obrotowe = root.find('.//{*}Aktywa_B')
#           zapasy = './/{*}Aktywa_B_I'
#           zapasy = convert_to_float(element_obrotowe, zapasy)
#
#           naleznosci_krotkoterminowe = './/{*}Aktywa_B_II'
#           naleznosci_krotkoterminowe = convert_to_float(root, naleznosci_krotkoterminowe)
#
#           naleznosci_dostawy_uslugi_powiazani = './/{*}Aktywa_B_II_1_A'
#           naleznosci_dostawy_uslugi_powiazani = convert_to_float(root, naleznosci_dostawy_uslugi_powiazani)
#           naleznosci_dostawy_uslugi_udzialy = './/{*}Aktywa_B_II_2_A'
#           naleznosci_dostawy_uslugi_udzialy = convert_to_float(root, naleznosci_dostawy_uslugi_udzialy)
#           naleznosci_dostawy_uslugi_pozostale = './/{*}Aktywa_B_II_3_A'
#           naleznosci_dostawy_uslugi_pozostale = convert_to_float(root, naleznosci_dostawy_uslugi_pozostale)
#           naleznosci_dostaw_uslug = naleznosci_dostawy_uslugi_powiazani + naleznosci_dostawy_uslugi_udzialy + naleznosci_dostawy_uslugi_pozostale
#
#           naleznosci_podatkowe = './/{*}Aktywa_B_II_3_B'
#           naleznosci_podatkowe = convert_to_float(root, naleznosci_podatkowe)
#
#           inwestycje_krotkoterminowe = './/{*}Aktywa_B_III'
#           inwestycje_krotkoterminowe = convert_to_float(root, inwestycje_krotkoterminowe)
#
#           srodki_pieniezne = './/{*}Aktywa_B_III_1_C'
#           srodki_pieniezne = convert_to_float(root, srodki_pieniezne)
#
#           kapital_wlasny = './/{*}Pasywa_A'
#           kapital_wlasny = convert_to_float(root, kapital_wlasny)
#
#           kapital_podstawowy = './/{*}Pasywa_A_I'
#           kapital_podstawowy = convert_to_float(root, kapital_podstawowy)
#
#           rezerwy = './/{*}Pasywa_B_I'
#           rezerwy = convert_to_float(root, rezerwy)
#           rozliczenia_miedzyokresowe = './/{*}Pasywa_B_IV'
#           rozliczenia_miedzyokresowe = convert_to_float(root, rozliczenia_miedzyokresowe)
#           rezerwy_rozliczenia_miedzyokresowe = round(rezerwy + rozliczenia_miedzyokresowe,2)
#
#           zobowiazania_dlugoterminowe = './/{*}Pasywa_B_II'
#           zobowiazania_dlugoterminowe = convert_to_float(root, zobowiazania_dlugoterminowe)
#
#           dl_pozostale_kredyty = './/{*}Pasywa_B_II_3_A'
#           dl_pozostale_kredyty = convert_to_float(root, dl_pozostale_kredyty)
#           dl_pozostale_inne_fiansowe = './/{*}Pasywa_B_II_3_C'
#           dl_pozostale_inne_fiansowe = convert_to_float(root, dl_pozostale_inne_fiansowe)
#
#           dl_zobowiazania_finansowe = dl_pozostale_kredyty + dl_pozostale_inne_fiansowe
#
#           zobowiazania_krotkoterminowe = './/{*}Pasywa_B_III'
#           zobowiazania_krotkoterminowe = convert_to_float(root, zobowiazania_krotkoterminowe)
#
#           kr_pozostale_kredyty = './/{*}Pasywa_B_III_3_A'
#           kr_pozostale_kredyty = convert_to_float(root, kr_pozostale_kredyty)
#           kr_pozostale_inne_fiansowe = './/{*}Pasywa_B_III_3_C'
#           kr_pozostale_inne_fiansowe = convert_to_float(root, kr_pozostale_inne_fiansowe)
#           kr_zobowiazania_finansowe = kr_pozostale_kredyty + kr_pozostale_inne_fiansowe
#
#           zobowiazania_podatkowe = './/{*}Pasywa_B_III_3_G'
#           zobowiazania_podatkowe = convert_to_float(root, zobowiazania_podatkowe)
#
#           przychody = './/{*}A'
#           przychody = convert_to_float(root, przychody)
#
#           zysk_strata_dzialalnosc_operacyjna = './/{*}F'
#           zysk_strata_dzialalnosc_operacyjna = convert_to_float(root, zysk_strata_dzialalnosc_operacyjna)
#
#           zysk_strata_dzialalnosc_operacyjna = './/{*}F'
#           zysk_strata_dzialalnosc_operacyjna = convert_to_float(root, zysk_strata_dzialalnosc_operacyjna)
#
#           amortyzacja = give_depreciation(root, './/{*}B_I', './/{*}A_II_1')
#
#           zysk_strata_brutto = './/{*}I'
#           zysk_strata_brutto = convert_to_float(root, zysk_strata_brutto)
#
#           podatek_dochodowy = './/{*}J'
#           podatek_dochodowy = convert_to_float(root, podatek_dochodowy)
#
#           zysk_strata_netto = './/{*}L'
#           zysk_strata_netto = convert_to_float(root, zysk_strata_netto)
#
#           suma_aktywow = './/{*}Aktywa'
#           suma_aktywow = convert_to_float(root, suma_aktywow)
#
#           suma_pasywow = './/{*}Pasywa'
#           suma_pasywow = convert_to_float(root, suma_pasywow)
#
#           kapitalizacja = round(kapital_wlasny / suma_pasywow * 100, 2)
#           plynnosc = round(aktywa_obrotowe / zobowiazania_krotkoterminowe, 2)
#           zobowiazania = zobowiazania_krotkoterminowe + zobowiazania_dlugoterminowe + rezerwy_rozliczenia_miedzyokresowe
#           zobowiazania_kapitale = round(zobowiazania / kapital_wlasny * 100, 2)
#           obrot_naleznosciami = round(naleznosci_dostaw_uslug / przychody * 360 * 1, 0)
#           marza_operacyjna = round(zysk_strata_dzialalnosc_operacyjna / przychody * 100,2)
#           marza_netto = round(zysk_strata_netto / przychody * 100, 2)
#           zadl_finansowe_netto = round(dl_zobowiazania_finansowe + kr_zobowiazania_finansowe - srodki_pieniezne, 2)
#           ebitda = round(zysk_strata_dzialalnosc_operacyjna + amortyzacja, 2)
#
#
#           user = request.user
#           if user.is_authenticated:
#               trade, _ = Trade.objects.get_or_create(trade_name=pkd_firmy)
#               trade.save()
#
#               company, _ = Company.objects.get_or_create(
#                   number_NIP=number_NIP,
#                   defaults={'company_name': nazwa_firmy, 'author': request.user, 'trade': trade})
#               company.save()
#
#
#               if kapitalizacja > 20 and plynnosc > 1 and zobowiazania_kapitale < 300:
#                   add_category = Category()
#                   add_category.id = 1
#                   add_category.rating_name = 1
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = wartrosc_rok
#
#                   new_add.aktywa_trwale = aktywa_trwale
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = naleznosci_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = naleznosci_dostaw_uslug
#                   new_add.naleznosci_podatkowe = naleznosci_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwestycje_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniezne
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapital_wlasny
#                   new_add.kapital_podstawowy = kapital_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rezerwy_rozliczenia_miedzyokresowe
#                   new_add.zobowiazania_dlugoterminowe = zobowiazania_dlugoterminowe
#                   new_add.dl_zobowiazania_finansowe = dl_zobowiazania_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zobowiazania_krotkoterminowe
#                   new_add.kr_zobowiazania_finansowe = kr_zobowiazania_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = zysk_strata_dzialalnosc_operacyjna
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = zysk_strata_brutto
#                   new_add.podatek_dochodowy = podatek_dochodowy
#                   new_add.zysk_strata_netto = zysk_strata_netto
#
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#               if kapitalizacja < 20 and plynnosc < 1 and zobowiazania_kapitale > 300:
#                   add_category = Category()
#                   add_category.id = 2
#                   add_category.rating_name = 2
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = wartrosc_rok
#                   new_add.aktywa_trwale = aktywa_trwale
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = naleznosci_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = naleznosci_dostaw_uslug
#                   new_add.naleznosci_podatkowe = naleznosci_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwestycje_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniezne
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapital_wlasny
#                   new_add.kapital_podstawowy = kapital_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rezerwy_rozliczenia_miedzyokresowe
#                   new_add.zobowiazania_dlugoterminowe = zobowiazania_dlugoterminowe
#                   new_add.dl_zobowiazania_finansowe = dl_zobowiazania_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zobowiazania_krotkoterminowe
#                   new_add.kr_zobowiazania_finansowe = kr_zobowiazania_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = zysk_strata_dzialalnosc_operacyjna
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = zysk_strata_brutto
#                   new_add.podatek_dochodowy = podatek_dochodowy
#                   new_add.zysk_strata_netto = zysk_strata_netto
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#               else:
#                   add_category = Category()
#                   add_category.id = 3
#                   add_category.rating_name = 3
#                   add_category.save()
#
#                   new_add = CompanyRatios()
#                   new_add.company = company
#                   new_add.category = add_category
#                   new_add.year_name = wartrosc_rok
#                   new_add.aktywa_trwale = aktywa_trwale
#                   new_add.aktywa_obrotowe = aktywa_obrotowe
#                   new_add.zapasy = zapasy
#                   new_add.naleznosci_krotkoterminowe = naleznosci_krotkoterminowe
#                   new_add.naleznosci_dostaw_uslug = naleznosci_dostaw_uslug
#                   new_add.naleznosci_podatkowe = naleznosci_podatkowe
#                   new_add.inwestycje_krotkoterminowe = inwestycje_krotkoterminowe
#                   new_add.srodki_pieniezne = srodki_pieniezne
#                   new_add.suma_aktywow = suma_aktywow
#                   new_add.kapital_wlasny = kapital_wlasny
#                   new_add.kapital_podstawowy = kapital_podstawowy
#                   new_add.rezerwy_rozliczenia_miedzyokresowe = rezerwy_rozliczenia_miedzyokresowe
#                   new_add.zobowiazania_dlugoterminowe = zobowiazania_dlugoterminowe
#                   new_add.dl_zobowiazania_finansowe = dl_zobowiazania_finansowe
#                   new_add.zobowiazania_krotkoterminowe = zobowiazania_krotkoterminowe
#                   new_add.kr_zobowiazania_finansowe = kr_zobowiazania_finansowe
#                   new_add.suma_pasywow = suma_pasywow
#                   new_add.przychody = przychody
#                   new_add.zysk_strata_dzialalnosc_operacyjna = zysk_strata_dzialalnosc_operacyjna
#                   new_add.amortyzacja = amortyzacja
#                   new_add.zysk_strata_brutto = zysk_strata_brutto
#                   new_add.podatek_dochodowy = podatek_dochodowy
#                   new_add.zysk_strata_netto = zysk_strata_netto
#                   new_add.capitalization = kapitalizacja
#                   new_add.current_ratio = plynnosc
#                   new_add.debt_ratio = zobowiazania
#                   new_add.debt_to_equity_ratio = zobowiazania_kapitale
#                   new_add.receivable_turnover_ratio = obrot_naleznosciami
#                   new_add.operating_profit_margin = marza_operacyjna
#                   new_add.net_profit_margin = marza_netto
#                   new_add.net_financial_debt = zadl_finansowe_netto
#                   new_add.EBITDA_12 = ebitda
#                   new_add.author = request.user
#                   new_add.save()
#
#                   deadline = datetime.today() + timedelta(days=180)
#
#                   new_task = Task()
#                   new_task.author = request.user
#                   new_task.title = "Badanie kondycji"
#                   new_task.deadline = deadline
#                   new_task.company = company
#                   new_task.save()
#
#                   return redirect('show', result_id=new_add.id)
#
#           else:
#               if kapitalizacja > 20 and plynnosc > 1 and zobowiazania_kapitale < 300:
#                   category = "Niskie ryzyko niewypłacalności"
#               elif kapitalizacja < 20 and plynnosc < 1 and zobowiazania_kapitale > 300 or zobowiazania_kapitale < 0:
#                   category = "Wysokie ryzyko niewypłacalności"
#               else:
#                   category = "Umiarkowane ryzyko niewypłacalności, wymagana pogłębiona analiza"
#
#               return render(request, 'bezLogowaniaLink.html', locals())
#
#
#
# class ViewRatios(View):
#   def get(self, request, result_id):
#       results = get_object_or_404(CompanyRatios, pk=result_id)
#       return render(request, 'show_result.html', {'results': [results]})
#
#
# class EditRatios(LoginRequiredMixin,View):
#
#   def get(self, request, result_id):
#       results = get_object_or_404(CompanyRatios, pk=result_id)
#       form = ResultForm(initial={'dl_zobowiazania_finansowe': results.dl_zobowiazania_finansowe, 'kr_zobowiazania_finansowe': results.kr_zobowiazania_finansowe})
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request, result_id):
#       results = get_object_or_404(CompanyRatios, pk=result_id)
#       form = ResultForm(request.POST)
#       if form.is_valid():
#
#           edit_result, _ = CompanyRatios.objects.update_or_create(pk=result_id)
#           edit_result.dl_zobowiazania_finansowe = form.cleaned_data.get('dl_zobowiazania_finansowe')
#           edit_result.kr_zobowiazania_finansowe = form.cleaned_data.get('kr_zobowiazania_finansowe')
#           edit_result.save()
#
#           return redirect('show', result_id=edit_result.id)
#       return redirect('accounts')
#
# class DeleteRatios(LoginRequiredMixin, View):
#
#   def get(self, request, result_id):
#       results = get_object_or_404(CompanyRatios, pk=result_id)
#       return render(request, 'delete_company.html', {'company': results})
#
#   def post(self, request, result_id):
#       results = get_object_or_404(CompanyRatios, pk=result_id)
#       results.delete()
#       return redirect('accounts')
#
#
#
# class AddTask(LoginRequiredMixin, View):
#   def get(self, request):
#       form = TaskForm()
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request):
#       form = TaskForm(request.POST)
#       if form.is_valid():
#           title = form.cleaned_data.get('title')
#           deadline = form.cleaned_data.get('deadline')
#           company = form.cleaned_data.get('company')
#           description = form.cleaned_data.get('description')
#           new_task = Task()
#           new_task.author = request.user
#           new_task.title = title
#           new_task.deadline = deadline
#           new_task.description = description
#           new_task.company = company
#           new_task.save()
#           return redirect('accounts')
#       return redirect('accounts')
#
# class TaskView(LoginRequiredMixin, View):
#   def get(self, request):
#       task_all = Task.objects.filter(author=request.user)
#
#       return render(request, 'accounts.html', {'task_all': task_all})
#
# class EditTask(LoginRequiredMixin, View):
#
#   def get(self, request, task_id):
#       task = get_object_or_404(Task, pk=task_id)
#       form = TaskEditForm(initial={'title': task.title, 'deadline': task.deadline, 'description': task.description})
#       return render(request, 'add_form.html', {'form': form})
#
#   def post(self, request, task_id):
#       task= get_object_or_404(Task, pk=task_id)
#       form = TaskEditForm(request.POST, initial={'title': task.title, 'deadline': task.deadline, 'description': task.description})
#       if form.is_valid():
#
#           edit_task, _ = Task.objects.update_or_create(pk=task_id)
#           edit_task.title = form.cleaned_data.get('title')
#           edit_task.deadline = form.cleaned_data.get('deadline')
#           edit_task.description = form.cleaned_data.get('description')
#           edit_task.company = edit_task.company
#           edit_task.save()
#
#           return redirect('accounts')
#       return redirect('accounts')
#
# class DeleteTask(LoginRequiredMixin, View):
#
#   def get(self, request, task_id):
#       task = get_object_or_404(Task, pk=task_id)
#       return render(request, 'delete_company.html', {'company': task})
#
#   def post(self, request, task_id):
#       task = get_object_or_404(Task, pk=task_id)
#       task.delete()
#       return redirect('accounts')
#
# class TaskViewDetail(LoginRequiredMixin, View):
#   def get(self, request, task_id):
#       task = get_object_or_404(Task, pk=task_id)
#
#       return render(request, 'show_detail_task.html', {'task': task})
#
