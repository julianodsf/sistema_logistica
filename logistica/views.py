from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import UsuarioCreationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from .models import Entrega, Veiculo, Motorista
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Entrega, Motorista, Veiculo

class EntregaCreateView(LoginRequiredMixin, CreateView):
    model = Entrega
    fields = ['codigo_rastreio', 'cliente', 'motorista', 'veiculo', 'origem', 'destino', 'data_chegada_prevista', 'status']
    template_name = 'logistica/entrega_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nova Ordem de Entrega'
        return context

class MotoristaListView(LoginRequiredMixin, ListView):
    model = Motorista
    template_name = 'logistica/motorista_list.html'
    context_object_name = 'motoristas'

class VeiculoListView(LoginRequiredMixin, ListView):
    model = Veiculo
    template_name = 'logistica/veiculo_list.html'
    context_object_name = 'veiculos'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_entregas'] = Entrega.objects.count()
        context['entregas_pendentes'] = Entrega.objects.filter(status='PENDENTE').count()
        context['entregas_transito'] = Entrega.objects.filter(status='EM_TRANSITO').count()
        context['veiculos_disponiveis'] = Veiculo.objects.filter(disponivel=True).count()

        context['ultimas_entregas'] = Entrega.objects.select_related('cliente', 'motorista').order_by('-criado_em')[:5]
        
        return context

class CadastroUsuarioView(CreateView):
    template_name = 'registration/cadastro.html'
    form_class = UsuarioCreationForm
    success_url = reverse_lazy('login') 

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'