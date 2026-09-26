from django.contrib import admin
from .models import Expense, Category
from .models import UserIncome, IncomeSource
# Register your models here.


admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(UserIncome)
admin.site.register(IncomeSource)