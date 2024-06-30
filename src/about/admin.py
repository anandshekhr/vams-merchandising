from django import forms
from django.contrib import admin
from .models import *
# Register your models here.

class VcReviewForm(forms.ModelForm):
    avatar = forms.FileField(required=False)
    

    def save(self, commit=True):
        if self.cleaned_data.get('avatar') is not None \
                and hasattr(self.cleaned_data['avatar'], 'file'):
            data = self.cleaned_data['avatar'].file.read()
            self.instance.avatar = data
        
        return self.instance

    def save_m2m(self):
        # FIXME: this function is required by ModelAdmin, otherwise save process will fail
        pass

@admin.register(VCReview)
class VCReviewAdmin(admin.ModelAdmin):
    form = VcReviewForm
    list_display: list = ('username', 'designation', 
                          'active','scheme_image_tag')
