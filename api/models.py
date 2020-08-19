from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=256)
    done = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tasks', null=True)
    last_active = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} / {1}".format(self.title, "DONE" if self.done else "NOT DONE")


class CustomUser(AbstractUser):
    active_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    companies = models.ManyToManyField(Company, related_name='staff', blank=True)
