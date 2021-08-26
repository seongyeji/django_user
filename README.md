Django_Form, User
=============
멋쟁이 사자처럼 스터디 **django Form, User** 복습을 위해 작성한 repository입니다.   
***
# 1. Form
장고에서는 Form을 제공해준다.
Form은 입력공간을 뜻하며, html에서 사용하는 <form>태그를 생각하면 쉽다.

우리가 얻고자 하는 내용을 form태그안에 있는 input에 담아서 DB로 전송시켜준다.
form태그와 DB에 있는 형식과 다르면 **충돌**이 일어나게 된다.

만약 기존 회원가입에서 id와 password만 받았다고 가정했을 때,
회원관리를 위해 이름을 함께 받고자 한다면

1. html에서 이름을 담는 ```<input type="text" name="name"></input>```을 추가
2. DB를 나타내는 models.py에 ```writer = models.CharField(max_length=100)```을 추가
3. views.py에 ```new_user.name = req.POST['name']```을 추가

총 세번의 수정을 거쳐야한다.

**하지만 forms.py를 사용한다면?**
DB의 모델이 변화할때마다 하나씩 변경하지 않아도 된다.
(+ 유효성 검사)
## 1.1. crud app에 forms.py추가
```
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'writer', 'body']

```

모델(Blog)에 있는 필요한 fields들을 가져와 준다.
(pub_date는 form으로 관리할 필요가 없으므로 제외한다.)


## 1.2. views.py
```
from .forms import BlogForm

def create(req):
    if req.method =="POST":
        new_blog = Blog()
        new_blog.title = req.POST['title']
        new_blog.writer = req.POST['writer']
        new_blog.pub_date = timezone.now()
        new_blog.body = req.POST['body']
        new_blog.save()
        return redirect('detail', str(new_blog.id))
    else :
        form = BlogForm()
        return render(req, 'new.html', {'form':form})
```


## 1.3. new.html
```    
<form action="{% url 'create' %}" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```

그 이후 출력 후 확인해본다.
태그에 감싸고 싶다면 다음과 같이 선언해주면 된다.

- {{form.as_p}} p태그에 감싸기
- {{form.as_table}} table태그에 감싸기

## 1.4. views.py
```
def create(req):
    if req.method =="POST":
        form = BlogForm(req.POST, req.FILES)
        if form.is_valid:
            new_blog = form.save(commit = False)
            new_blog.pub_date = timezone.now()
            new_blog.save()
            return redirect('detail', str(new_blog.id))
        return redirect('home')
    else :
        form = BlogForm()
        return render(req, 'new.html', {'form':form})
```

form = BlogForm(req.POST, req.FILES)
> form에 담아준다.
if form.is_valid:
>form에 있는 내용이 유효하다면
new_blog = form.save(commit = False)
>new_blog에 임시저장해준다.
new_blog.pub_date = timezone.now()
>pub_date를 담아준다.
new_blog.save()
>DB에 저장한다.
return redirect('detail', str(new_blog.id))
>detail로 이동한다.

return redirect('home')
>유효성 검사에 실패해서 작성에 실패했을 경우 홈으로 이동한다.


# 2. 기본 login 만들기
user를 만들어서 이용자에게 맞는 페이지를 제공한다.
>admin페이지에 있는 user를 확인할 수 있다.
장고에서 제공해주는 user를 이용하여 쉽게 만들어보자.
## 2.1. account app 만들기
회원정보를 관리할 app을 만든다.

```python manage.py startapp account```

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crud.apps.CrudConfig',
    'account',
]
```


## 2.2. account/views.py
장고에서 기본제공하는 내용을 이용해서 만들어보자

```
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(req):
    form = AuthenticationForm()
    return render(req, 'login.html', {'form':form})
```

AuthenticationForm - 인증
UserCreationForm - 회원가입

원리는 form.py와 동일하다.

django.contrib.auth에 있는 login을 가져와 사용할 예정이므로 우리가 만들어준 login은 login_view로 사용한다.


## 2.3. urls.py
account에 urls.py를 만들어준다.

```
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
]
```

blog의 urls.py에 include 시켜준다.
```
from django.urls import path,include

urlpatterns = [
    path('account/', include('account.urls'))
]
```


## 2.4. account/templates/login.html
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>로그인페이지</title>
</head>
<body>
    <h1>login</h1>
    <form action="{% url 'login_view' %}" method="POST">
        {% csrf_token %}
    {{form.as_p}}
    <input type="submit">
    </form>
</body>
</html>
```

home.html에 링크를 연결해준다.
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>blog</title>
</head>
<body>
    <h1>blog Project</h1>
    <a href="{% url 'create' %}">Write</a>
    <a href="{% url 'login' %}">login</a>
    
    {% for blog in blogs %}
    <div>
        <h3>
            {{blog.title}}
        </h3>
        {{blog.pub_date}}
        <br>
        {{blog.wirter}}
        <br>
        {{blog.summary}}
        <a href="{% url 'detail' blog.id %}">...more</a>
    </div>
    {% endfor %}
    
</body>
</html>
```

## 2.5. views.py
로그인 및 로그아웃을 시켜주는 함수를 만든다.

```
from django.contrib.auth import authenticate,login,logout

def login_view(req):
    if req.method == "POST":
        form = AuthenticationForm(request=req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request=req, username=username, password=password)
            if user is not None:
                login(req, user)
        return redirect("home")
    else : 
        form = AuthenticationForm()
        return render(req, 'login.html', {'form':form})

def logout_view(req):
    logout(req)
    return redirect("home")
```

authenticate 인증해준다.


## 2.7. urls.py

```
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
```

## 2.8. home.html 추가하기
```
{% if user.is_authenticated %}
    <a href="{% url 'logout' %}">logout</a>
    {{user.username}}
{% else %}
    <a href="{% url 'login' %}">login</a>
{% endif %}
```


# 3. 회원가입 만들기
## 3.1. views.py 및 urls.py 추가
```
def regiseter_view(req):
    form = UserCreationForm()
    return render(req, 'signup.html', {'form':form})
```

```
    path('register/', regiseter_view, name="register"),
```


## 3.2. signup.html 만들기

```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>회원가입페이지</title>
</head>
<body>
    <h1>signup</h1>
    <form action="{% url 'register' %}" method="POST">
        {% csrf_token %}
    {{form.as_p}}
    <input type="submit">
    </form>
</body>
</html>
```

home.html과 연결해준다.

```
{% if user.is_authenticated %}
    <a href="{% url 'logout' %}">logout</a>
    {{user.username}}
{% else %}
    <a href="{% url 'login' %}">login</a>
    <a href="{% url 'register' %}">register</a>
{% endif %}
```

## 3.3. views.py 수정하기
```
def regiseter_view(req):
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
        return redirect("home")
    else : 
        form = UserCreationForm()
        return render(req, 'signup.html', {'form':form})
```


# 4. User 확장
## 4.1. models.py
```
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=100)
    university = models.CharField(max_length=50)
```

## 4.2. settings.py
새로운 모델로 사용하겠다고 settings.py에서 알려주기

```
AUTH_USER_MODEL = 'account.CustomUser'
```

## 4.3. makemigrations
```
python manage.py makemigrations
python manage.py migrate
```

migrate에서 **오류가 발생**한다.
admin에 문제가 발생했기때문에 settings.py, urls.py에 있는 admin을 주석처리한다.

## 4.4. form.py
```
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'password1', 'nickname', 'university']
```

## 4.5. views.py
```
from .forms import RegisterForm

def regiseter_view(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
        return redirect("home")
    else : 
        form = RegisterForm()
        return render(req, 'signup.html', {'form':form})
```

## 4.6. home.html
```
    {% if user.is_authenticated %}
        <a href="{% url 'logout' %}">logout</a>
        안녕하세요. {{user.university}}{{user.nickname}}님
    {% else %}
        <a href="{% url 'login' %}">login</a>
        <a href="{% url 'register' %}">register</a>
    {% endif %}
```

## 4.7. admin.py
```
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
```