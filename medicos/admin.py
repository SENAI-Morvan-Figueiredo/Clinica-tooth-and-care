from django.contrib import admin
from .models import Medico, Especialidade

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'user__email', 'cpf', 'rg', 'crm', 'telefone', 'get_especialidades']
    search_fields = ['user__username', 'user__email', 'cpf', 'rg', 'crm']

    def get_especialidades(self, obj):
        return ", ".join([esp.nome for esp in obj.especialidades.all()])

    get_especialidades.short_description = "Especialidades"

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class MedicoInline(admin.StackedInline):
    model = Medico
    can_delete = False
    verbose_name_plural = 'Perfil de Médico'
    
    # Define a ordem e agrupamento dos campos do Médico
    fieldsets = (
        ('Detalhes Profissionais', {
            'fields': ('crm', 'especialidades', 'telefone')
        }),
        ('Documentos', {
            'fields': ('cpf', 'rg')
        }),
    )