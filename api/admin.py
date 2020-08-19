from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Company, Task, CustomUser

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'done', 'company', 'last_active', 'created']
    search_fields = ['title', 'company']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'active_company']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Companies', {'fields': ('active_company', 'companies')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
