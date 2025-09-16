from django.contrib import admin

# Register your models here.
from .models import Movie, Review
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ('name', 'price', 'amount_left')
    fields = ('name', 'price', 'description', 'image', 'amount_left')

    def get_readonly_fields(self, request, obj=None):
        # Admin can always edit amount_left (to restock). When a movie has
        # amount_left == 0, prevent editing other product fields to avoid
        # accidental modifications while out of stock.
        if obj is None:
            return []
        amount_left = getattr(obj, 'amount_left', None)
        try:
            if amount_left is not None and int(amount_left) <= 0:
                return ('name', 'price', 'description', 'image')
        except Exception:
            pass
        return []
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)


