from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.utils import timezone
from .models import Post
from .forms import PostForm,UserCreateForm, LoginForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'mybook/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'mybook/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'mybook/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #編集したいPost モデルを取得
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        #formを保存するとき
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        #formを開くだけのとき
    return render(request, 'mybook/post_edit.html', {'form': form})


#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'mybook/create.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'mybook/create.html', {'form': form,})

create_account = Create_account.as_view()

#ログイン機能
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'mybook/login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'mybook/login.html', {'form': form,})

account_login = Account_login.as_view()


#def Account_logout(request):
#    return render(request, 'mybook/login.html')