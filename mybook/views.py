from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.views import View
from django.views.generic import CreateView, TemplateView,ListView,DetailView,DeleteView
from django.utils import timezone
from .models import Post,Like
from .forms import PostForm,UserCreateForm, LoginForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages

#@login_required
#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#    return render(request, 'mybook/post_list.html', {'posts':posts})

class PostListView(LoginRequiredMixin,ListView):
    template_name = 'mybook/post_list.html'
    #model = Post
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context_object_name = 'posts'

#@login_required
#def post_detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    return render(request, 'mybook/post_detail.html', {'post': post})

class PostDetail(LoginRequiredMixin,DetailView):
    template_name = 'mybook/post_detail.html'
    model = Post
    context_object_name = 'post'

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #commit=False は Post モデルをまだ保存しないという意味
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
            #新しく作成されたポストの post_detail ページに移動
    else:
        form = PostForm()
    return render(request, 'mybook/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #編集したいPost モデルを取得
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        #formを保存するとき
        if form.is_valid():
            post = form.save(commit=False)
            if post.author == request.user:
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
            else:
                raise PermissionDenied

    else:
        form = PostForm(instance=post)
        #formを開くだけのとき
    return render(request, 'mybook/post_edit.html', {'form': form})

def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('post_list')
    else:
        raise PermissionDenied

class PostDelete(DeleteView):
    template_name = 'mybook/post_confirm_delete.html'
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

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

#    logout(request,user)
#    return render(request, 'mybook/logout.html')

class MyLogoutView(auth_views.LogoutView):
    
    # ログアウト時に表示されるテンプレート
    template_name = "templates/mybook/logout.html"

#class MyPage(LoginRequiredMixin, TemplateView):
    #template_name = 'templates/mybook/mypage.html'

#def get_myposts(request):
#        posts = Post.objects.filter(published_date__lte=timezone.now(),author=request.user).order_by('published_date')
#        #return posts
#        return render(request, 'mybook/mypage.html', {'posts':posts})

#class MyPageView(LoginRequiredMixin,ListView):
#    template_name = 'mybook/mypage.html'
#    context_object_name = 'posts'
    #model = Post
#    queryset = Post.objects.filter(published_date__lte=timezone.now(),author=request.user.order_by('published_date'))
    
class MyPageView(ListView):
    template_name = 'mybook/mypage.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # queryset = super(ListView, self).get_queryset()  
        queryset = Post.objects.filter(published_date__lte=timezone.now(),author=self.request.user).order_by('published_date')
        return queryset
    

@login_required
def like(request,pk):
    post = get_object_or_404(Post, pk=pk)
    
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(pk=pk, user=request.user)
        liking.delete()
        post.like_num -= 1
        post.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('post_detail'))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('post_detail'))
