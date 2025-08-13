from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import RegisterForm, PostForm
from .models import Post

# Handles user registration
# - Displays a registration form (GET request)
# - Saves new user and logs them in automatically (POST request)

def register_view(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)  # Log in user after registration
      return redirect('profile')
  else:
    form = RegisterForm()
  return render(request, 'registration/register.html', {'form': form})

@login_required

# Handles user profile view & update
# - Requires login to access (@login_required)
# - Allows updating email address
@login_required
def profile_view(request):
  if request.method == 'POST':
    request.user.email = request.POST.get('email')
    request.user.save()
  return render(request, 'registration/profile.html')

# LIST: Anyone can view all posts. Ordered newest first.
class PostListView(ListView):
  model = Post
  template_name = "blog/post_list.html"        # templates/blog/post_list.html
  context_object_name = "posts"
  ordering = ["-published_date"]
  paginate_by = 10  # optional

# DETAIL: Anyone can view a single post.
class PostDetailView(DetailView):
  model = Post
  template_name = "blog/post_detail.html"      # templates/blog/post_detail.html
  context_object_name = "post"

# CREATE: Only authenticated users can create.
# - author is set to request.user in form_valid()
class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"        # used for both create & update

  def form_valid(self, form):
    # Bind the logged-in user as the author (not exposed on the form)
    form.instance.author = self.request.user
    return super().form_valid(form)

# UPDATE: Only the author can edit.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"

  def test_func(self):
    # Author-only access
    post = self.get_object()
    return post.author == self.request.user

# DELETE: Only the author can delete. Redirect to list on success.
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = "blog/post_confirm_delete.html"
  success_url = reverse_lazy("post-list")

  def test_func(self):
    post = self.get_object()
    return post.author == self.request.user
