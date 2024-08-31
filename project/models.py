from django.db import models

# Create your models here.
class Setting(models.Model):
    name = models.CharField(max_length=200)
    _type = models.CharField(max_length=100, null=True, blank=True)
    v = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.name}"