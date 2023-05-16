from django.contrib import admin

from .models import BaseForm, WordForm

# Register your models here.
admin.site.register(BaseForm)
admin.site.register(WordForm)
