from django.contrib import admin
from page_app.models import Books

# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['name']
