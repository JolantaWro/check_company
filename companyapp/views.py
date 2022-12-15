from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AddResultsForm, CompanyForm, AddFileForm, LoginForm, AddUserForm, ChangePasswordForm, TradeForm, \
   SearchForm, TaskForm, ResultForm, TaskEditForm
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from .models import Company, CompanyRatios, Category, Document, Trade, Task
from django.contrib.auth.models import Group, Permission


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user_login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                form.add_error(None, 'Incorrect login or password')
        return redirect('accounts')

class LogoutUser(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('index')


class AddUser(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'user_form.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            password_repeat = form.cleaned_data.get('password_repeat')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            mail = form.cleaned_data.get('mail')
            if User.objects.filter(username=username).exists():
                raise ValidationError('Login already exists')

            if password != password_repeat:
                form.add_error(None, 'Password entered incorrectly')


            new_user = User.objects.create_user(username=username, password=password, email=mail)
            add_company = Permission.objects.get(codename='add_company')
            view_company = Permission.objects.get(codename='view_company')
            change_company = Permission.objects.get(codename='change_company')
            delete_company = Permission.objects.get(codename='delete_company')
            add_document = Permission.objects.get(codename='add_document')
            view_document = Permission.objects.get(codename='view_document')
            add_category = Permission.objects.get(codename='add_category')
            view_category = Permission.objects.get(codename='view_category')
            change_category = Permission.objects.get(codename='change_category')
            delete_category = Permission.objects.get(codename='delete_category')

            add_companyratios = Permission.objects.get(codename='add_companyratios')
            view_companyratios = Permission.objects.get(codename='view_companyratios')
            change_companyratios = Permission.objects.get(codename='change_companyratios')
            delete_companyratios = Permission.objects.get(codename='delete_companyratios')

            add_trade = Permission.objects.get(codename='add_trade')
            view_trade = Permission.objects.get(codename='view_trade')
            change_trade = Permission.objects.get(codename='change_trade')
            delete_trade = Permission.objects.get(codename='delete_trade')

            add_task = Permission.objects.get(codename='add_task')
            view_task = Permission.objects.get(codename='view_task')
            change_task = Permission.objects.get(codename='change_task')
            delete_task = Permission.objects.get(codename='delete_task')

            new_user.user_permissions.add(add_company, view_company, change_company, delete_company, add_document \
                                        , view_document, add_category, view_category, change_category, delete_category \
                                        , add_companyratios, view_companyratios, change_companyratios \
                                        , delete_companyratios, add_trade, view_trade, change_trade, delete_trade
                                        , add_task, view_task, change_task, delete_task)


            new_user.save()
            return redirect('accounts')

        return redirect('accounts')



class ChangePasswordView(PermissionRequiredMixin, View):

    def get(self, request, user_id):
        form = ChangePasswordForm()
        return render(request, 'user_form.html', {'form': form})

    def post(self, request, user_id):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=user_id)
            password = form.cleaned_data.get('password')
            repeat_password = form.cleaned_data.get('repeat_password')
            if password != repeat_password:
                form.add_error('Password entered incorrectly')

            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('accounts')
        return redirect('accounts')

class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
#
#
class MyAccount(View):
    """View for the logged in user and displays his information"""

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            amount_of_company = Company.objects.filter(author=request.user).count()
            company_all = Company.objects.filter(author=request.user)
            task_all = Task.objects.filter(author=request.user).order_by("deadline")
            cnx = {
                "amount_of_company": amount_of_company,
                "company_all": company_all,
                "task_all": task_all
            }
            return render(request, 'accounts.html', cnx)
        else:
            message = f"Lack of access"
            return render(request, 'accounts.html', context={'message': message})


class CompanyAdd(LoginRequiredMixin,View):
    """The ability to add a company to the database"""

    def get(self, request):
        form = CompanyForm()
        return render(request, 'base_form.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            number_nip = form.cleaned_data.get('number_NIP')
            active = form.cleaned_data.get('active')
            trade = form.cleaned_data.get('trade')

            trade, _ = Trade.objects.get_or_create(
                trade_name=trade
            )
            trade.save()

            company, _ = Company.objects.get_or_create(
                number_NIP=number_nip,
                defaults={'company_name': company_name, 'author': request.user, 'active': active, 'trade': trade}
            )
            company.save()
            return redirect('accounts')
        return redirect('accounts')


class CompanyView(View):
    """The ability to view a company from user database"""
    def get(self, request):
        company_all = Company.objects.filter(author=request.user)

        return render(request, 'company.html', {'company_all': company_all})

class CompanyDetail(LoginRequiredMixin,View):
    """The ability to view a detail company from user database"""

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        result = CompanyRatios.objects.filter(author=request.user).filter(company=company_id)
        result = list(result)
        task = Task.objects.filter(author=request.user).filter(company=company_id).count()
        if not task > 0:
            message = "No task"
            return render(request, 'company_detail.html', {'company': company, 'result': result, 'message': message})
        task = Task.objects.filter(author=request.user).filter(company=company_id).order_by("deadline")

        return render(request, 'company_detail.html', {'company': company, 'result': result, 'task': task})



class CompanyEdit(LoginRequiredMixin,View):
    """The ability to edit a detail company from user database"""

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        form = CompanyForm(initial={'company_name': company.company_name, 'number_NIP': company.number_NIP, 'trade': company.trade})
        return render(request, 'base_form.html', {'form': form})

    def post(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        form = CompanyForm(request.POST, initial={'company_name': company.company_name, 'number_NIP': company.number_NIP})
        if form.is_valid():
            trade = form.cleaned_data.get('trade')

            trade, _ = Trade.objects.get_or_create(
              trade_name=trade
            )
            trade.save()

            company, _ = Company.objects.update_or_create(pk=company_id)
            company.company_name = form.cleaned_data.get('company_name')
            company.number_NIP = form.cleaned_data.get('number_NIP')
            company.active = form.cleaned_data.get('active')
            company.trade = trade
            company.save()

            return redirect('accounts')
        return redirect('accounts')

class CompanyDelete(LoginRequiredMixin,View):
    """The ability to delete a company from user database"""

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        return render(request, 'delete_form.html', {'form': company})

    def post(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        company.delete()
        return redirect('accounts')


class TradeAdd(LoginRequiredMixin,View):
    """Add Trade to user database"""

    def get(self, request):
        form = TradeForm()
        return render(request, 'base_form.html', {'form': form})

    def post(self, request):
        form = TradeForm(request.POST)
        if form.is_valid():
            trade_name = form.cleaned_data.get('trade_name')
            description = form.cleaned_data.get('description')

            trade, _ = Trade.objects.get_or_create(
                trade_name=trade_name,
                defaults={'description': description}
            )
            trade.save()
            return redirect('accounts')
        return redirect('accounts')


class TradeSearchCompany(LoginRequiredMixin,View):
    """Search company from user database"""

    def get(self, request):
        form = SearchForm()
        return render(request, 'trade_search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            company_all = Company.objects.filter(trade__trade_name__icontains=name)
            return render(request, 'trade_search.html', {'company_all': company_all, 'form': SearchForm()})

        return render(request, 'trade_search.html', {'form': form})



class RatiosAdd(View):
    """Iterator for analyzing the company's financial result of manually entered data."""
    def get(self, request):
        form = AddResultsForm()
        return render(request, 'ratios_manual_add_form.html', {'form': form})

    def post(self, request):
        form = AddResultsForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name')
            number_nip = form.cleaned_data.get('number_NIP')
            number_nip = int(number_nip)
            year_result = form.cleaned_data.get('year_results')
            assets_fixed = form.cleaned_data.get('assets_fixed')
            assets_current = form.cleaned_data.get('assets_current')
            stock = form.cleaned_data.get('stock')
            receivables_short_term = form.cleaned_data.get('receivables_short_term')
            receivables_trade = form.cleaned_data.get('receivables_trade')
            receivables_tax = form.cleaned_data.get('receivables_tax')
            investments_short_term = form.cleaned_data.get('investments_short_term')
            assets_cash = form.cleaned_data.get('assets_cash')
            capital_share = form.cleaned_data.get('capital_share')
            provision_and_accruals = form.cleaned_data.get('provision_and_accruals')
            liabilities_long_therm = form.cleaned_data.get('liabilities_long_therm')
            liabilities_long_therm_financial = form.cleaned_data.get('liabilities_long_therm_financial')
            liabilities_short_therm = form.cleaned_data.get('liabilities_short_therm')
            liabilities_short_therm_financial = form.cleaned_data.get('liabilities_short_therm_financial')
            liabilities_short_therm_trade = form.cleaned_data.get('liabilities_short_therm_trade')
            revenue = form.cleaned_data.get('revenue')
            profit_operating = form.cleaned_data.get('profit_operating')
            depreciation = form.cleaned_data.get('depreciation')
            profit_gross = form.cleaned_data.get('profit_gross')
            tax_income = form.cleaned_data.get('tax_income')
            assets_total = assets_fixed + assets_current
            equity = assets_total - provision_and_accruals - liabilities_long_therm - liabilities_short_therm
            liabilities_and_equity = liabilities_long_therm + provision_and_accruals + equity + liabilities_short_therm
            profit_net = profit_gross - tax_income

            capitalization = round(equity / liabilities_and_equity * 100, 1)
            current_ratio = round(assets_current / liabilities_short_therm, 2)
            debt_ratio = round(liabilities_short_therm + liabilities_long_therm + provision_and_accruals, 0)
            debt_to_equity_ratio = round(debt_ratio / equity * 100, 1)
            receivables_turnover_ratio = round(receivables_trade / revenue * 360 * 1, 0)
            liabilities_turnover_ratio = round(liabilities_short_therm_trade / revenue * 360 * 1, 0)
            profit_operating_margin = round(profit_operating / revenue * 100, 1)
            profit_net_margin = round(profit_net / revenue * 100, 1)
            debt_financial_net = round(liabilities_long_therm_financial + liabilities_short_therm_financial \
                                       - assets_cash, 0)
            ebitda = round(profit_operating + depreciation, 0)
            debt_financial_net_to_ebitda = round(debt_financial_net/ebitda, 2)


            user = request.user
            if user.is_authenticated:
                company, _ = Company.objects.get_or_create(
                  number_NIP=number_nip,
                  defaults={'company_name': company_name, 'author': request.user})
                company.save()

                if capitalization > 20 and current_ratio > 1 and debt_to_equity_ratio < 300:
                    category = Category()
                    category.id = 1
                    category.rating_name = 1
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income= tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)


                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

                if capitalization < 20 and current_ratio < 1 and debt_to_equity_ratio > 300:
                    category = Category()
                    category.id = 2
                    category.rating_name = 2
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income = tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)

                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

                else:
                    category = Category()
                    category.id = 3
                    category.rating_name = 3
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income = tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)

                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

            else:
                if capitalization > 20 and current_ratio > 1 and debt_to_equity_ratio < 300:
                    category = "Low risk"
                elif capitalization < 20 and current_ratio < 1 and debt_to_equity_ratio > 300:
                    category = "High risk"
                else:
                    category = "Medium risk"

                return render(request, 'ratios_view.html', locals())


def convert_to_float(root, value):
    element = root.find(value)
    if element:
        element_value = element.find('.//{*}KwotaA').text
        element_value = round(float(element_value)/1000, 2)
    else:
        element_value = 0.00
    return element_value


def give_depreciation(root, value_first, value_second):
    depreciation = root.find(value_first)
    if depreciation:
        depreciation = depreciation.find('.//{*}KwotaA').text
        depreciation = round(float(depreciation) / 1000, 2)
    else:
        depreciation = root.find(value_second)
        depreciation = depreciation.find('.//{*}KwotaA').text
        depreciation = round(float(depreciation) / 1000, 2)
    return depreciation



class NewRatiosFile(View):
    """Iterator to analyze the financial result of the company automatically entered data."""

    def get(self, request):
        form = AddFileForm()
        return render(request, 'ratios_file_add.html', {'form': form})

    def post(self, request):
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Document(file_name=request.FILES['file_name'])
            instance.save()

            tree = ET.parse(instance.file_name)
            root = tree.getroot()
            ET.register_namespace("", "http://www.mf.gov.pl/schematy/SF/DefinicjeTypySprawozdaniaFinansowe/2018/07/09/JednostkaInnaWZlotych")

            element_year = root.find('.//{*}Naglowek')
            year = element_year.find('.//{*}OkresDo')
            year_result = year.text
            year_result = year_result[0:4]
            year_result = int(year_result)

            company_name = root.find('.//{*}NazwaFirmy')
            company_name = company_name.text

            number_nip = root.find('.//{*}P_1D')
            number_nip = number_nip.text
            number_nip = int(number_nip)

            company_pkd = root.find('.//{*}KodPKD')
            company_pkd = company_pkd.text

            assets_fixed = './/{*}Aktywa_A'
            assets_fixed = convert_to_float(root, assets_fixed)

            assets_current = './/{*}Aktywa_B'
            assets_current = convert_to_float(root, assets_current)

            element_assets_current = root.find('.//{*}Aktywa_B')
            stock = './/{*}Aktywa_B_I'
            stock = convert_to_float(element_assets_current, stock)

            receivables_short_term = './/{*}Aktywa_B_II'
            receivables_short_term = convert_to_float(root, receivables_short_term)

            receivables_trade_related = './/{*}Aktywa_B_II_1_A'
            receivables_trade_related = convert_to_float(root, receivables_trade_related)
            receivables_trade_shares = './/{*}Aktywa_B_II_2_A'
            receivables_trade_shares = convert_to_float(root, receivables_trade_shares)
            receivables_trade_other = './/{*}Aktywa_B_II_3_A'
            receivables_trade_other = convert_to_float(root, receivables_trade_other)
            receivables_trade = receivables_trade_related + receivables_trade_shares + receivables_trade_other

            receivables_tax = './/{*}Aktywa_B_II_3_B'
            receivables_tax = convert_to_float(root, receivables_tax)

            investments_short_term = './/{*}Aktywa_B_III'
            investments_short_term = convert_to_float(root, investments_short_term)

            assets_cash = './/{*}Aktywa_B_III_1_C'
            assets_cash = convert_to_float(root, assets_cash)

            equity = './/{*}Pasywa_A'
            equity = convert_to_float(root, equity)

            capital_share = './/{*}Pasywa_A_I'
            capital_share = convert_to_float(root, capital_share)

            provision = './/{*}Pasywa_B_I'
            provision = convert_to_float(root, provision)
            accruals = './/{*}Pasywa_B_IV'
            accruals = convert_to_float(root, accruals)
            provision_and_accruals = round(provision + accruals, 2)

            liabilities_long_therm = './/{*}Pasywa_B_II'
            liabilities_long_therm = convert_to_float(root, liabilities_long_therm)

            liabilities_long_therm_credits = './/{*}Pasywa_B_II_3_A'
            liabilities_long_therm_credits = convert_to_float(root, liabilities_long_therm_credits)
            liabilities_long_therm_other_financial = './/{*}Pasywa_B_II_3_C'
            liabilities_long_therm_other_financial = convert_to_float(root, liabilities_long_therm_other_financial)

            liabilities_long_therm_financial = liabilities_long_therm_credits + liabilities_long_therm_other_financial

            liabilities_short_therm = './/{*}Pasywa_B_III'
            liabilities_short_therm = convert_to_float(root, liabilities_short_therm)

            liabilities_short_therm_credits = './/{*}Pasywa_B_III_3_A'
            liabilities_short_therm_credits = convert_to_float(root, liabilities_short_therm_credits)
            liabilities_short_therm_other_financial = './/{*}Pasywa_B_III_3_C'
            liabilities_short_therm_other_financial = convert_to_float(root, liabilities_short_therm_other_financial)
            liabilities_short_therm_financial = liabilities_short_therm_credits+ liabilities_short_therm_other_financial

            liabilities_short_therm_trade_related = './/{*}Pasywa_B_III_1_A'
            liabilities_short_therm_trade_related = convert_to_float(root, liabilities_short_therm_trade_related)
            liabilities_short_therm_trade_shares = './/{*}Pasywa_B_III_2_A'
            liabilities_short_therm_trade_shares = convert_to_float(root, liabilities_short_therm_trade_shares)
            liabilities_short_therm_trade_other = './/{*}Pasywa_B_III_3_D_1'
            liabilities_short_therm_trade_other = convert_to_float(root, liabilities_short_therm_trade_other)
            liabilities_short_therm_trade = liabilities_short_therm_trade_related + liabilities_short_therm_trade_shares\
                                            + liabilities_short_therm_trade_other

            revenue = './/{*}A'
            revenue = convert_to_float(root, revenue)

            profit_operating = './/{*}F'
            profit_operating = convert_to_float(root, profit_operating)

            depreciation = give_depreciation(root, './/{*}B_I', './/{*}A_II_1')

            profit_gross = './/{*}I'
            profit_gross = convert_to_float(root, profit_gross)

            tax_income = './/{*}J'
            tax_income = convert_to_float(root, tax_income)

            profit_net = './/{*}L'
            profit_net = convert_to_float(root, profit_net)

            assets_total = './/{*}Aktywa'
            assets_total = convert_to_float(root, assets_total)

            liabilities_and_equity = './/{*}Pasywa'
            liabilities_and_equity = convert_to_float(root, liabilities_and_equity)

            capitalization = round(equity / liabilities_and_equity * 100, 1)
            current_ratio = round(assets_current / liabilities_short_therm, 2)
            debt_ratio = round(liabilities_short_therm + liabilities_long_therm + provision_and_accruals, 0)
            debt_to_equity_ratio = round(debt_ratio / equity * 100, 1)
            receivables_turnover_ratio = round(receivables_trade / revenue * 360 * 1, 0)
            liabilities_turnover_ratio = round(liabilities_short_therm_trade / revenue * 360 * 1, 0)
            profit_operating_margin = round(profit_operating / revenue * 100, 1)
            profit_net_margin = round(profit_net / revenue * 100, 1)
            debt_financial_net = round(liabilities_long_therm_financial + liabilities_short_therm_financial \
                                   - assets_cash, 0)
            ebitda = round(profit_operating + depreciation, 0)
            debt_financial_net_to_ebitda = round(debt_financial_net / ebitda, 2)


            user = request.user
            if user.is_authenticated:
                trade, _ = Trade.objects.get_or_create(trade_name=company_pkd)
                trade.save()

                company, _ = Company.objects.get_or_create(
                    number_NIP=number_nip,
                    defaults={'company_name': company_name, 'author': request.user, 'trade': trade})
                company.save()


                if capitalization > 20 and current_ratio > 1 and debt_to_equity_ratio < 300:
                    category = Category()
                    category.id = 1
                    category.rating_name = 1
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income = tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)

                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

                if capitalization < 20 and current_ratio < 1 and debt_to_equity_ratio > 300:
                    category = Category()
                    category.id = 2
                    category.rating_name = 2
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income = tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)

                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

                else:
                    category = Category()
                    category.id = 3
                    category.rating_name = 3
                    category.save()

                    ratios = CompanyRatios()
                    ratios.company_name = company
                    ratios.category = category
                    ratios.year_name = year_result
                    ratios.assets_fixed = assets_fixed
                    ratios.assets_current = assets_current
                    ratios.stock = stock
                    ratios.receivables_short_term = receivables_short_term
                    ratios.receivables_trade = receivables_trade
                    ratios.receivables_tax = receivables_tax
                    ratios.investments_short_term = investments_short_term
                    ratios.assets_cash = assets_cash
                    ratios.assets_total = assets_total
                    ratios.equity = equity
                    ratios.capital_share = capital_share
                    ratios.provision_and_accruals = provision_and_accruals
                    ratios.liabilities_long_therm = liabilities_long_therm
                    ratios.liabilities_long_therm_financial = liabilities_long_therm_financial
                    ratios.liabilities_short_therm = liabilities_short_therm
                    ratios.liabilities_short_therm_financial = liabilities_short_therm_financial
                    ratios.liabilities_and_equity = liabilities_and_equity
                    ratios.revenue = revenue
                    ratios.profit_operating = profit_operating
                    ratios.depreciation = depreciation
                    ratios.profit_gross = profit_gross
                    ratios.tax_income = tax_income
                    ratios.profit_net = profit_net
                    ratios.capitalization = capitalization
                    ratios.current_ratio = current_ratio
                    ratios.debt_ratio = debt_ratio
                    ratios.debt_to_equity_ratio = debt_to_equity_ratio
                    ratios.receivables_turnover_ratio = receivables_turnover_ratio
                    ratios.liabilities_turnover_ratio = liabilities_turnover_ratio
                    ratios.profit_operating_margin = profit_operating_margin
                    ratios.profit_net_margin = profit_net_margin
                    ratios.debt_financial_net = debt_financial_net
                    ratios.ebitda = ebitda
                    ratios.debt_financial_net_to_ebitda = debt_financial_net_to_ebitda
                    ratios.author = request.user
                    ratios.save()

                    deadline = datetime.today() + timedelta(days=180)

                    task = Task()
                    task.author = request.user
                    task.title = "Add new financial analysis"
                    task.deadline = deadline
                    task.company = company
                    task.save()

                    return redirect('show', result_id=ratios.id)

            else:
                if capitalization > 20 and current_ratio > 1 and debt_to_equity_ratio < 300:
                    category = "Low risk"
                elif capitalization < 20 and current_ratio < 1 and debt_to_equity_ratio > 300:
                    category = "High risk"
                else:
                    category = "Medium risk"

                return render(request, 'ratios_view.html', locals())

        return redirect('index')


#
# #
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
class TaskAdd(LoginRequiredMixin, View):
  def get(self, request):
      form = TaskForm()
      return render(request, 'base_form.html', {'form': form})

  def post(self, request):
      form = TaskForm(request.POST)
      if form.is_valid():
          title = form.cleaned_data.get('title')
          deadline = form.cleaned_data.get('deadline')
          company = form.cleaned_data.get('company')
          description = form.cleaned_data.get('description')
          task = Task()
          task.author = request.user
          task.title = title
          task.deadline = deadline
          task.description = description
          task.company = company
          task.save()
          return redirect('accounts')
      return redirect('accounts')

class TaskDetail(LoginRequiredMixin, View):
  def get(self, request):
      task_all = Task.objects.filter(author=request.user)

      return render(request, 'accounts.html', {'task_all': task_all})

class TaskEdit(LoginRequiredMixin, View):

  def get(self, request, task_id):
      task = get_object_or_404(Task, pk=task_id)
      form = TaskEditForm(initial={'title': task.title, 'deadline': task.deadline, 'description': task.description})
      return render(request, 'base_form.html', {'form': form})

  def post(self, request, task_id):
      task= get_object_or_404(Task, pk=task_id)
      form = TaskEditForm(request.POST, initial={'title': task.title, 'deadline': task.deadline, 'description': task.description})
      if form.is_valid():

          task, _ = Task.objects.update_or_create(pk=task_id)
          task.title = form.cleaned_data.get('title')
          task.deadline = form.cleaned_data.get('deadline')
          task.description = form.cleaned_data.get('description')
          task.company = task.company
          task.save()
          return redirect('accounts')

      return redirect('accounts')

class TaskDelete(LoginRequiredMixin, View):

  def get(self, request, task_id):
      task = get_object_or_404(Task, pk=task_id)
      return render(request, 'delete_form.html', {'form': task })

  def post(self, request, task_id):
      task = get_object_or_404(Task, pk=task_id)
      task.delete()
      return redirect('accounts')

class TaskDetail(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)

        return render(request, 'task_detail.html', {'task': task})

