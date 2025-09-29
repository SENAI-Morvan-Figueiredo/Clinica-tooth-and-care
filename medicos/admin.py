from django.contrib import admin
from .models import Medico, Especialidade

# Register your models here.
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf', 'rg', 'crm', 'telefone', 'get_especialidades']
    search_fields = ['nome', 'email', 'cpf', 'rg', 'crm']

    fieldsets = (
        ('Informações pessoais', {
            'fields': ('nome', 'cpf', 'rg', 'crm')
        }),
        (('Contato'), {
            'fields': ('email', 'telefone')
        }),
        (('Outros'), {
            'fields': ('especialidades',)
        })
    )

    def get_especialidades(self, obj):
        return ", ".join([esp.nome for esp in obj.especialidades.all()])

    get_especialidades.short_description = "Especialidades"

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']