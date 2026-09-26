from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model) :
    amount=models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
    category=models.CharField(max_length=266)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']

class Category(models.Model) :
    name=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name

class IncomeSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural : 'Incoming sources'

    def __str__(self):
        return self.name

class UserIncome(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    name = models.ForeignKey(IncomeSource, on_delete=models.SET_NULL, null=True, blank=True) # Diubah jadi relasi ForeignKey

    def __str__(self):
        return str(self.name)