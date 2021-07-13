from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from blog.models import Post
from django.contrib.auth.models import User
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'blog/home.html'


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3           # MINS ye ordring hain ye kya karta,ki ye jo ham nayi post dalte hain nto ye post startting me diknni chahiye..old bad me


class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'


    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")





'''  create the details view : 
          the default html page view create then name is is post_detail.html.
          then it is use for my page is list viewthen click for name then shows for user deatails....
          '''

class PostDetailsView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ["title","content"]
    template_name = "blog/newcreate.html"

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    template_name = "blog/update.html"
    fields=["title","content"]

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = "blog/delete.html"
    success_url = reverse_lazy("blog-posts")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
