from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404, request
from django.shortcuts import render, get_object_or_404, redirect, render_to_response, reverse
from django.db.models import Q
from . forms import *
from .models import *
import datetime
from django.template import RequestContext, loader
from difflib import SequenceMatcher
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        answers = question.answer_set.all()
        score = question.get_score()
        form = AnswerForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                answer = Answer()
                answer.answer_text = form.data['answer_text']
                answer.author = request.user
                answer.answer_time = datetime.datetime.now()
                answer.question = question
                answer.save()
                form = AnswerForm()
                return render(request, 'html_pages/detail.html', {'score': score,
                                                                  'question_title': question.question_title,
                                                                  'question_content': question.question_content,
                                                                  'sub_code': question.sub_code,
                                                                  'answers': answers,
                                                                  'form': form
                                                                  })
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'html_pages/detail.html', {'score': score,
                                                      'question_title': question.question_title,
                                                      'question_content': question.question_content,
                                                      'sub_code': question.sub_code,
                                                      'answers': answers,
                                                      'form': form
                                                      })


def vote_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    form = QuestionVotesForm()
    previous_page = request.META['HTTP_REFERER']

    if request.method == 'POST':
        form = QuestionVotesForm(request.POST)
        if form.is_valid():
            qv = QuestionVotes()
            qv.user = request.user
            qv.question = question
            qv.val = form.data['val']
            if not QuestionVotes.objects.filter(question=qv.question, user=qv.user):
                qv.save()
            else:
                existing_votes = QuestionVotes.objects.filter(question=question, user=qv.user)
                for vote in existing_votes:
                    vote.delete()
                qv.save()
            return HttpResponseRedirect('/' + question_id)
    return render(request, template_name='html_pages/vote_question.html', context={
            'question_id': question_id,
            'question_title': question.question_title,
            'question_content': question.question_content,
            'score': question.get_score(),
            'form': form,
            'previous_page': previous_page,
            })


def vote_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    form = AnswerVotesForm()
    current_score = answer.get_score()

    if request.method == 'POST':
        form = AnswerVotesForm(request.POST)
        if form.is_valid():
            answ = AnswerVotes()
            answ.user = request.user
            answ.ans = answer
            answ.val = form.data['val']
            if not AnswerVotes.objects.filter(ans=answer, user=answ.user):
                answ.save()
            else:
                existing_votes = AnswerVotes.objects.filter(ans=answer, user=answ.user)
                for vote in existing_votes:
                    vote.delete()
                answ.save()
            return HttpResponseRedirect('/' + str(answer.question.id))
    return render(request, template_name='html_pages/vote_answer.html', context={
            'question': answer.question,
            'answer': answer,
            'score': current_score,
            'form': form
            })
# ------------------------------------------------------------------------------------------------------------------


def TDT4140_a(request):
    sub_code = 'TDT4140'
    # connecter til databasen
    all_questions_with_sub_code = Question.objects.filter(sub_code = sub_code)
    context = {
        'all_questions_with_sub_code': all_questions_with_sub_code,
    }
    return render(request, 'courses/TDT4140_a.html', context=context)

def TDT4110_a(request):
    sub_code = 'TDT4110'
    # connecter til databasen
    all_questions_with_sub_code = Question.objects.filter(sub_code = sub_code)
    context = {
        'all_questions_with_sub_code': all_questions_with_sub_code,
    }
    return render(request, 'courses/TDT4110_a.html', context=context)

def TDT4145_a(request):
    sub_code = 'TDT4145'
    # connecter til databasen
    all_questions_with_sub_code = Question.objects.filter(sub_code = sub_code)
    context = {
        'all_questions_with_sub_code': all_questions_with_sub_code,
    }
    return render(request, 'courses/TDT4145_a.html', context=context)

def TDT4180_a(request):
    sub_code = 'TDT4180'
    # connecter til databasen
    all_questions_with_sub_code = Question.objects.filter(sub_code = sub_code)
    context = {
        'all_questions_with_sub_code': all_questions_with_sub_code,
    }
    return render(request, 'courses/TDT4180_a.html', context=context)


def TTM4100_a(request):
    sub_code = 'TTM4100'
    # connecter til databasen
    all_questions_with_sub_code = Question.objects.filter(sub_code = sub_code)
    context = {
        'all_questions_with_sub_code': all_questions_with_sub_code,
    }
    return render(request, 'courses/TTM4100_a.html', context=context)

def TTM4100_b(request):
    sub_code = 'TTM4100'
    all_questions_with_sub_code = Question.objects.filter(sub_code=sub_code)
    similar_questions = []

    a = Question.objects.filter(sub_code=sub_code).latest('ask_time')
    a_content = a.question_content

    for questions in all_questions_with_sub_code:
        b = questions.question_content

        likhet = SequenceMatcher(None, a_content, b).ratio()
        if likhet >= 0.5:
            similar_questions.append(questions)

    context = {
        'similar_questions': similar_questions
    }

    return render(request, 'courses/TTM4100_b.html', context)

def TDT4110_b(request):
    sub_code = 'TDT4110'
    all_questions_with_sub_code = Question.objects.filter(sub_code=sub_code)
    similar_questions = []

    a = Question.objects.filter(sub_code=sub_code).latest('ask_time')
    a_content = a.question_content

    for questions in all_questions_with_sub_code:
        b = questions.question_content

        likhet = SequenceMatcher(None, a_content, b).ratio()
        if likhet >= 0.5:
            similar_questions.append(questions)

    context = {
        'similar_questions': similar_questions
    }

    return render(request, 'courses/TDT4110_b.html', context)

def TDT4140_b(request):
    sub_code = 'TDT4140'
    all_questions_with_sub_code = Question.objects.filter(sub_code=sub_code)
    similar_questions = []

    a = Question.objects.filter(sub_code=sub_code).latest('ask_time')
    a_content = a.question_content

    for questions in all_questions_with_sub_code:
        b = questions.question_content

        likhet = SequenceMatcher(None, a_content, b).ratio()
        if likhet >= 0.5:
            similar_questions.append(questions)

    context = {
        'similar_questions': similar_questions
    }

    return render(request, 'courses/TDT4140_b.html', context)

def TDT4145_b(request):
    sub_code = 'TDT4145'
    all_questions_with_sub_code = Question.objects.filter(sub_code=sub_code)
    similar_questions = []

    a = Question.objects.filter(sub_code=sub_code).latest('ask_time')
    a_content = a.question_content

    for questions in all_questions_with_sub_code:
        b = questions.question_content

        likhet = SequenceMatcher(None, a_content, b).ratio()
        if likhet >= 0.5:
            similar_questions.append(questions)

    context = {
        'similar_questions': similar_questions
    }

    return render(request, 'courses/TDT4145_b.html', context)

def TDT4180_b(request):
    sub_code = 'TDT4180'
    all_questions_with_sub_code = Question.objects.filter(sub_code=sub_code)
    similar_questions = []

    a = Question.objects.filter(sub_code=sub_code).latest('ask_time')
    a_content = a.question_content

    for questions in all_questions_with_sub_code:
        b = questions.question_content

        likhet = SequenceMatcher(None, a_content, b).ratio()
        if likhet >= 0.5:
            similar_questions.append(questions)

    context = {
        'similar_questions': similar_questions
    }

    return render(request, 'courses/TDT4180_b.html', context)


def TDT4140_q(request):
    sub_code = 'TDT4140'
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.question_title = form.data['question_title']
            question.question_content = form.data['question_content']
            question.sub_code = sub_code
            question.author = request.user
            question.ask_time = datetime.datetime.now()
            question.save()
            return redirect("../../TDT4140_b")
        """""
        question.question_title= form.question_title.save_form_data()
        question.question_content = form.question_content
        return redirect('/music/')
        """""
    return render(request, 'courses/TDT4140_q.html', {'form': form})

def TDT4110_q(request):
    sub_code = 'TDT4110'
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.question_title = form.data['question_title']
            question.question_content = form.data['question_content']
            question.sub_code = sub_code
            question.author = request.user
            question.ask_time = datetime.datetime.now()
            question.save()
            return redirect("../../TDT4110_b")
        """""
        question.question_title= form.question_title.save_form_data()
        question.question_content = form.question_content
        return redirect('/music/')
        """""
    return render(request, 'courses/TDT4110_q.html', {'form': form})

def TDT4145_q(request):
    sub_code = 'TDT4145'
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.question_title = form.data['question_title']
            question.question_content = form.data['question_content']
            question.sub_code = sub_code
            question.author = request.user
            question.ask_time = datetime.datetime.now()
            question.save()
            return redirect("../../TDT4145_b")
        """""
        question.question_title= form.question_title.save_form_data()
        question.question_content = form.question_content
        return redirect('/music/')
        """""
    return render(request, 'courses/TDT4145_q.html', {'form': form})

def TDT4180_q(request):
    sub_code = 'TDT4180'
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.question_title = form.data['question_title']
            question.question_content = form.data['question_content']
            question.sub_code = sub_code
            question.author = request.user
            question.ask_time = datetime.datetime.now()
            question.save()
            return redirect("../../TDT4180_b")
        """""
        question.question_title= form.question_title.save_form_data()
        question.question_content = form.question_content
        return redirect('/music/')
        """""
    return render(request, 'courses/TDT4180_q.html', {'form': form})

def TTM4100_q(request):
    sub_code = 'TTM4100'
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = Question()
            question.question_title = form.data['question_title']
            question.question_content = form.data['question_content']
            question.sub_code = sub_code
            question.author = request.user
            question.ask_time = datetime.datetime.now()
            question.save()
            return redirect("../../TTM4100_b")
        """""
        question.question_title= form.question_title.save_form_data()
        question.question_content = form.question_content
        return redirect('/music/')
        """""
    return render(request, 'courses/TTM4100_q.html', {'form': form})

def about(request):
    if not request.user.is_authenticated():
        return render(request, 'html_pages/login.html')
    else:
        return render(request, 'html_pages/about.html')


def ask(request):
    if not request.user.is_authenticated():
        return render(request, 'html_pages/login.html')
    else:
        return render(request, 'html_pages/ask.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'html_pages/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'html_pages/ask.html')
            else:
                return render(request, 'html_pages/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'html_pages/login.html', {'error_message': 'Invalid login'})
    return render(request, 'html_pages/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'html_pages/login.html')
    context = {
        "form": form,
    }
    return render(request, 'html_pages/register.html', context)


def answer(request):
    if not request.user.is_authenticated():
        return render(request, 'html_pages/login.html')
    else:
        return render(request, 'html_pages/answer.html')
