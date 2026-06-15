from django import forms
from .models import ClothingItem

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        # We let users specify everything except the owner user profile and the image URL
        fields = ['name', 'category', 'color_category', 'formality_level', 'weather_suitability', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply unified Tailwind styles to all our selector fields dynamically
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition text-sm bg-white'
            })