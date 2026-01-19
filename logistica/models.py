from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('ADMIN', 'Administrador'),
        ('OPERADOR', 'Operador Logístico'),
        ('MOTORISTA', 'Motorista'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='OPERADOR')
    telefone = models.CharField(max_length=20, blank=True, null=True)

class Veiculo(models.Model):
    placa = models.CharField(max_length=8, unique=True)
    modelo = models.CharField(max_length=50)
    capacidade_kg = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    cnh = models.CharField(max_length=20, unique=True)
    validade_cnh = models.DateField()
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfil_motorista')

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.TextField()

    def __str__(self):
        return self.razao_social

class Entrega(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('EM_TRANSITO', 'Em Trânsito'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    )

    codigo_rastreio = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    data_saida = models.DateTimeField(null=True, blank=True)
    data_chegada_prevista = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entrega {self.codigo_rastreio} - {self.status}"