from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ResumeForm
from .models import Resume,SPECIALITY_CHOICES
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
def index(request):
    specialities=(choice[1] for choice in SPECIALITY_CHOICES)
    resumes = Resume.objects.all().order_by('-created_at')
    search_query = request.GET.get('q')    
    speciality_filter=request.GET.get('speciality')
    if speciality_filter:
        resumes=resumes.filter(speciality=speciality_filter)
    if search_query:
        resumes = resumes.filter(
        Q(name__icontains=search_query) |
        Q(surname__icontains=search_query) |
        Q(speciality__icontains=search_query)
    )
    context = {
        'resumes': resumes,
        'specialities':specialities,
    }
    return render(request, 'resume/index.html', context)

@login_required
def create_resume(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('index')
    else:
        form = ResumeForm()
    return render(request, 'resume/create_resume.html', {'form': form})
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request,'resume/resume_detail.html',{'resume': resume})
@staff_member_required
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not request.user.is_staff and request.user != resume.user:
        return HttpResponse('У вас нет прав на изменение этого резюме')
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ResumeForm(instance=resume)
    return render(request,'resume/edit_resume.html', {'form': form, 'resume': resume})
@staff_member_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not request.user.is_staff and request.user != resume.user:
        return HttpResponse('У вас нет прав на удаление этого резюме')
    if request.method == 'POST':
        resume.delete()
        return redirect('index')
    return render(request, 'resume/delete_resume.html', {'resume': resume})