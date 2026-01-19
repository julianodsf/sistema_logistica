from django.contrib import admin
from .models import Usuario, Veiculo, Motorista, Cliente, Entrega

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('codigo_rastreio', 'cliente', 'status', 'data_chegada_prevista')
    list_filter = ('status', 'data_saida')
    search_fields = ('codigo_rastreio', 'cliente__razao_social')

admin.site.register(Usuario)
admin.site.register(Veiculo)
admin.site.register(Motorista)
admin.site.register(Cliente)