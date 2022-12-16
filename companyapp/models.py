from datetime import date
from django.conf import settings
from django.db import models
from django.utils.text import slugify

CATEGORY_CLASS = (
    (1, "Low risk"),
    (2, "Medium risk"),
    (3, "High risk"),
)


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating_name = models.IntegerField(choices=CATEGORY_CLASS)

    def __str__(self):
        return self.rating_name


class Trade(models.Model):
    trade_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.trade_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.trade_name


class Company(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    number_NIP = models.BigIntegerField(unique=True, null=True)
    active = models.BooleanField(null=True, default=True)
    category_ratios = models.ManyToManyField(Category, through="CompanyRatios")
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.company_name


class CompanyRatios(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    year_name = models.IntegerField()
    assets_fixed = models.FloatField()
    assets_current = models.FloatField()
    stock = models.FloatField()
    receivables_short_term = models.FloatField()
    receivables_trade = models.FloatField()
    receivables_tax = models.FloatField()
    investments_short_term = models.FloatField()
    assets_cash = models.FloatField()
    assets_total = models.FloatField()
    equity = models.FloatField()
    capital_share = models.FloatField()
    provision_and_accruals = models.FloatField()
    liabilities_long_therm = models.FloatField()
    liabilities_long_therm_financial = models.FloatField()
    liabilities_short_therm = models.FloatField()
    liabilities_short_therm_financial = models.FloatField()
    liabilities_trade = models.FloatField()
    liabilities_and_equity = models.FloatField()
    revenue = models.FloatField()
    profit_operating = models.FloatField()
    depreciation = models.FloatField()
    profit_gross = models.FloatField()
    tax_income = models.FloatField()
    profit_net = models.FloatField()
    capitalization = models.FloatField()
    current_ratio = models.FloatField()
    debt_ratio = models.FloatField()
    debt_to_equity_ratio = models.FloatField()
    receivables_turnover_ratio = models.FloatField()
    liabilities_turnover_ratio = models.FloatField()
    profit_operating_margin = models.FloatField()
    profit_net_margin = models.FloatField()
    debt_financial_net = models.FloatField()
    ebitda = models.FloatField()
    debt_financial_net_to_ebitda = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    file_name = models.FileField()


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    deadline = models.DateField(null=True, default=date.today())
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
