"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from companyapp.views import IndexView, MyAccount, RatiosAdd, RatiosAddFile, AddUser, LoginUser, LogoutUser, \
    ChangePasswordView, CompanyAdd, TradeAdd, CompanyEdit, CompanyDetail, CompanyDelete, TradeSearchCompany, \
    TaskDetail, TaskEdit, TaskDelete, TaskAdd, RatiosDetail, RatiosEdit, RatiosDelete, EmptyPage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('accounts/', MyAccount.as_view(), name="accounts"),
    path('page_empty/', EmptyPage.as_view(), name="page_empty"),
    path('user_add/', AddUser.as_view(), name="user_add"),
    path('user_login/', LoginUser.as_view(), name="user_login"),
    path('user_logout/', LogoutUser.as_view(), name="user_logout"),
    path('user_change_password/<int:user_id>/', ChangePasswordView.as_view(), name="user_change_pass"),
    path('file_add/', RatiosAddFile.as_view(), name="file_add"),
    path('ratios_add/', RatiosAdd.as_view(), name="ratios_add"),
    path('ratios_detail/<int:ratios_id>/', RatiosDetail.as_view(), name="ratios_detail"),
    path('ratios_edit/<int:ratios_id>/', RatiosEdit.as_view(), name="ratios_edit"),
    path('ratios_delete/<int:ratios_id>/', RatiosDelete.as_view(), name="ratios_delete"),
    path('company_detail/<int:company_id>/', CompanyDetail.as_view(), name="company_detail"),
    path('company_add/', CompanyAdd.as_view(), name="company_add"),
    path('company_edit/<int:company_id>/', CompanyEdit.as_view(), name="company_edit"),
    path('company_delete/<int:company_id>/', CompanyDelete.as_view(), name="company_delete"),
    path('trade_add/', TradeAdd.as_view(), name="trade_add"),
    path('trade_search/', TradeSearchCompany.as_view(), name="trade_search"),
    path('task_add/', TaskAdd.as_view(), name="task_add"),
    path('task_detail/<int:task_id>/', TaskDetail.as_view(), name="task_detail"),
    path('task_edit/<int:task_id>/', TaskEdit.as_view(), name="task_edit"),
    path('task_delite/<int:task_id>/', TaskDelete.as_view(), name="task_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
