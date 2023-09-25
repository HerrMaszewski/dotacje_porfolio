from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = (
        ('1', 'Fundacja'),
        ('2', 'Organizacja pozarządowa'),
        ('3', 'Lokalna zbiórka'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES, default="1")
    categories = models.ManyToManyField(Category)

    def get_category_ids(self):
        return ",".join([str(category.id) for category in self.categories.all()])

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(default=0, null=False)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    pick_up_date = models.DateField(auto_now_add=True)
    pick_up_time = models.TimeField(auto_now_add=True)
    pick_up_comment = models.TextField(max_length=1024)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
