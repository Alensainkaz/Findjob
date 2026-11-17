from django.contrib.messages import get_messages


def toasts(request):
    """Django messages as props for the Vue toast host."""
    level_map = {'error': 'error', 'warning': 'error', 'success': 'success'}
    return {
        'toast_props': {
            'messages': [
                {'text': str(m), 'level': level_map.get(m.level_tag, 'info')}
                for m in get_messages(request)
            ],
        },
    }


def vercel(request):
    """Expose whether we run on Vercel, so the bundle loads Web Analytics only there."""
    from django.conf import settings
    return {'on_vercel': getattr(settings, 'ON_VERCEL', False)}
