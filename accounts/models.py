import uuid
from datetime import timezone

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, GroupManager, Permission

from .managers import AccountManager

class AccountRole(models.Model):
    """
    AccountRole like Group model. However, instead of Group we have roles which user have
    """
    role_name = models.CharField("role name", max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
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

class AccountPermission(models.Model):
    """
    Add the fields and methods necessary to support the Role and Permission
    models using the ModelBackend.
    """
    roles = models.ManyToManyField(
        AccountRole,
        verbose_name='account role',
        blank=True,
        related_name="accountuser_set",
        related_query_name="accountuser",
    )
    account_permissions = models.ManyToManyField(
        Permission,
        verbose_name='account permission',
        blank=True,
        related_name="accountuser_set",
        related_query_name="accountuser",
    )
    
    class Meta:
        abstract = True

    def get_account_permissions(self, obj=None):
        """
        Return a list of permission strings that this account has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "group")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

class AccountUser(AbstractBaseUser, AccountPermission):
    uuid = models.UUIDField('Public identifier', unique=True, editable=False, default=uuid.uuid4)
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

    managers = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def __str__(self) -> str:
        return self.uuid

    def get_full_name(self):
        return self.first_name + " " + self.last_name