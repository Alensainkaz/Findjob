import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from cart.models import CartItem
from users.views import _mask_email
from .forms import ResumeForm
from .cities import CITY_LABELS, city_groups
from .models import Resume, ResumeEmailCode, SPECIALITY_CHOICES

logger = logging.getLogger(__name__)

PAGE_SIZE = 12


def _can_manage(user, resume):
    return user.is_authenticated and (user.is_staff or resume.user_id == user.id)


def _filtered_resumes(params):
    resumes = Resume.objects.filter(email_verified=True).order_by('-created_at')
    search_query = (params.get('q') or '').strip()
    speciality_filter = params.get('speciality')
    if speciality_filter:
        resumes = resumes.filter(speciality=speciality_filter)
    city_filter = params.get('city')
    if city_filter in CITY_LABELS:
        resumes = resumes.filter(city=city_filter)
    if search_query:
        needle = search_query.lower()
        with translation.override('en'):
            english = {value: str(label) for value, label in SPECIALITY_CHOICES}
        # Match the label in the visitor's language and in English
        matching_specialities = [
            value for value, label in SPECIALITY_CHOICES
            if needle in str(label).lower() or needle in english[value].lower()
        ]
        resumes = resumes.filter(
            Q(name__icontains=search_query) |
            Q(surname__icontains=search_query) |
            Q(speciality__icontains=search_query) |
            Q(speciality__in=matching_specialities)
        )
    return resumes


def _speciality_options():
    options = [{'value': v, 'label': str(l)} for v, l in SPECIALITY_CHOICES]
    return sorted(options, key=lambda o: o['label'].lower())


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
        'city': resume.get_city_display() if resume.city else '',
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
        'specialities': _speciality_options(),
        'city': request.GET.get('city', '') if request.GET.get('city') in CITY_LABELS else '',
        'cities': city_groups(),
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
    initial = {name: (form[name].value() or '') for name in ['name', 'surname', 'father_name', 'city', 'education', 'experience', 'email', 'speciality']}
    return {
        'form': form,
        'resume': resume,
        'props': {
            'initial': initial,
            'errors': errors,
            'image': resume.image.url if resume and resume.image else '',
            'specialities': _speciality_options(),
            'cities': city_groups(),
            'submitLabel': _('Save changes') if resume else _('Publish resume'),
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
            resume.email_verified = _owns_address(request.user, resume.email)
            return _save_and_confirm(request, form, resume, 'resume/create_resume.html')
    else:
        form = ResumeForm(initial={'email': request.user.email})
    return render(request, 'resume/create_resume.html', _resume_form_context(form))


def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    can_manage = _can_manage(request.user, resume)
    if not resume.email_verified and not can_manage:
        raise Http404
    return render(request, 'resume/resume_detail.html', {
        'resume': resume,
        'can_manage': can_manage,
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
        return HttpResponseForbidden(_('You cannot edit this resume.'))
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            if 'email' in form.changed_data:
                resume.email_verified = _owns_address(request.user, resume.email)
            return _save_and_confirm(request, form, resume, 'resume/edit_resume.html', resume)
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resume/edit_resume.html', _resume_form_context(form, resume))


@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        return HttpResponseForbidden(_('You cannot delete this resume.'))
    if request.method == 'POST':
        resume.delete()
        return redirect('index')
    return render(request, 'resume/delete_resume.html', {'resume': resume})


# ---------- resume email confirmation ----------

def _owns_address(user, email):
    """The account email was confirmed at sign-up, so reusing it needs no new code."""
    return bool(user.is_active and user.email and email and user.email.lower() == email.lower())


def _send_resume_code(resume):
    code_obj, _created = ResumeEmailCode.objects.get_or_create(resume=resume, defaults={'email': resume.email})
    code_obj.email = resume.email
    code = code_obj.issue_code()
    code_obj.save(update_fields=['email'])
    context = {'resume': resume, 'code': code, 'minutes': int(ResumeEmailCode.CODE_TTL.total_seconds() // 60)}
    send_mail(
        subject=_('%(code)s is your Findy-Job resume confirmation code') % {'code': code},
        message=render_to_string('resume/email/verify_code.txt', context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[resume.email],
        fail_silently=False,
        html_message=render_to_string('resume/email/verify_code.html', context),
    )


def _save_and_confirm(request, form, resume, template, existing=None):
    """Save the resume; when its email is unconfirmed, send a code and go to the code page."""
    try:
        with transaction.atomic():
            form.save()  # form.instance is `resume`, with user/email_verified already set
    except IntegrityError:
        form.add_error('email', _('A resume with this email already exists.'))
        return render(request, template, _resume_form_context(form, existing))
    if resume.email_verified:
        return redirect('resume_detail', pk=resume.pk)
    # The code page sends a code only when none exists for the current address,
    # so re-saving an unconfirmed resume cannot bypass the resend cooldown
    return redirect('verify_resume_email', pk=resume.pk)


def _managed_unverified(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if not _can_manage(request.user, resume):
        raise Http404
    return resume


@login_required
def verify_resume_email(request, pk):
    resume = _managed_unverified(request, pk)
    if resume.email_verified:
        return redirect('resume_detail', pk=resume.pk)
    code_obj = ResumeEmailCode.objects.filter(resume=resume, email=resume.email).first()
    if code_obj is None:
        # No code for the current address yet (e.g. the send failed earlier): issue one now
        try:
            _send_resume_code(resume)
        except Exception:
            logger.exception('Could not send resume confirmation code to %s', resume.email)
            messages.error(request, _('We could not send the confirmation code. Please try again later.'))
            return redirect('resume_detail', pk=resume.pk)
        code_obj = resume.email_code

    error = ''
    if request.method == 'POST':
        code = ''.join(ch for ch in request.POST.get('code', '') if ch.isdigit())
        ok, error = code_obj.check_code(code)
        if ok:
            resume.email_verified = True
            try:
                with transaction.atomic():
                    resume.save(update_fields=['email_verified'])
            except IntegrityError:
                error = _('A resume with this email already exists.')
            else:
                code_obj.delete()
                messages.success(request, _('Email confirmed. Your resume is now published.'))
                return redirect('resume_detail', pk=resume.pk)

    return render(request, 'resume/verify_email.html', {
        'resume': resume,
        'props': {
            'email': _mask_email(resume.email),
            'error': error,
            'resendIn': code_obj.resend_available_in,
            'resendUrl': reverse('resend_resume_code', args=[resume.pk]),
        },
    })


@login_required
@require_POST
def resend_resume_code(request, pk):
    resume = _managed_unverified(request, pk)
    if resume.email_verified:
        return JsonResponse({'ok': False, 'error': _('This email is already confirmed.')}, status=400)
    code_obj = ResumeEmailCode.objects.filter(resume=resume).first()
    wait = code_obj.resend_available_in if code_obj else 0
    if wait:
        return JsonResponse({'ok': False, 'error': _('Please wait %(seconds)d s.') % {'seconds': wait}, 'resendIn': wait}, status=429)
    try:
        _send_resume_code(resume)
    except Exception:
        logger.exception('Could not resend resume confirmation code to %s', resume.email)
        return JsonResponse({'ok': False, 'error': _('We could not send the code. Try again later.')}, status=502)
    return JsonResponse({'ok': True, 'resendIn': resume.email_code.resend_available_in})
