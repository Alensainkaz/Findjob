from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ResumeForm
from .models import Resume, SPECIALITY_CHOICES


def _can_manage(user, resume):
    return user.is_staff or resume.user_id == user.id


def index(request):
    resumes = Resume.objects.all().order_by('-created_at')
    search_query = request.GET.get('q')
    speciality_filter = request.GET.get('speciality')
    if speciality_filter:
        resumes = resumes.filter(speciality=speciality_filter)
    if search_query:
        matching_specialities = [
            value for value, label in SPECIALITY_CHOICES
            if search_query.lower() in label.lower()
        ]
        resumes = resumes.filter(
            Q(name__icontains=search_query) |
            Q(surname__icontains=search_query) |
            Q(speciality__icontains=search_query) |
            Q(speciality__in=matching_specialities)
        )
    context = {
        'resumes': resumes,
        'specialities': SPECIALITY_CHOICES,
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


def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request, 'resume/resume_detail.html', {'resume': resume})


@login_required
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        return HttpResponseForbidden('У вас нет прав на изменение этого резюме')
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume/edit_resume.html', {'form': form, 'resume': resume})


@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        return HttpResponseForbidden('У вас нет прав на удаление этого резюме')
    if request.method == 'POST':
        resume.delete()
        return redirect('index')
    return render(request, 'resume/delete_resume.html', {'resume': resume})
