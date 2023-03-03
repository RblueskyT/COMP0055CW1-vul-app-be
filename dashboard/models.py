from django.db import models

class Balance(models.Model):
    username = models.CharField(max_length=200)
    current_balance = models.IntegerField(default=100)
    
    def __str__(self):
        return self.username + str(self.current_balance)
    
class BalanceRecord(models.Model):
    username = models.CharField(max_length=200)
    balance_change = models.IntegerField(default=0)
    change_reason = models.CharField(max_length=1000)
    change_date = models.DateTimeField('date changed')
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    