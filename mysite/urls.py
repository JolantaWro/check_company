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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from companyapp.views import IndexView, MyAccount, NewRatios, NewRatiosFile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('accounts/', MyAccount.as_view(), name="accounts"),

    # path('add_user/', AddUser.as_view(), name="add_user"),
    # path('login_user/', LoginUser.as_view(), name="login_user"),
    # path('logout_user/', LogoutUser.as_view(), name="logout_user"),
    # path('change_password/', ChangePasswordView.as_view(), name="change_pass"),
    path('file_add/', NewRatiosFile.as_view(), name="file_add"),
    path('results_add/', NewRatios.as_view(), name="results_add"),
    # path('show/<int:result_id>/', ViewRatios.as_view(), name="show"),
    # path('edit_result/<int:result_id>/', EditRatios.as_view(), name="edit_result"),
    # path('delete_result/<int:result_id>/', DeleteRatios.as_view(), name="delete_result"),
    # path('show_company/<int:company_id>/', ShowCompany.as_view(), name="show_company"),
    # path('add_company/', NewCompany.as_view(), name="add_company"),
    # path('edit_company/<int:company_id>/', EditCompany.as_view(), name="edit_company"),
    # path('delete_company/<int:company_id>/', DeleteCompany.as_view(), name="delete_company"),
    # # path('company/', CompanyView.as_view(), company_name="company_all"),
    # path('add_trade/', NewTrade.as_view(), name="add_trade"),
    # path('search_trade/', TradeSearchCompany.as_view(), name="search_trade"),
    # path('add_task/', AddTask.as_view(), name="add_task"),
    # path('show_task/<int:task_id>/', TaskViewDetail.as_view(), name="show_task"),
    # path('edit_task/<int:task_id>/', EditTask.as_view(), name="edit_task"),
    # path('delete_task/<int:task_id>/', DeleteTask.as_view(), name="delete_task"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
