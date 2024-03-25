from django.contrib import admin
from events.models import Bookings, UserProfile, Packages , Contact

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'class_name', 'prn_number')

@admin.register(Packages)
class packageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'venue', 'theme', 'games', 'cards', 'gifts', 'food')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','package','options', 'name', 'class_year', 'department', 'mobile_number', 'datetime', 'created_at')

