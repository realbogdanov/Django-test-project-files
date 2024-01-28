from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
        return "profile/{instance}/avatar/{filename}".format(
            instance=instance.user.username,
            filename=filename,
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=profile_avatar_directory_path, null=True, blank=True)
