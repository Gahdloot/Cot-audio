from django.db import models
from .validator import validate_file_extension
from cloudinary_storage.storage import VideoMediaCloudinaryStorage


# Create your models here.


class Minister(models.Model):
    content_type = [
        ('song', 'song'),
        ('message', 'message'),
        ('presentation', 'presentation'),

    ]
    name = models.CharField(max_length=240, null=False, blank=False)
    publish = models.IntegerField(default=0)
    content = models.CharField(
        max_length=15,
        choices=content_type,
        default='presentation', )
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images/author/')
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Events(models.Model):
    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    times_played = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Content(models.Model):
    minister = models.ForeignKey(Minister, on_delete=models.CASCADE, related_name='minister')
    name = models.CharField(max_length=240, null=False, blank=False)
    content = models.FileField(upload_to='content/audio', validators=[validate_file_extension],
                               storage=VideoMediaCloudinaryStorage, null=True, blank=True)
    image = models.ImageField(upload_to='content/images')
    # change to set to null for on delete
    tag = models.ForeignKey(Events, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField()
    times_played = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        minister__ = Minister.objects.get(id=self.author.id)
        minister__.publish += 1
        minister__.save()
        return super().save(*args, **kwargs)

    def event_name(self):
        return f'{self.tag.name}'

    def minister_name(self):
        return f'{self.minister.name}'

    def __str__(self):
        return f'{self.name}'