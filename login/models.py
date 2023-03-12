from django.db import models

# Create your models here.
class UserStatus(models.Model):
    username = models.CharField(max_length=100)
    isLoggedIn = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

