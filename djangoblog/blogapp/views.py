from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import author, category, article
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    article_data = article.objects.all()
    paginator = Paginator(article_data, 4) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    context={
        "post":contacts
        
    }
  
    return render(request, "index.html", context)

def getauthor(request, name):
    get_author=get_object_or_404(User, username=name)
    auth=get_object_or_404(author, name=get_author.id)
    post=article.objects.filter(article_author=auth.id)
    context={
        "auth":auth,
        "post":post
    }
    return render(request, "profile.html", context)

def getsingle(request, id):
    post = get_object_or_404(article, pk = id)
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category = post.category).exclude(id=id)[:4]
    context = {
        "post":post,
        "first":first,
        "last":last,
        "related":related
    }
    
    return render(request, "single.html", context)

def getTopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category = cat.id)
    context = {
        "post":post,
        "cat":cat
    }

    return render(request, "category.html", context)

def getLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=="POST":
            user=request.POST.get('user')
            password=request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
    return render(request, "login.html")

def getLogout(request):
    logout(request)
    return redirect ('login')

def test(request, Name):
    Name = Name
    author_data = article.objects.all()
    category_filter=article.objects.filter(category = Name)
    context={
        "AuthorData":author_data

    }
    
    return render(request, "sample.html",context)

