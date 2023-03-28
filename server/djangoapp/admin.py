from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


admin.site.register(CarModel)
admin.site.register(CarMake, CarMakeAdmin)
