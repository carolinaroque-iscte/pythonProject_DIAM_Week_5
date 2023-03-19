
from django.urls import include
from . import views
from django.urls import path

app_name = 'votacao'

urlpatterns = [
     #ex: votacao/
     path("", views.index, name="index"),
     # ex: votacao/1
     path('<int:questao_id>', views.detalhe, name='detalhe'),
     # ex: votacao/3/resultados
     path('<int:questao_id>/resultados', views.resultados, name='resultados'),
     # ex: votacao/5/voto
     path('<int:questao_id>/voto', views.voto, name='voto'),
     path('cria_questao', views.cria_questao, name='cria_questao'),
     path('cria_opcao', views.cria_opcao, name='cria_opcao'),
     path('<int:questao_id>/inserir_opcao', views.inserir_opcao, name='inserir_opcao'),
     path('<int:questao_id>/inserir_questao', views.inserir_questao, name='inserir_questao'),
]