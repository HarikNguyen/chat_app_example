import uuid
from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, GroupManager

from .managers import EmployeeManager

class EmployeeRole(models.Model):
    """
    AccountRole like Group model. However, instead of Group we have roles which user have
    """
    role_name = models.CharField("role name", max_length=150, unique=True)
    permissions = models.ManyToManyField(
        PermissionsMixin,
        verbose_name="permissions",
        blank=True,
    )
    roles = GroupManager()

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Employee(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField('Public identifier', unique=True, editable=False, default=uuid.uuid4)
    employee_number = models.CharField(max_length=30,unique=True)
    first_name = models.TextField(max_length=100, blank=True)
    last_name = models.TextField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(verbose_name='email', unique=True)
    avatar = models.ImageField()
    country = models.TextField(max_length=200)
    province = models.TextField(max_length=200)
    district = models.TextField(max_length=200)
    ward = models.TextField(max_length=200)
    street = models.TextField(max_length=200)
    date_joined = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, verbose_name='user is activated')
    is_delete = models.BooleanField(default=False, verbose_name='user is deleted')
    created_by = models.EmailField()
    modified_by = models.EmailField()

    managers = EmployeeManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "employee_number"
    REQUIRED_FIELDS = ["email"]
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def __str__(self) -> str:
        return self.uuid

    def get_full_name(self):
        return self.first_name + " " + self.last_name