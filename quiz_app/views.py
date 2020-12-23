from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, SignInForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import QuestionAnswerModel, TimeCalulate, StudentQuizResult
from rest_framework.response import Response
from rest_framework.views import APIView
from quiz_app import serializers
from datetime import datetime, timedelta
import requests

# Create your views here.
class Login(View):
    template_name = "login.html"
    def get(self, request):
        signin = SignInForm()
        datas = {
            'form': signin,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        # signin = SignInForm(request.POST)
        signin = AuthenticationForm(request=request, data=request.POST)
        if signin.is_valid():
            username = signin.cleaned_data['username']
            password = signin.cleaned_data['password']
            chk_user = User.objects.filter(username=username)
            
            if chk_user:    
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f'Welcome {username}')
                    return redirect('/home')
                return redirect('/')
        
        form = SignInForm()
        datas = {'form_error': signin.errors.as_text(), 'form': form}
        print(datas)
        return render(request, template_name=self.template_name, context=datas)
        
class Logout(View):
    def get(self, request):
        qna = QuestionAnswerModel.objects.filter(username=request.user.username).delete()
        logout(request)
        return redirect('/')

class Register(View):
    template_name = "register.html"
    def get(self, request):
        signup = SignUpForm()
        datas = {
            'form': signup
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        signup = SignUpForm(request.POST)
        if signup.is_valid():
            username = signup.cleaned_data['username']
            email = signup.cleaned_data['email']
            password = signup.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.info(request, f'Welcome {username}, You Are Register Successfully')
            return redirect('/register')
        datas = {'form': signup,}
        return render(request, template_name=self.template_name, context=datas)

class Home(View):
    template_name = 'home.html'
    def get(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        datas = {
            'username': str(username).capitalize(),
            'auth': request.user.is_authenticated,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        username = request.user.username

        trivia_url = f'https://opentdb.com/api.php?amount=3&category={category}&difficulty={difficulty}&type=multiple'
        trivia_result = requests.get(trivia_url).json()
        trivia_result = trivia_result['results']
        cnt = 0
        if trivia_result:
            for trivia in trivia_result:
                options = trivia['incorrect_answers']
                options.append(trivia['correct_answer'])
                category_num = {
                    9: 'General Knowledge',
                    10: 'Books',
                    11: 'Films',
                }
                qna = QuestionAnswerModel(username=username, category=category_num[int(category)],
                      difficulty=difficulty, question=trivia['question'],
                      correct_answer=trivia['correct_answer'], options=options)
                qna.save()
                cnt += 1
                if cnt == 1:
                    tc = TimeCalulate(username=qna, start_time=datetime.today(),
                                         end_time=datetime.today())
                    tc.save()
        return redirect('/start-quiz')

class StartQuiz(View):
    template_name = "quiz.html"
    def get(self, request):
        page = request.GET.get('page')
        question_answer = QuestionAnswerModel.objects.filter(username=request.user.username)

        pagination = Paginator(question_answer, 1)
        
        try:
            question = pagination.page(page)
        except PageNotAnInteger:
            question = pagination.page(1)
        except EmptyPage:
            question = pagination.page(pagination.num_pages)
        
        datas = {
            'question_page': question,
            'username': str(request.user.username).capitalize(),
            'auth': request.user.is_authenticated,
        }
        
        return render(request, template_name=self.template_name, context=datas)

class QuestionAnswerAPI(APIView):
    def get(self, request, pk):
        qna = QuestionAnswerModel.objects.get(id=pk)
        serializer = serializers.QuestionAnswerSerializer(qna)
        return Response(serializer.data)
    
    def put(self, request, pk):
        qna = QuestionAnswerModel.objects.get(id=pk)
        serializer = serializers.QuestionAnswerSerializer(qna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class SubmitTest(View):
    template_name = 'submit_test.html'
    def wrong_right_result(self,):
        total_questions = QuestionAnswerModel.objects.all().count()
        qna = QuestionAnswerModel.objects.all()
        right_answer = 0
        wrong_answer = 0
        for q in qna:
            if q.correct_answer == q.click_data:
                right_answer += 1
            else:
                wrong_answer += 1
        return (total_questions, right_answer, wrong_answer)

    def get(self, request):
        qna = QuestionAnswerModel.objects.filter(username=request.user.username).first()
        tc = TimeCalulate.objects.get(username=qna)
        tc.end_time = datetime.today()
        tc.save()
        
        tcal = TimeCalulate.objects.get(username=qna)
        # print(tcal.start_time.time().hour)
        t1 = timedelta(hours=tcal.start_time.time().hour, minutes=tcal.start_time.time().minute,
                        seconds=tcal.start_time.time().second)
        t2 = timedelta(hours=tcal.end_time.time().hour, minutes=tcal.end_time.time().minute,
                        seconds=tcal.end_time.time().second)
        
        total_seconds = t2 - t1

        total_questions, right_answer, wrong_answer = self.wrong_right_result()
        
        student = StudentQuizResult(username=request.user.username, topic=qna.category, 
                    total_time=total_seconds, total_questions=10, right_answer=right_answer,
                    wrong_answer=wrong_answer)
        student.save()

        datas = {
            'auth': request.user.is_authenticated,
            'username': str(request.user.username).capitalize(),
            'total_time': total_seconds,
            'total_questions': total_questions,
            'right_answer': right_answer,
            'wrong_answer': wrong_answer,
            }

        return render(request, template_name=self.template_name, context=datas)

class TryAgain(View):
    def get(self, request):
        qna = QuestionAnswerModel.objects.filter(username=request.user.username).delete()
        return redirect('/home')

class YourQuizResult(View):
    template_name = 'your_quiz_results.html'
    def get(self, request):
        results = StudentQuizResult.objects.filter(username=request.user.username)
        datas = {
            'results': results,
            'username': str(request.user.username).capitalize(),
            'auth': request.user.is_authenticated,
        }
        return render(request, template_name=self.template_name, context=datas)