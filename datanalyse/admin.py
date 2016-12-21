from django.contrib import admin
from datanalyse.models import UserPorts,UserMoney,TickerComp,BuyStockTable
# Register your models here.

admin.site.register(UserPorts)
admin.site.register(UserMoney)
admin.site.register(TickerComp)
admin.site.register(BuyStockTable)
