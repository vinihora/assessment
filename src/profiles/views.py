from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from users.models import *
from profiles.models import *
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def myprofile_view(request):
    profile = Profile.objects.get(user = request.user)
    teams = Teams.objects.filter(user = profile)
    choices = Choice.objects.filter(user=profile.user)
    
    avaliable_avaliations = []

    for team in range(len(teams)):
        for assess in teams[team].avaliations.all():
            avaliable_avaliations.append(assess)
 
    pontuação = []

    for obj in range(len(avaliable_avaliations)):
        avaliation_loop = Avaliation.objects.get(name=avaliable_avaliations[obj])
        filtred_choice = Choice.objects.filter(assess=avaliation_loop)
        soma = 0
        for choice in filtred_choice:
            point = int(choice.choiced)
            soma += point
        pontuação.append(soma)

    print(pontuação)

    context = {
        'profile':profile,
        'teams':teams
    }

    return render(request, 'profiles/myprofile.html', context)

def assessment_view(request, assessment):
    profile = Profile.objects.get(user=request.user)
    assess = Avaliation.objects.get(id=assessment)
    categories = list(assess.category.all())

    questions = []
    for obj in categories:
        category = Category.objects.get(name = obj)
        for quest in category.questions.all():
            questions.append(quest.id)

    exist_quest = False

    if request.method=="POST":
        for i in questions:
            k = request.POST.get(str(i))
            quest = Question.objects.get(id=i)
            actual_choice = Choice(user=profile.user, choiced=k, quest=quest, assess=assess)
            if Choice.objects.filter(quest=quest).exists():
                Choice.objects.get(quest=quest).delete()
                actual_choice.save()
            else:
                actual_choice.save()

    context = {
        'profile':profile,
        'assess':assess,
    }

    return render(request, 'profiles/assessment.html', context)

def results(request):
    profile = Profile.objects.get(user = request.user)
    teams = Teams.objects.filter(user = profile)
    choices = Choice.objects.filter(user=profile.user)
    
    avaliable_avaliations = []

    for team in range(len(teams)):
        for assess in teams[team].avaliations.filter(value="pontuação"):
            avaliable_avaliations.append(assess.name)

    pontuação = []

    for obj in range(len(avaliable_avaliations)):
        avaliation_loop = Avaliation.objects.get(name=avaliable_avaliations[obj])
        filtred_choice = Choice.objects.filter(assess=avaliation_loop)
        soma = 0
        for choice in filtred_choice:
            point = int(choice.choiced)
            soma += point
        pontuação.append(soma)

    number_of_avaliations = []
    for i in range(len(avaliable_avaliations)):
        number_of_avaliations.append(i)
    
    # Numero total de questões por categoria
    questions_total_not_separeted_by_avaliations = []
    for obj in range(len(avaliable_avaliations)):
        avaliation_loop = Avaliation.objects.get(name=avaliable_avaliations[obj])
        questions = 0
        temp = []
        for i,cat in enumerate(avaliation_loop.category.all()):
            questions = cat.questions.count()
            questions_total_not_separeted_by_avaliations.append(questions)

    # print("total de questões na categoria", questions_total_not_separeted_by_avaliations)

    # Numero total de questões por categoria e por avaliations
    questions_total_separeted_by_avaliations = []
    for obj in range(len(avaliable_avaliations)):
        avaliation_loop = Avaliation.objects.get(name=avaliable_avaliations[obj])
        questions = 0
        temp = []
        for i,cat in enumerate(avaliation_loop.category.all()):
            questions = cat.questions.count()
            temp.append(questions)
        questions_total_separeted_by_avaliations.append(temp)

    # print("total de questões nas categorias separdas por avaliações", questions_total_separeted_by_avaliations)

    # Escolha de número máximo
    total_points = []
    for obj in range(len(avaliable_avaliations)):
        avaliation_loop = Avaliation.objects.get(name=avaliable_avaliations[obj])
        temporaria = []
        for cat in avaliation_loop.category.all():
            choice_max = 0
            for choice in cat.choices.all():
                temp = int(choice.ans)
                if temp > choice_max:
                    choice_max = temp
            temporaria.append(choice_max)
        total_points.append(temporaria)

    # print("high choice", total_points)

    # máximo de pontos possíveis a ser feito na categoria
    category_max_points = []
    for i in range(len(total_points)):
        temporaria = []
        for pos,num in enumerate(total_points[int(i)]):
            temporaria.append(questions_total_separeted_by_avaliations[i][pos] * num)
        category_max_points.append(temporaria)

    # print(category_max_points)

    # Categorias dividas por assessment
    avaliable_categories = []

    for team in range(len(teams)):
        for assess in teams[team].avaliations.filter(value="pontuação"):
            avaliable_categories.append(assess.category.all())

    # print(avaliable_categories)

    # numeros de avaliações feitas pelo coolaborador e respectivos nomes
    zipped_avaliations = zip(number_of_avaliations, avaliable_avaliations)
    
    # Pontos feitos pelo coolaborador separado por categoria e avaliação
    teste = {}
    temporaria = {}
    slk = []
    for obj in avaliable_avaliations:
        teste[obj] = []
        avaliation_loop = Avaliation.objects.get(name=obj)
        for num,cat in enumerate(avaliation_loop.category.all()):
            choices_filter = Choice.objects.filter(Q(user=profile.user) & Q(quest=Question.objects.filter(questions__name=cat)))
            temporaria[cat.name] = 0
            soma = 0
            for i in Question.objects.filter(questions__name=cat):
                choices_filter = Choice.objects.filter(quest=i)
                for choice in choices_filter:
                    soma += int(choice.choiced)
            temporaria[cat.name] = soma
        slk.append(list(temporaria.values()))
        temporaria.clear()

    zipped_user_max_points = zip(category_max_points,slk)

    # print(category_max_points)

    # divisao das notas por categoria
    points_divisions_by_category = []
    for index1,assess in enumerate(category_max_points):
        temporaria = []
        for index2,cat in enumerate(assess):
            temporaria2 = []
            for index3 in range(1,4):
                div_by = int(category_max_points[index1][index2]) / 3
                temporaria2.append(int(index3*div_by))
            temporaria.append(temporaria2)
        points_divisions_by_category.append(temporaria)

    zipped2 = enumerate(category_max_points)

    # print(points_divisions_by_category)

    phrases_index = []
    controle = 0
    for index1,obj in enumerate(avaliable_avaliations):
        temp = []
        for index2,points in enumerate(slk[index1]):
            for index3,fronteira in enumerate(points_divisions_by_category[index1][index2]):
                if points <= fronteira:
                    controle = index3
                    break
            temp.append(controle)
        phrases_index.append(temp)
    
    print(phrases_index)
    print(points_divisions_by_category)

    lista_teste = [
        [
        ['RuimHands','MédioHands','ÓtimoHands'],
        ['Ruimcoachable','Mediocoachable','Ótimocoachable'],
        ['Ruimtrouble','Médiotrouble','ÓtimoTrouble']],
        [
        ['RuimEstratégia','MédioEstratégia','ÓtimoEstratégia'],
        ['RuimGestão','MédioGestão','ÓtimoGestão'],
        ['RuimExecução','MédioExecução','ÓtimoExecução']]
        ]
    
    # print(lista_teste)
    
    context = {
        'zipped':zipped_avaliations,
        'number_of_avaliations':number_of_avaliations,
        'avaliable_avaliations':avaliable_avaliations,
        'pontuação':pontuação,
        'profile':profile,
        'teams':teams,
        'choices':choices,
        'questions_total':questions_total_not_separeted_by_avaliations,
        'category_max_points':category_max_points,
        'user_points':slk,
        'zipped_user_max_points':zipped_user_max_points,
        'points_divisions_by_category':points_divisions_by_category,
        'zipped2':zipped2,
        'lista_teste':lista_teste,
        'phrases_index':phrases_index,
        'avaliable_categories':avaliable_categories,
    }
    return render(request, 'profiles/results.html', context)

def assessment_results_view(request):
    profile = Profile.objects.get(user = request.user)
    teams = Teams.objects.filter(user = profile)
    choices = Choice.objects.filter(user=profile.user)
    
    avaliable_avaliations = {}
    categories = []

    for team in range(len(teams)):
        for assess in teams[team].avaliations.filter(value="pontuação"):
            categories = []
            for cat in assess.category.all():
                categories.append(cat.name)
                avaliable_avaliations[assess.name] = categories
    
    teste = {}
    pontuação = {}
    slk = []
    for obj in avaliable_avaliations.keys():
        teste[obj] = []
        avaliation_loop = Avaliation.objects.get(name=obj)
        for num,cat in enumerate(avaliation_loop.category.all()):
            choices_filter = Choice.objects.filter(Q(user=profile.user) & Q(quest=Question.objects.filter(questions__name=cat)))
            pontuação[cat.name] = 0
            soma = 0
            for i in Question.objects.filter(questions__name=cat):
                choices_filter = Choice.objects.filter(quest=i)
                for choice in choices_filter:
                    soma += int(choice.choiced)
            pontuação[cat.name] = soma
        slk.append(list(pontuação.values()))
        pontuação.clear()

    categories = list(avaliable_avaliations.values())
    avaliations = list(avaliable_avaliations.keys())

    return JsonResponse(data={
        'labels':avaliations,
        'categories': categories,
        'data': slk,
    })