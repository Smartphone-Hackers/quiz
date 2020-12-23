"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view(), name="login"),
    path('register', views.Register.as_view(), name="register"),
    path('home', views.Home.as_view(), name="home"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('start-quiz', views.StartQuiz.as_view(), name="start-quiz"),
    path('submit-test', views.SubmitTest.as_view(), name="submit-test"),
    path('try-again', views.TryAgain.as_view(), name="try-again"),
    path('results', views.YourQuizResult.as_view(), name="results"),
    # API
    path('api/question/<int:pk>', views.QuestionAnswerAPI.as_view(), name="api-question"),
    
]
