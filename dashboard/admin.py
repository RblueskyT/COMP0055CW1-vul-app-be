from django.contrib import admin

# Register your models here.
from .models import Balance
from .models import BalanceRecord

admin.site.register(Balance)
admin.site.register(BalanceRecord)