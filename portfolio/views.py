from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    Profile, Skill, Education, Project,
    Experience, Certificate, BlogPost
)
from .forms import ContactForm


def home(view):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()
    recent_blog_posts = BlogPost.objects.filter(published=True)[:3]

    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'skills': skills,
        'recent_blog_posts': recent_blog_posts,
    }
    return render(view, 'home.html', context)


def about(request):
    profile = Profile.objects.first()
    education = Education.objects.all()
    certificates = Certificate.objects.all()

    context = {
        'profile': profile,
        'education': education,
        'certificates': certificates,
    }
    return render(request, 'about.html', context)


def projects(request):
    project_type = request.GET.get('type', 'all')

    if project_type == 'all':
        projects_list = Project.objects.all()
    else:
        projects_list = Project.objects.filter(project_type=project_type)

    paginator = Paginator(projects_list, 6)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)

    context = {
        'projects': projects_page,
        'current_type': project_type,
        'project_types': Project.PROJECT_TYPE,
    }
    return render(request, 'projects.html', context)


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.exclude(pk=pk).filter(
        technologies__icontains=project.technologies.split(',')[0]
    )[:3]

    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)


def experience_view(request):
    experiences = Experience.objects.all()
    context = {
        'experiences': experiences,
    }
    return render(request, 'experience.html', context)


def skills_view(request):
    skills_by_category = {}
    for category_code, category_name in Skill.SKILL_CATEGORIES:
        skills_by_category[category_name] = Skill.objects.filter(category=category_code)

    context = {
        'skills_by_category': skills_by_category,
    }
    return render(request, 'skills.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    profile = Profile.objects.first()
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'contact.html', context)


def blog_list(request):
    blog_posts = BlogPost.objects.filter(published=True)
    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'posts': posts_page,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    post.views += 1
    post.save()

    related_posts = BlogPost.objects.filter(published=True).exclude(slug=slug)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)