"""graphweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from datanalyse import views as views1
from django.contrib.auth import views as views2
from datanalyse.forms import LoginForm
from django.contrib.auth.decorators import login_required
from datanalyse.forms import RegistrationForm



app_name="datanalyse"
urlpatterns = [

    #url(r'^$',  views.homeview, name='home'),
    #url(r'^(?P<username>[\w.@+-]+)/$',  views.UserPortsListView.as_view(), name='index'),
    url(r'^home/$',  login_required(views1.UserPortsListView.as_view()), name='index'),
    url(r'^$', views2.login, {'template_name': 'datanalyse/landingnew.html', 'authentication_form': LoginForm,},name='loggingin'),
    url(r'^logout/$', views2.logout, {'next_page': '/'},name='logout'),
    url(r'^register/$', views1.RegisterUser.as_view(), name='register'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(views1.DetailView.as_view()), name='detail'),
    url(r'^sell/(?P<pk>\d+)$', login_required(views1.SellStock.as_view()), name='sell-detail'),
    url(r'^ss/(?P<pk>\d+)$',  login_required(views1.Sell.as_view()), name='ss'),
    url(r'^howto/$',  login_required(views1.howtoview.as_view()), name='howto'),
    url(r'^buy/$',  login_required(views1.buyview.as_view()), name='buystock'),
    # url(r'^autocomplete/$',views1.AutoCompleteView.as_view(), name='autocomplete'),
    url(r'^news/$',  login_required(views1.newsView.as_view()), name='news'),
    url(r'^buys/$', login_required(views1.buy_category), name='buy_category'),
    url(r'^finalbuy/$', login_required(views1.FinalBuy.as_view()), name='finalbuy'),
    url(r'^learn/$',  login_required(views1.learnview.as_view()), name='learn'),
]
