from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_users = models.IntegerField(default=0)
    max_users = models.IntegerField(default=0)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if isinstance(self.start_date, str):
            self.start_date = timezone.make_aware(datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S'),
                                                  timezone.get_default_timezone())
        super().save(*args, **kwargs)


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    video_link = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    objects = models.Manager()


class Group(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)
    objects = models.Manager()
