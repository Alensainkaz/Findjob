from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from cart.models import CartItem
from .forms import ResumeForm
from .models import Resume, SPECIALITY_CHOICES

PAGE_SIZE = 12


def _can_manage(user, resume):
    return user.is_authenticated and (user.is_staff or resume.user_id == user.id)


def _filtered_resumes(params):
    resumes = Resume.objects.all().order_by('-created_at')
    search_query = (params.get('q') or '').strip()
    speciality_filter = params.get('speciality')
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
    return resumes


def _saved_ids(user):
    if not user.is_authenticated:
        return set()
    return set(CartItem.objects.filter(cart__user=user).values_list('resume_id', flat=True))


def _serialize(resume, user, saved_ids):
    can_manage = _can_manage(user, resume)
    return {
        'id': resume.pk,
        'name': resume.name,
        'surname': resume.surname,
        'fatherName': resume.father_name,
        'speciality': resume.get_speciality_display(),
        'education': resume.education,
        'experience': resume.experience,
        'image': resume.image.url if resume.image else '',
        'url': reverse('resume_detail', args=[resume.pk]),
        'editUrl': reverse('edit_resume', args=[resume.pk]) if can_manage else '',
        'deleteUrl': reverse('delete_resume', args=[resume.pk]) if can_manage else '',
        'saved': resume.pk in saved_ids,
    }


def _page_payload(request):
    paginator = Paginator(_filtered_resumes(request.GET), PAGE_SIZE)
    page = paginator.get_page(request.GET.get('page') or 1)
    saved = _saved_ids(request.user)
    return {
        'results': [_serialize(r, request.user, saved) for r in page.object_list],
        'page': page.number,
        'hasNext': page.has_next(),
        'total': paginator.count,
    }


def index(request):
    payload = _page_payload(request)
    board = {
        **payload,
        'q': request.GET.get('q', ''),
        'speciality': request.GET.get('speciality', ''),
        'specialities': [{'value': v, 'label': l} for v, l in SPECIALITY_CHOICES],
        'isAuthenticated': request.user.is_authenticated,
        'loginUrl': reverse('login_view'),
        'apiUrl': reverse('api_resumes'),
        'toggleUrl': reverse('cart_toggle', args=[0]),
    }
    return render(request, 'resume/index.html', {
        'resumes': payload['results'],
        'board': board,
    })


@require_GET
def api_resumes(request):
    return JsonResponse(_page_payload(request))


def _resume_form_context(form, resume=None):
    errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
    initial = {name: (form[name].value() or '') for name in ['name', 'surname', 'father_name', 'education', 'experience', 'email', 'speciality']}
    return {
        'form': form,
        'resume': resume,
        'props': {
            'initial': initial,
            'errors': errors,
            'image': resume.image.url if resume and resume.image else '',
            'specialities': [{'value': v, 'label': l} for v, l in SPECIALITY_CHOICES],
            'submitLabel': 'Save changes' if resume else 'Publish resume',
            'cancelUrl': reverse('resume_detail', args=[resume.pk]) if resume else reverse('index'),
        },
    }


@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm()
    return render(request, 'resume/create_resume.html', _resume_form_context(form))


def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request, 'resume/resume_detail.html', {
        'resume': resume,
        'can_manage': _can_manage(request.user, resume),
        'save_props': {
            'saved': resume.pk in _saved_ids(request.user),
            'isAuthenticated': request.user.is_authenticated,
            'toggleUrl': reverse('cart_toggle', args=[resume.pk]),
            'loginUrl': reverse('login_view'),
        },
    })


@login_required
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        return HttpResponseForbidden('You cannot edit this resume.')
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume/edit_resume.html', _resume_form_context(form, resume))


@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        return HttpResponseForbidden('You cannot delete this resume.')
    if request.method == 'POST':
        resume.delete()
        return redirect('index')
    return render(request, 'resume/delete_resume.html', {'resume': resume})
