from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Blog, Project, ProjectFile, ProjectService, Service, Team, TeamMember, Testimonial, Article,Comment,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .forms import ArticleForm, CommentForm, CustomRegistrationForm, ProjectForm, blogCommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.status = 'in_progress'
            project.client = request.user  # Set the current user as the client
            project.save()
            return redirect('request')     # Replace 'project_list' with the appropriate URL or view name for your project list
    else:
        form = ProjectForm()
        projects = Project.objects.filter(client=request.user)  # Fetch all projects created by the logged-in user
    
    return render(request, 'create_project.html', {'form': form , 'navbar': 'request', 'projects': projects})
def about_view(request):
    projects = Project.objects.filter(status="C").count()
    
    users=User.objects.all().count()

    return render(request,'about.html',{"projects":projects, "users":users})

class RegistrationView(View):
    def get(self, request):
        form = CustomRegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Replace 'login' with the URL name of your login page
        return render(request, 'registration.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def homePageView(request):
    projects = Project.objects.all().count()
    users=User.objects.all().count()
    team=Team.objects.all().count()
    teamMember=TeamMember.objects.all().count()
    return render(request, 'home.html', {'projects': projects , 'navbar': 'home' , "users":users, "team":team, "teamMember":teamMember})

def servicesPageView(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services, 'navbar': 'services'})



def team_view(request, id):
    team = get_object_or_404(Team, id=id)
    members = team.members.all()
    completed_projects = team.project_set.filter(status='C')
    in_progress_projects = team.project_set.filter(status='IP')
    
    return render(request, 'team.html', {
        'team': team,
        'members': members,
        'completed_projects': completed_projects,
        'in_progress_projects': in_progress_projects,
        'navbar': 'teams'
    })


def teams_view(request):
    teams = Team.objects.all()
     # Create a paginator with 10 items per page
    paginator = Paginator(teams, 2)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page_number)
    context = {
        'teams': page_obj
        ,'navbar': 'teams'
    }

    return render(request, 'teams.html', context)
def contact_view(request):
    if request.method == 'POST':
        # Handle contact form submission
        pass
    else:
        # Render contact form template
        return render(request, 'contact.html')



@login_required(login_url='login')
def add_comment(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect('detail_portfolio', id=id)

    return redirect('detail_portfolio', id=id)

def portfolio_detail(request, id):
    project = get_object_or_404(Project, id=id)
    comments = Comment.objects.filter(project=project)
    comment_form = CommentForm()

    # Get the ProjectService objects for the project
    project_services = ProjectService.objects.filter(project=project)

    context = {
        'project': project,
        'comments': comments,
        'comment_form': comment_form,
        'project_services': project_services,
        'navbar': 'portfolio',
    }
    return render(request, 'detail_portfolio.html', context)

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

def portfolio_view(request):
    projects = Project.objects.filter(status='C')
    Projects_S = ProjectService.objects.all()
    Projectf = ProjectFile.objects.all()

    # Create a paginator with 10 items per page
    paginator = Paginator(projects, 6)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page_number)


    return render(request, 'portfolio.html', {
        'projects': page_obj,
        'projects_S': Projects_S,
        'projectf': Projectf,
        'navbar': 'portfolio'
    })
@login_required(login_url='login')
def contact_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('contact')  # Replace 'article_list' with the name of your article list view
    else:
        form = ArticleForm()
    return render(request, 'contact.html', {'form': form})

#partie static

def blog_item(request):
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs,
    }

    return render(request, 'blog.html', context)

def pricing_view(request):
    return render(request,'pricing.html')



def single_blog_view(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all()
    blogform = blogCommentForm()
    context = {
        'blog': blog,
        'comments': comments,
        'form': blogform,
    }
    return render(request, 'blog_single.html', context)
@login_required(login_url='login')
def add_blog_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        form = blogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('single_blog', id=blog_id)
    return redirect('single_blog', id=blog_id)


