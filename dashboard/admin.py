from django.contrib import admin

# Register your models here.
from .models import Balance
from .models import BalanceRecord
from .models import Post
admin.site.register(Balance)
admin.site.register(BalanceRecord)
admin.site.register(Post)