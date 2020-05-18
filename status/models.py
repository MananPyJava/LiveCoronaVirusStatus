from django.db import models

# Create your models here.
class CoronaVirusStatus(models.Model):
    country = models.CharField(max_length=15, unique=True)
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    time = models.TimeField(auto_now=True)
    oldinf = []
    def __str__(self):
        return f"{self.country} =  i:{self.infected}, d:{self.deaths}, r:{self.recovered}"