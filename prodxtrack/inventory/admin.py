from django.contrib import admin
from .models import UserProfile, Inventory, Inbound, Outbound


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Inventory)
admin.site.register(Inbound)
admin.site.register(Outbound)