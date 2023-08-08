from django.contrib import admin

from .models import EcsInstance, WafInstance

# Register your models here.
admin.site.register(EcsInstance)
admin.site.register(WafInstance)
