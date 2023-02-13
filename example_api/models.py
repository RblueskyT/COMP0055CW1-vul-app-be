from django.db import models

class ExampleModel(models.Model):
    username = models.CharField(max_length=50)
    time_created = models.DateTimeField()

    def __str__(self):
        return (self.username, self.time_created)
