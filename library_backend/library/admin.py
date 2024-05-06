from django.contrib import admin
from library.models import User,Book


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","password","user_type"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name","author","publication_year"]
