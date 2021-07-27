from django.contrib import admin
from .models import user_details,login,products,cart_contents,checkout
# Register your models here.
admin.site.register(user_details)
admin.site.register(login)
admin.site.register(products)
admin.site.register(cart_contents)
admin.site.register(checkout)