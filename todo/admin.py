from django.contrib import admin
from .models import Todo,TodoCollection

# Register your models here.
admin.site.register(Todo)
admin.site.register(TodoCollection)