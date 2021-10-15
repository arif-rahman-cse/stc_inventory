from django.contrib import admin

# Register your models here.
from stock.models import LC, Stock

admin.site.register(LC)
admin.site.register(Stock)