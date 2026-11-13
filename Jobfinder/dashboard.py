from datetime import timedelta

from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from cart.models import CartItem
from resume.models import Resume
from users.models import User


def dashboard_callback(request, context):
    week_ago = timezone.now() - timedelta(days=7)
    top_specialities = (
        Resume.objects.values('speciality').annotate(total=Count('id')).order_by('-total')[:6]
    )
    labels = dict(Resume._meta.get_field('speciality').choices)
    context.update({
        'kpis': [
            {'title': 'Resumes', 'value': Resume.objects.count(),
             'note': f'+{Resume.objects.filter(created_at__gte=week_ago).count()} this week',
             'href': reverse('admin:resume_resume_changelist')},
            {'title': 'Users', 'value': User.objects.count(),
             'note': f'{User.objects.filter(is_active=False).count()} not verified',
             'href': reverse('admin:users_user_changelist')},
            {'title': 'Saved resumes', 'value': CartItem.objects.count(),
             'note': 'across all saved lists', 'href': reverse('admin:cart_cart_changelist')},
        ],
        'top_specialities': [
            {'label': labels.get(row['speciality'], row['speciality']), 'total': row['total']}
            for row in top_specialities
        ],
        'latest_resumes': Resume.objects.select_related('user').order_by('-created_at')[:6],
    })
    return context
