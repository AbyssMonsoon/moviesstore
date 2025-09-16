from django.contrib import admin

# Register your models here.
from .models import Order, Item
class ItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'movie', 'quantity', 'price', 'order')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'total', 'date')

admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)