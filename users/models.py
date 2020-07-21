from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    user_bio = models.TextField(null=True)
    country = CountryField(blank=True, null=True)
    gender = models.CharField(
        max_length=140,
        null=True,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        )
    )
    birth_date = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=True)
    receive_emails= models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.user.username}
        )

    def natural_key(self):
        return (self.user.username, self.user.pk)

    class Meta:
        permissions = (
            ('special_access', 'Can access the special page'),
        )


class ProfileRelation(models.Model):
    user_profile_1 = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='profile1'
    )
    user_profile_2 = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='profile2'
    )
    relation_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Relation b/w {self.user_profile_1} and {self.user_profile_2}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user_profile_1', 'user_profile_2'),
                name='profile_relations'
            )
        ]
