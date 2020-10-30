from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.views import View
from django.views.generic import CreateView, TemplateView,ListView,DetailView,DeleteView,FormView
from django.utils import timezone
from .models import Post,Like,Comment
from .forms import PostForm,UserCreateForm, LoginForm,CommentForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect 
from django.utils.functional import cached_property
#@login_required
#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#    return render(request, 'mybook/post_list.html', {'posts':posts})

def home_page(request):
    return render(request, 'mybook/home.html')

class PostListView(LoginRequiredMixin,ListView):
    template_name = 'mybook/post_list.html'
    #model = Post
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context_object_name = 'posts'

#@login_required
#def post_detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    likes = Like.objects.filter(post=post,user=request.user).exists()
    #return render(request, 'mybook/post_detail.html', {'post': post},{'likes': likes})
    #return render(request, 'mybook/post_detail.html', {'post': post})

class PostDetail(LoginRequiredMixin,DetailView):
    template_name = 'mybook/post_detail.html'
    model = Post
    context_object_name = 'post'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['check'] = Like.objects.filter(user=self.request.user, post=self.kwargs.get('pk')).exists()
        context['comments']= Comment.objects.filter(post=self.kwargs.get('pk'))
        return context

class NewPost(FormView):
   template_name ="mybook/post_edit.html"
   form_class=PostForm
   def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        return super().form_valid(form)
   def get_success_url(self, **kwargs):
       return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

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
#def like(request, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    #post = Post.objects.get(id=kwargs['post_id'])
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    # unlike
    if is_like > 0:
        #liking = Like.objects.get(user=request.user,post__id=kwargs['post_id'])
        liking = Like.objects.get(user=request.user,post=post)
        liking.delete()
        post.like_num -= 1
        post.save()
        #messages.warning(request, 'いいねを取り消しました')
        return redirect('post_detail',pk=post.pk)
        #return redirect(reverse_lazy('posts:post_detail', kwargs={'post_id': kwargs['post_id']}))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    #messages.success(request, 'いいね！しました')
    return redirect('post_detail',pk=post.pk)
    #return HttpResponseRedirect(reverse_lazy('posts:post_detail', kwargs={'post_id': kwargs['post_id']}))

#@login_required
#def myLike(request):  
#    posts = Like.objects.filter(date_created__lte=timezone.now(),user=request.user).order_by('date_created')

#    return render(request, 'mybook/mylike.html', {'posts':posts})

class MyLikeView(ListView):
    template_name = 'mybook/mylike.html'
    context_object_name = 'posts'
    def get_queryset(self):
        # queryset = super(ListView, self).get_queryset()  
        queryset = Like.objects.filter(date_created__lte=timezone.now(),user=self.request.user).order_by('date_created')
        return queryset

@login_required
def comment(request,pk):
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            #comment.date_created = timezone.now()
            #posts = Post.objects.filter(pk=pk)
            #comment.post = posts.first()
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm()
    return render(request, 'mybook/comment.html', {'form': form})