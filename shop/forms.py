from django import forms
from .models import Product, Rating


class ImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image')
        
        


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }

    def as_custom_widget(self):
        return self['rating'].as_widget()