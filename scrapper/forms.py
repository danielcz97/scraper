from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='URL strony')

from .models import  Product
from .models import Category, UserProfile

# class CategoryPreferenceForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['preferred_categories']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         categories = Product.objects.values_list('category', flat=True).distinct()
#         choices = [(cat, cat) for cat in categories]
#         self.fields['preferred_categories'] = forms.MultipleChoiceField(
#             choices=choices, widget=forms.CheckboxSelectMultiple, required=False)

#     def save(self, *args, **kwargs):
#         # Przy zapisie, konwertuj listę na ciąg znaków
#         self.instance.preferred_categories = ','.join(self.cleaned_data['preferred_categories'])
#         super().save(*args, **kwargs)
class UserCategoryForm(forms.ModelForm):
    preferred_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ['preferred_categories']