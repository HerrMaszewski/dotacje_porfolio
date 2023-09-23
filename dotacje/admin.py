from django.contrib import admin
from .models import Institution, Category

admin.site.register(Category)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    search_fields = ('name', 'description')
    list_filter = ('type', 'categories')
    filter_horizontal = ('categories',)


admin.site.register(Institution, InstitutionAdmin)
