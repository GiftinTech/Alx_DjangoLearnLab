from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import RegisterForm, PostForm, CommentForm

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
class ListView(ListView):
  model = Post
  template_name = "blog/post_list.html"        # templates/blog/post_list.html
  context_object_name = "posts"
  ordering = ["-published_date"]
  paginate_by = 10  # optional

# DETAIL: Anyone can view a single post.
class DetailView(DetailView):
  model = Post
  template_name = "blog/post_detail.html"      # templates/blog/post_detail.html
  context_object_name = "post"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comments.all().order_by('-created_at')
    context['form'] = CommentForm()
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = self.object
      comment.author = request.user
      comment.save()
      return redirect('post-detail', pk=self.object.pk)
    return self.get(request, *args, **kwargs)

# CREATE: Only authenticated users can create.
# - author is set to request.user in form_valid()
class CreateView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"        # used for both create & update

  def form_valid(self, form):
    # Bind the logged-in user as the author (not exposed on the form)
    form.instance.author = self.request.user
    return super().form_valid(form)

# UPDATE: Only the author can edit.
class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_form.html"

  def test_func(self):
    # Author-only access
    post = self.get_object()
    return post.author == self.request.user

# DELETE: Only the author can delete. Redirect to list on success.
class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = "blog/post_confirm_delete.html"
  success_url = reverse_lazy("post-list")

  def test_func(self):
    post = self.get_object()
    return post.author == self.request.user

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm

def add_comment(request, pk):
  """Handle adding a comment to a specific post."""
  post = get_object_or_404(Post, pk=pk)

  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)  # Create but don't save yet
      comment.author = request.user      # Set logged-in user as author
      comment.post = post                # Link to the current post
      comment.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = CommentForm()

  return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  """Allow comment authors to edit their comments."""
  model = Comment
  form_class = CommentForm
  template_name = 'blog/edit_comment.html'

  def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author

  def get_success_url(self):
    return reverse('post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  """Allow comment authors to delete their comments."""
  model = Comment
  template_name = 'blog/delete_comment.html'

  def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author

  def get_success_url(self):
    return reverse('post_detail', kwargs={'pk': self.object.post.pk})
