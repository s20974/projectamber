from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import UserManager
from django.conf import settings

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = None

    email = models.EmailField( verbose_name=_('email address'), max_length=255, unique=True, null=True)
    email_verified = models.BooleanField(default=False)

    phone = models.CharField(max_length=17, null=True, unique=True)
    phone_number_verified = models.BooleanField(default=False)

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    instance = 'email'
    if not phone:
        if email:
            instance = email
    if not email:
        if phone:
            instance = phone
            

    USERNAME_FIELD = instance
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def delete_user(self):
        self.User.delete()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{}'.format(self.get_full_name())


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True)

    def update_profile(request, user_id):
        user = User.objects.get(pk=user_id)
        user.save()
        verbose_name=_('user')

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

    def __self__(self):
        return self.user.first_name

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
