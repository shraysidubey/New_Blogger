from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self',symmetrical=False)
    alias = models.CharField(max_length=128, null=False, unique=True)

    def __unicode__(self):
        return self.user.username


class blog(models.Model):
    title = models.CharField(max_length=128, unique=True)
    created_by = models.ForeignKey(UserProfile)
    body = models.CharField(max_length=5000)
    slug = models.SlugField(null=False)
    views = models.IntegerField(default=0)
    likedBy = models.ManyToManyField(UserProfile, related_name='likes', symmetrical=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Comment_on_blog(models.Model):
    comment = models.CharField(max_length=500)
    blogg = models.ForeignKey(blog,null=False)
    user = models.ForeignKey(UserProfile,null=False)

    def __unicode__(self):
        return self.comment
