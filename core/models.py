from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClothingItem(models.Model):
    CATEGORY_CHOICES = [
        ('TOP', 'Top / Shirt'),
        ('BOTTOM', 'Bottom / Pants'),
        ('FOOTWEAR', 'Footwear / Shoes'),
        ('OUTERWEAR', 'Outerwear / Coat / Blazer'),
    ]
    
    COLOR_CHOICES = [
        ('NEUTRAL', 'Neutral (Black, White, Grey, Navy)'),
        ('WARM', 'Warm (Red, Yellow, Brown, Beige)'),
        ('COOL', 'Cool (Blue, Green, Purple)'),
    ]
    
    FORMALITY_CHOICES = [
        (3, 'Sharp Corporate (Monday Style)'),
        (2, 'Smart Casual (Mid-Week Style)'),
        (1, 'Casual Professional (Friday Style)'),
    ]

    WEATHER_CHOICES = [
        ('SUNNY', 'Sunny / Hot'),
        ('RAINY', 'Rainy / Wet'),
        ('COLD', 'Cold / Chilly'),
        ('ALL', 'All-Weather / Versatile'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='closet')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    color_category = models.CharField(max_length=15, choices=COLOR_CHOICES)
    formality_level = models.IntegerField(choices=FORMALITY_CHOICES)
    weather_suitability = models.CharField(max_length=15, choices=WEATHER_CHOICES, default='ALL')
    in_laundry = models.BooleanField(default=False)
    last_worn = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"