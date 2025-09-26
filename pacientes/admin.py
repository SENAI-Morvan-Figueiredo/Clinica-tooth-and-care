from django.contrib import admin
from .models import Paciente

# Register your models here.
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'rg', 'email', 'telefone', 'data_nasc', 'genero', 'endereco']
    list_filter = ['genero']
    search_fields = ['nome', 'cpf', 'rg', 'email']

    fieldsets = (
        ('Informações pessoais', {
            'fields': ('nome', 'cpf', 'rg', 'data_nasc', 'genero')
        }),
        ('Contato', {
            'fields': ('email', 'telefone')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        })
    )