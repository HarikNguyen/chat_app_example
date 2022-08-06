"""
Django manager is a class that acts as an interface through which Django models interact with databases.
Every model has at least one manager object. It has a lot of methods, attributes to ease working with databases.
In fact, the default Manager object that Django provides in models is “objects“.
To use it, what needed is run the command like <model_name>.objects.<method_name>

So these code in below to show all Account Managers's method of Account Models. Such as create user...

How to use this?
It simply adds property like this (objects = Account Manager but "manager_name" can substitute for "objects")
"""

from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.contrib import auth

class EmployeeManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        # Get a Global user model which registed
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        # Normalize username using a AbstractBaseUser's classmethod which applies NFCK 
        # Unicode normalization to usernames so that visually identical characters with 
        # different Unicode code points are considered identical.
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    