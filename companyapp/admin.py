from django.contrib import admin
from .models import Category, Company, Trade, CompanyRatios, Document, Task

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Trade)
admin.site.register(CompanyRatios)
admin.site.register(Document)
admin.site.register(Task)
