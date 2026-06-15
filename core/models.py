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
    image = models.ImageField(upload_to='closet_items/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class WeeklySchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    week_start_date = models.DateField(help_text="The Monday date representing this specific week")
    created_at = models.DateTimeField(auto_now_add=True)

    # --- MONDAY SLOTS ---
    monday_top = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='monday_tops')
    monday_bottom = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='monday_bottoms')
    monday_shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='monday_footwear')
    monday_outerwear = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='monday_coats')
    monday_weather = models.CharField(max_length=100, blank=True, null=True, default="Awaiting forecast...")
    monday_confirmed = models.BooleanField(default=False)

    # --- TUESDAY SLOTS ---
    tuesday_top = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='tuesday_tops')
    tuesday_bottom = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='tuesday_bottoms')
    tuesday_shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='tuesday_footwear')
    tuesday_outerwear = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='tuesday_coats')
    tuesday_weather = models.CharField(max_length=100, blank=True, null=True, default="Awaiting forecast...")
    tuesday_confirmed = models.BooleanField(default=False)

    # --- WEDNESDAY SLOTS ---
    wednesday_top = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='wednesday_tops')
    wednesday_bottom = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='wednesday_bottoms')
    wednesday_shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='wednesday_footwear')
    wednesday_outerwear = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='wednesday_coats')
    wednesday_weather = models.CharField(max_length=100, blank=True, null=True, default="Awaiting forecast...")
    wednesday_confirmed = models.BooleanField(default=False)

    # --- THURSDAY SLOTS ---
    thursday_top = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='thursday_tops')
    thursday_bottom = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='thursday_bottoms')
    thursday_shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='thursday_footwear')
    thursday_outerwear = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='thursday_coats')
    thursday_weather = models.CharField(max_length=100, blank=True, null=True, default="Awaiting forecast...")
    thursday_confirmed = models.BooleanField(default=False)

    # --- FRIDAY SLOTS ---
    friday_top = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='friday_tops')
    friday_bottom = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='friday_bottoms')
    friday_shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='friday_footwear')
    friday_outerwear = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='friday_coats')
    friday_weather = models.CharField(max_length=100, blank=True, null=True, default="Awaiting forecast...")
    friday_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'week_start_date')
        ordering = ['-week_start_date']

    def __str__(self):
        return f"Week of {self.week_start_date} for {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField(max_length=100, default='Nairobi', help_text="City name for accurate weather forecasts")
    receive_evening_alerts = models.BooleanField(default=True, help_text="Toggle to receive tomorrow's outfit email at 8:00 PM")
    
    def __str__(self):
        return f"Profile for {self.user.username}"