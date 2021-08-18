Django_crud
=============
멋쟁이 사자처럼 스터디 **django crud** 복습을 위해 작성한 repository입니다.   
***
# 1. 기본셋팅
## 1.1. 가상환경 만들기
가상환경명은 보통 myvenv나 venv 같은 네이밍을 사용한다.

**WINDOW**
>python -m venv (가상환경명)

**MAC**
>python3 -m venv (가상환경명)

맥은 os자체에 2버전의 파이썬이 내장 되어 있습니다. (3버전 파이썬 사용 권장)
>alias python=‘python3’

기본적으로 사용하는 python을 3로 지정하면 python3라고 쓰지 않아도 괜찮습니다.

## 1.2. 가상환경 실행
.을 사용하여 source를 생략 할 수 있다.

**WINDOW**
> source (가상환경명)/scripts/activate   
. (가상환경명)/scripts/activate

**MAC**
>source (가상환경명)/bin/activate   
. (가상환경명)/bin/activate

성공적으로 실행이 되었다면 터미널 뒤에 (가상환경명)이 나오게 된다.


## 1.3. 장고 설치
가상환경이 켜져 있는 상태에서 설치해준다.

**WINDOW, MAC**
> pip install django

Successfully installed django가 나온다면 설치가 된 것이다.

## 1.4. 블로그 프로젝트 만들기
가상환경이 켜져 있는 상태에서 생성해준다.

**WINDOW, MAC**
> django-admin startproject blog

프로젝트 이름의 폴더가 생성 된다.

## 1.5. 장고 앱 만들기
~~app은 어디에서 만들어도 상관없지만,~~    
**manage.py가 있는 경로**에서 장고 앱을 만드는 것을 권장
>python manage.py startapp crud

## 1.6. 장고 앱과 프로젝트를 연결시켜주기
**프로젝트폴더/settings.py**
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crud.apps.CrudConfig',
]
```
> 두번째 앱 이름의 시작은 대문자로 적어주어야 된다.

허나 **앱 이름**만 적어주어도 무방하다.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crud',
]
```

***

# 2. READ 만들기 (home)
## 2.1. crud/Templates/home.html 만들기
app폴더 안에 Templates라는 폴더를 만들고 그 안에 home.html 파일을 생성해준다.   
(views.py 에서 처리된 데이터를 받아 사용자에게 보여주는 파일이다.)

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
</body>
</html>
```

## 2.2. crud/views.py
app폴더 안에 views.py안에 앱의 기능을 구현해준다.   
ex)
```
def home(request):
  reurn render(requst, 'home.html')
```

>여기서 사용된 render라는 함수는 django에서 제공해주는 함수이다.
>> 첫번재 인자로 requst를 받으며, 두번재로는 템플릿, 세번재로는 템플릿에 보내줄 객체를 넣어준다.

## 2.3. urls.py
요청에 맞는 함수를 views.py에서 찾아 요청을 전달한다.

```
from django.contrib import admin
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
]
```

>사용할 views.py를 import 해주어야 한다.

>path(url, 함수경로, path의 이름)
>>path의 이름은 함수의 이름과 일치시키는 것을 권장한다.


## 2.4. crud/models.py
어떤 내용을 저장할지 작성해줍니다.   
- Blog(객체)
  - title(제목)
  - writer(작성자)
  - pub_date(작성일)
  - body(내용)
  - summary(줄이기)

>CharField =  문자(256글자 이하 작성가능)   
TextField = 문자(256글자 이상도 작성가능)
DateTimeField = 날짜   
BooleanField = 참/거짓   
IntegerField = 숫자   
FileField = 파일
ImageField = 이미지   
EmailField = 이메일   
URLField = URL   
...등등

담고자 하는 내용과 알맞는 Field를 골라서 models.py을 작성합니다.

```
from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()

    def summary(self):
        return self.body[:100]
```

## 2.5. 데이터 베이스에 적용하기
우리가 만들어준 model을 인식시켜주는 작업이다.   
터미널에 다음 명령어를 입력한다.

**변경사항에 대한 마이그레이션 만들기** 
> python manage.py makemigrations

**변경사항을 데이터베이스에 적용하기**
> python manage.py migrate 

## 2.6. crud/views.py
models.py에 맞춰서 crud/views/home을 수정합니다.

```
from .models import Blog
# models.py의 Blog를 가져와줍니다.

def home(req):
    blogs = Blog.objects.all()
    # Blog의 모든 objects를 가져옵니다.
    return render(req, 'home.html', {'blogs':blogs})
```

## 2.7. crud/Templates/home.html
views.py에 맞춰 crud/Templates/home.html을 수정합니다.

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
    {% for blog in blogs %}
    <div>
        <h3>
            {{blog.title}}
        </h3>
        {{blog.pub_date}}
        <br>
        {{blog.wirter}}
        <br>
        {{blog.summary}}...more
    </div>
    {% endfor %}
    
</body>
</html>
```
> for문을 통하여 blog안에 있는 object들을 하나씩 꺼내줍니다.   
>> 저장된 object하나씩 blog라는 이름에 넣어 해당하는 값(ex. title, pub_date...)을 하나씩 가져와 줍니다.

## 2.8. admin에서 업로드해보기
### 2.8.1. crud/admin.py
admin.py에 우리가 만든 model Blog를 가져와줍니다.

```
from .models import Blog

# Register your models here.
admin.site.register(Blog)
```

해당 작업을 통해 admin에서 blog를 확인 할 수 있습니다.

### 2.8.2. admin계정 만들기
manage.py가 있는 경로(프로젝트/crud)일 때,
터미널에 다음 명령어를 입력하여 계정을 생성한다.
> python manage.py createsuperuser

비밀번호는 보안을 위해 입력시 보이지 않는다.
너무 단순한 비밀번호일 경우 (y/n)로 확인 받는다.
사용을 원할 경우 y를 입력해주면 된다.

### 2.8.3. runserver
manage.py가 있는 경로(프로젝트/crud)에서 다음 명령어를 입력한다.
> python manage.py runserver

**'입력 시 나오는 주소/admin'**을 통하여 admin 사이트로 이동한다.
생성한 아이디와 비밀번호를 입력하여 들어간다.

### 2.8.4. Blog 생성하기
Blogs안에 들어가면 ADD BLOG 버튼을 통해 블로그를 생성할 수 있다.

### 2.8.5. READ 확인하기
다시 home.html인 '기본 주소'로 돌아가 제대로 나오는지 확인한다.
***
# 3. READ 만들기 (detail)
## 3.1. crud/Templates/detail.html 만들기
html을 작성하며 어떤 내용이 필요한지 정리한다.
- title(제목)
- writer(작성자)
- pub_date(작성일)
- body(내용)

```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상세페이지</title>
</head>
<body>
    <h1>제목</h1>
    <hr>
    작성자 : 
    날짜 : 
    내용 : 
    <a href="{% url 'home' %}">홈으로</a>
</body>
</html>
```

django에서는 주소를 {% url 'path name' %}으로 작성한다.

## 3.2. crud/views.py

```
from django.shortcuts import get_object_or_404, render
from .models import Blog

def home(req):
    blogs = Blog.objects.all()
    return render(req, 'home.html', {'blogs':blogs})

def detail(req, id):
    blog = get_object_or_404(Blog, pk=id)
    return render(req, 'detail.html', {'blog':blog})
```
> model Blog에서 id값에 해당하는 객체를 get방식으로 가져와 객체 blog에 저장한다. 없다면 404페이지를 띄운다.

## 3.3. crud/Templates/detail.html 수정하기
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상세페이지</title>
</head>
<body>
    <h1>{{blog.title}}</h1>
    <hr>
    작성자 : {{blog.writer}}
    날짜 : {{blog.pub_date}}
    내용 : {{blog.body}}
    
    <a href="{% url 'home' %}">홈으로</a>
</body>
</html>
```
객체 blog에 있는 내용을 하나씩 가져온다.

## 3.4. urls.py
```
from django.contrib import admin
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('detail/<int:id>', detail, name="detail"),
```
<int:id>id값을 int로 받아온다.

## 3.5. crud/Templates/home.html 수정하기
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

blog를 보러가는 버튼을 만들어준다.
***
# 4. Create 만들기
## 4.1. crud/Templates/new.html 만들기
html을 작성하며 어떤 내용이 필요한지 정리한다.
- title(제목)
- writer(작성자)
- body(내용)

```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>작성페이지</title>
</head>
<body>
    <h1>Write</h1>
    <form action="" method="POST">
        {% csrf_token %}
        <label for="title">제목 : </label>
        <input type="text" name="title" id="title">
        <br>
        <label for="writer">작성자 : </label>
        <input type="text" name="writer" id="writer">
        <br>
        <label for="body">내용 : </label>
        <textarea name="body" id="body" cols="30" rows="10"></textarea>
        <br>
        <input type="submit">
    </form>
</body>
</html>
```
> django 1.2 부터 form으로 post 요청을 전송 시 csrf를 검사하기 때문에 {% csrf_token %} 잊지말고 작성해준다.

> label의 for과 input의 id값을 일치시킨다.   
input의 name은 views와 일치시킨다. 

## 4.2. crud/views.py 만들기
만약 작성 완료 후 제출을 했다면, 새로 작성한 blog를 저장하고   
아직 작성하기 전이라면 작성하는 페이지를 띄워준다.   

작성을 구분하는 방법은 method를 이용한다.

시간은 현재시간을 자동으로 받아 저장한다.

```
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog
from django.utils import timezone

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
        return render(req, 'new.html')
```
## 4.3. urls.py
```
from django.contrib import admin
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('detail/<int:id>', detail, name="detail"),
    path('create/', create, name="create"),
]
```

## 4.4. 연결하기

**new.html**
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>작성페이지</title>
</head>
<body>
    <h1>Write</h1>
    <form action="{% url 'create' %}" method="POST">
        {% csrf_token %}
        <label for="title">제목 : </label>
        <input type="text" name="title" id="title">
        <br>
        <label for="writer">작성자 : </label>
        <input type="text" name="writer" id="writer">
        <br>
        <label for="body">내용 : </label>
        <textarea name="body" id="body" cols="30" rows="10"></textarea>
        <br>
        <input type="submit">
    </form>
</body>
</html>
```

**home.html**
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
***
# 5. UPDATE 만들기
## 5.1. crud/Templates/edit.html 만들기
html을 작성하며 어떤 내용이 필요한지 정리한다.
- title(제목)
- writer(작성자)
- body(내용)

```
<h1>update</h1>

<form action="" method="post">
    {% csrf_token %}
    <label for="title">제목 : </label>
    <input type="text" name="title" id="title" value="">
    <br>
    <label for="writer">작성자 : </label>
    <input type="text" name="writer" id="writer" value="">
    <br>
    <label for="body">내용 : </label>
    <textarea name="body" id="body" cols="30" rows="10"></textarea>
    <input type="submit">
</form>
```

> django 1.2 부터 form으로 post 요청을 전송 시 csrf를 검사하기 때문에 {% csrf_token %} 잊지말고 작성해준다.

## 5.2. crud/views.py
만약 작성 완료 후 제출을 했다면, 수정한 blog를 저장하고   
아직 수정하기 전이라면 수정하는 페이지를 띄워준다.   

작성을 구분하는 방법은 method를 이용한다.

```
def update(req, id):
    if req.method =="POST":
        update_blog = get_object_or_404(Blog, pk=id)
        update_blog.title = req.POST['title']
        update_blog.writer = req.POST['writer']
        update_blog.body = req.POST['body']
        update_blog.save()
        return redirect('detail', str(update_blog.id))
    else :
        edit_blog = get_object_or_404(Blog, pk=id)
        return render(req, 'edit.html', {'blog':edit_blog})
```

## 5.3. urls.py
```
from django.contrib import admin
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('detail/<int:id>', detail, name="detail"),
    path('create/', create, name="create"),
    path('update/<int:id>', update, name="update"),
]
```

## 5.4. 연결하기

**edit.html**
```
<h1>update</h1>

<form action="{% url 'update' blog.id %}" method="post">
    {% csrf_token %}
    <label for="title">제목 : </label>
    <input type="text" name="title" id="title" value="{{blog.title}}">
    <br>
    <label for="writer">작성자 : </label>
    <input type="text" name="writer" id="writer" value="{{blog.writer}}">
    <br>
    <label for="body">내용 : </label>
    <textarea name="body" id="body" cols="30" rows="10">{{blog.body}}</textarea>
    <input type="submit">
</form>
```

**detail.html**
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상세페이지</title>
</head>
<body>
    <h1>{{blog.title}}</h1>
    <hr>
    작성자 : {{blog.writer}}
    날짜 : {{blog.pub_date}}
    내용 : {{blog.body}}

    <a href="{% url 'update' blog.id %}">수정</a>
    <a href="{% url 'home' %}">홈으로</a>
</body>
</html>
```

> update를 이동할때는 id값을 함께 전달해준다.

***
# 6. DELETE 만들기
## 6.1. crud/views.py
```
def delete(req, id):
    delete_blog = get_object_or_404(Blog, pk=id)
    delete_blog.delete()
    return redirect('home')
```

## 6.2. urls.py
```
from django.contrib import admin
from django.urls import path
from crud.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('detail/<int:id>', detail, name="detail"),
    path('create/', create, name="create"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
]
```

## 6.3. crud/detail.html
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상세페이지</title>
</head>
<body>
    <h1>{{blog.title}}</h1>
    <hr>
    작성자 : {{blog.writer}}
    날짜 : {{blog.pub_date}}
    내용 : {{blog.body}}

    <a href="{% url 'update' blog.id %}">수정</a>
    <a href="{% url 'delete' blog.id %}">삭제</a>
    <a href="{% url 'home' %}">홈으로</a>
</body>
</html>
```
