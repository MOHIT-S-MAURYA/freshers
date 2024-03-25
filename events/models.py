from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    class_choice = (
        ('UG-SY', 'UG - SY'),
        ('UG-TY', 'UG - TY'),
        ('UG-FY', 'UG - FY'),
        ('PG-SY', 'PG - SY')
    )
    class_name = models.CharField(max_length=10, choices=class_choice)
    prn_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Packages(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    venue = models.TextField(max_length=1000)
    theme = models.TextField(max_length=1000)
    games = models.TextField(max_length=1000)
    cards = models.TextField(max_length=1000)
    gifts = models.TextField(max_length=1000)
    food = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=2000)
    
    def __str__(self):
        return self.name
    
    
class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Packages, on_delete=models.CASCADE)
    options = models.JSONField()
    name = models.CharField(max_length=100)
    class_year = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking for {self.package.name}'
