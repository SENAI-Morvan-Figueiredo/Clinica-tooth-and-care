from django.contrib import admin
from .models import Paciente

# Register your models here.
class PacienteInline(admin.StackedInline):
    model = Paciente
    can_delete = False
    verbose_name_plural = 'Informações do Paciente'
    
    # Dentro do Inline, você pode organizar os campos do Paciente:
    fieldsets = (
        ('Detalhes do Paciente', {
            'fields': ('cpf', 'rg', 'telefone', 'data_nasc', 'genero', 'endereco')
        }),
    )

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'cpf', 'rg', 'data_nasc', 'user__email']
    list_filter = ['genero']
    search_fields = ['cpf', 'rg', 'user__username', 'user__last_name']
