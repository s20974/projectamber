from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, password, email=None, phone=None, **extra_fields):
        if not email:
            if not phone:
                raise ValueError(_('The given phone must be set'))
        if not phone:
            if not email:
                raise ValueError(_('The given email must be set'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
                
        if email:
            email = self.normalize_email(email)

        user = self.model(
            email = email,
            phone = phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, first_name, last_name, password=None, email=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, phone=phone, first_name=first_name, last_name=last_name, password=password, **extra_fields)


    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields)