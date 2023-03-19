
from django.template import loader
from .models import Questao, Opcao
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    #template = loader.get_template('votacao/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)

def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request,
                  'votacao/resultados.html',
                  {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])

    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção", })
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
        return HttpResponseRedirect(
            reverse('votacao:resultados',
                    args=(questao.id,)))

def cria_questao(request):
    return render(request, 'votacao/cria_questao.html')

def cria_opcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/cria_opcao.html', {
        'questao': questao,
        'error_message': "Não criou uma opção", })

def inserir_questao(request):
    if not request.POST['questao_texto']:
        return render(request, 'votacao/criar_questao.html', {'error_message': 'Algo correu mal, por favor insira a sua questão.'})
    else:
        Questao(questao_texto=request.POST['questao_texto'])
        return HttpResponseRedirect(reverse('votacao:index'))


def inserir_opcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_selecionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo form para vota
        return render(request, 'votacao/criar_opcao.html', {'questao': questao, 'error_message': 'Opcão não válida.'})
    else:
        the_question= Questao.objects.get(pk=questao_id)
        the_question.opcao_set.create(opcao_texto=request.POST['opcao_texto'], votos=0)
        return HttpResponseRedirect(reverse('votacao:index'))