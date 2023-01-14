from django.contrib import admin
from .models import Minister, Content, Events

# Register your models here.

admin.site.register((Minister, Content, Events))