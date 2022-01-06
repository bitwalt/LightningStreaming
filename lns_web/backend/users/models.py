from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SEX_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )

    STATUS_CHOICE = (
        ('a', 'Active'),
        ('i', 'Inactive'),
        ('t', 'Terminated')
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICE, blank=True, null=True)
    age = models.DateField(null=True, blank=True)
    terms_agreement = models.BooleanField(default=True, blank=True)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE,
                              default=STATUS_CHOICE[0][0], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.email

    def get_all_expenses(self):
        return None

    def get_all_entries(self):
        return None

    class Meta:
        db_table = 'users'
