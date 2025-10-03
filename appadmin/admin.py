from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from pacientes.admin import PacienteInline
from medicos.admin import MedicoInline

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    # Aqui, a seção do Paciente e médico aparecerá junto com o user no painel
    inlines = (PacienteInline, MedicoInline)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
finally:
    admin.site.register(User, CustomUserAdmin)