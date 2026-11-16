import hashlib
import hmac
import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, ngettext


class User(AbstractUser):
    ROLE_CHOICES = (
        ('employer', _('Employer')),
        ('admin', _('Administrator')),
        ('jobfinder', _('Job seeker')),
    )
    role = models.CharField(choices=ROLE_CHOICES, default='jobfinder', max_length=20)


def _hash_code(code):
    return hmac.new(settings.SECRET_KEY.encode(), code.encode(), hashlib.sha256).hexdigest()


class EmailVerificationToken(models.Model):
    CODE_TTL = timedelta(minutes=15)
    RESEND_COOLDOWN = timedelta(seconds=60)
    MAX_ATTEMPTS = 5

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    code_hash = models.CharField(max_length=64, blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    sent_at = models.DateTimeField(null=True, blank=True)

    def issue_code(self):
        """Generate a fresh 6-digit code, store its hash and return the plain code."""
        code = f'{secrets.randbelow(10**6):06d}'
        self.code_hash = _hash_code(code)
        self.attempts = 0
        self.sent_at = timezone.now()
        self.save(update_fields=['code_hash', 'attempts', 'sent_at'])
        return code

    @property
    def is_expired(self):
        return not self.sent_at or timezone.now() > self.sent_at + self.CODE_TTL

    @property
    def resend_available_in(self):
        if not self.sent_at:
            return 0
        left = (self.sent_at + self.RESEND_COOLDOWN - timezone.now()).total_seconds()
        return max(0, int(left))

    def check_code(self, code):
        """Return (ok, error_message). Counts failed attempts."""
        if self.is_expired:
            return False, str(_('This code has expired. Request a new one.'))
        if self.attempts >= self.MAX_ATTEMPTS:
            return False, str(_('Too many attempts. Request a new code.'))
        if not hmac.compare_digest(self.code_hash, _hash_code(code or '')):
            self.attempts += 1
            self.save(update_fields=['attempts'])
            left = self.MAX_ATTEMPTS - self.attempts
            if left <= 0:
                return False, str(_('Too many attempts. Request a new code.'))
            return False, ngettext(
                'Wrong code. %(left)d attempt left.',
                'Wrong code. %(left)d attempts left.',
                left,
            ) % {'left': left}
        return True, ''
