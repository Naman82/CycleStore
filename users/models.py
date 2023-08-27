from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = None
    USER_TYPE_CHOICES = [
        (0, 'Admin'),
        (1, 'Customer'),
    ]
    email = models.EmailField(_('email address'), unique=True, null=True)
    email_verified = models.BooleanField(default=False)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    objects = UserManager()

    def __str__(self):
        return "{},{},{}".format(self.email, self.first_name, self.type_value)

    def gettype(self):
        return self.user_type

    @property
    def type_value(self):
        return dict(self.USER_TYPE_CHOICES)[self.user_type]
