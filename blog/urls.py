from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('resumo_cripto/', views.resumo_cripto, name='blog-resumo_cripto'),
    path('gera_chaves/', views.gera_chave, name='blog-gera_chaves'),
    path('certificado_digital/', views.certificado_digital, name='blog-certificado_digital'),
    path('listar_cert/', views.listar_cert, name='blog-listar_cert')
]