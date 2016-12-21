from django.shortcuts import render, render_to_response,get_object_or_404,redirect
from datanalyse.models import UserPorts,User,UserMoney,TickerComp
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
# Create your views here.
import models
import feedparser
from django.views.generic import ListView,View,DetailView
from .forms import RegistrationForm
import operator
import json
import urllib2  # works fine with Python 2.7.9 (not 3.4.+)
import time
from django.db.models import Q
import wikipedia
from google import search
from django.contrib.auth.decorators import login_required


def abc(request):
	# Full path and name to your csv file
    csv_filepathname="/home/ashraydimri/Downloads/ListOfScrips.csv"
    # Full path to your django project directory




    import csv
    dataReader = csv.reader(open(csv_filepathname), delimiter=',')

    for row in dataReader:
        if row[0] != 'Ticker': # Ignore the header row, import everything else
            tc = TickerComp()
            tc.ticker= row[0]
            tc.name = row[1]
            tc.save()
    return

#@login_required(login_url="login/")
class UserPortsListView(ListView):
    #model = models.UserPorts    # shorthand for setting queryset = models.Car.objects.all()
    template_name = 'datanalyse/letsee.html'  # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    context_object_name = "userports_list"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 2 #and that's it !!

    def get_queryset(self):
        print (self.request.user.is_authenticated())
        t=get_object_or_404(User, username=self.request.user)
        t_stocks=UserPorts.objects.filter(user=t)
        #return t_stocks
        result=t_stocks

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_,(Q(companies__icontains=q) for q in query_list)))

        return result

    def get_context_data(self, **kwargs):
        context = super(UserPortsListView, self).get_context_data(**kwargs)
        context['usern'] = self.request.user
        getuser=get_object_or_404(User, username=self.request.user)
        usermoney=UserMoney.objects.filter(user=getuser)
        for u in usermoney:
            money=u.money
        context['money']=money
        return context

class DetailView(DetailView):
    model = UserPorts
    template_name='datanalyse/detail.html'
    #allu=""
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['usern'] = self.request.user


        getuser=get_object_or_404(User, username=self.request.user)
        usermoney=UserMoney.objects.filter(user=getuser)
        for u in usermoney:
            money=u.money
        context['money']=money


        link = "http://www.google.com/finance/info?infotype=infoquoteall&q="
        data=""
        object = super(DetailView, self).get_object()
        allu= object.companies
        url = link+"%s:%s" % ("BSE",allu)
        linkgraph = "https://chart.finance.yahoo.com/t?s=%s.BO&lang=en-IN&region=IN&width=500&height=300" % (allu)
        context["link"]=linkgraph

        print allu
        for urls in search(allu, tld='co.in', lang='en', stop=20):
            if 'wikipedia' in urls:
                pages= urls.split('/')
                page=pages[len(pages)-1]

                context["summary"]=(wikipedia.summary(page)).encode('ascii', 'ignore')
                wikipage = wikipedia.page(page)
                allp=page.split('_')
                wikimages=wikipage.images
                imurl=""

                for i in wikimages:
                    if 'logo' in i or 'Logo' in i:
                        if allu in i:
                            imurl=str(i)
                            break
                        for wrd in allp:
                            if wrd in i:
                                imurl=str(i)
                                break

                context["logo"]=imurl
                print imurl
                break



        u = urllib2.urlopen(url)
        content = u.read()
        data = json.loads(content[3:])
        x= json.dumps(data)
        info = data[0]
        l = float(str(info["l_fix"]).replace(",",""))
        name = str(info["name"])
        c = float(str(info["c_fix"]).replace(",",""))
        cp = float(str(info["cp_fix"]).replace(",",""))
        op = float(str(info["op"]).replace(",",""))
        hi = float(str(info["hi"]).replace(",",""))
        vo = str(info["vo"])
        lo = float(str(info["lo"]).replace(",",""))
        hi52 = float(str(info["hi52"]).replace(",",""))
        lo52 = float(str(info["lo52"]).replace(",",""))
        mc = str(info["mc"])
        context['l'] = l
        context['c'] = c
        context['cp'] = cp
        context['op'] = op
        context['hi'] = hi
        context['vo'] = vo
        context['lo'] = lo
        context['hi52'] = hi52
        context['lo52'] = lo52
        context['mc'] = mc
        context['name'] = name

        rsslink='https://www.google.co.in/finance/company_news?q=BSE:%s&output=rss' % (allu)
        feeds=feedparser.parse(rsslink)
        context['feeds']=feeds
        return context

    #def get_object(self):
        # Call the superclass
        #object = super(DetailView, self).get_object()
        #allu= object.companies
        #print allu
        # Return the object
        #return object

#def homeview(request):
#    return render(request,'datanalyse/landingnew.html')


class RegisterUser(View):
    def post(self,request):
        if request.method=='POST' and 'email' in request.POST:
            username=request.POST.get('username')
            email=request.POST.get('email','')
            pass1=request.POST.get('password')
            pass2=request.POST.get('confirmpassword')
            if pass1==pass2:
                if User.objects.filter(username=username):
                    #return HttpResponse("<h1 color='red'>username exists</h1>")
                    return redirect('/', message='Usename exists')
                else:
                    user = User.objects.create_user(username, email)
                    um=UserMoney()

                    user.set_password(pass1)

                    user.save()
                    um.user=user
                    um.save()
                    user=authenticate(username=username,password=pass1)


                    if user is not None:
                        if user.is_active:
                            login(request,user)
                            return redirect('/home/')



        return redirect('datanalyse:loggingin')

# class RegistrationFormView(View):
#     form_class=RegistrationForm
#     template_name="datanalyse/landingnew.html"
#
#     def get(self,request):
#         form=self.form_class(None)
#         return render(request,self.template_name,{"form":fomr})
#
#     def post(self,request):
#         from = self.form_class(request.POST)
#
#             if form.is_valid():
#                 user=form.save(commit=False)
#                 username=form.cleaned_data['username']
#                 password=form.cleaned_data['password']
#                 user.set_password(password)
#                 user.save()
#
#                 user.authenticate(username=username,password=password)
#
#                 if user is not None:
#                     if user.is_active:
#                         login(request,user)
#                         return redirect('datanalyse:home')
#             return render(request,self.template_name,{"form":fomr})
