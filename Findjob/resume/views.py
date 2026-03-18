from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ResumeForm, CategoryForm
from .models import Resume, Category
def index(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    resumes = Resume.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    if category_id:
        resumes = resumes.filter(category_id=category_id)
    if search_query:
        resumes = resumes.filter(name__icontains=search_query)
    context = {
        'resumes': resumes,
        'categories': categories,
    }
    return render(request, 'resume/index.html', context)
@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('index')
    else:
        form = ResumeForm()
    return render(request, 'resume/create_resume.html', {'form': form})
@login_required
def create_resume_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoryForm()
    return render(request,'resume/create_resume_category.html',{'form':form})
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request,'resume/resume_detail.html',{'resume': resume})
@login_required
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.user != resume.user:
        return HttpResponse('У вас нет прав на изменение этого резюме')
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ResumeForm(instance=resume)
    return render(request,'resume/edit_resume.html', {'form': form, 'resume': resume})
@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.user != resume.user:
        return HttpResponse('У вас нет прав на удаление этого резюме')

    if request.method == 'POST':
        resume.delete()
        return redirect('index')
    return render(request,'resume/delete_resume.html', {'resume': resume})