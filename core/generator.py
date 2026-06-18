import random
from .models import ClothingItem

def get_random_item_for_slot(user, category, weather_suitability):
    """
    Queries the database for clothing matching a specific category,
    filters them based on the current day's weather condition,
    and returns one random selection.
    """
    # 1. Fetch items owned by this specific user in this clothing category
    queryset = ClothingItem.objects.filter(user=user, category=category)
    
    # 2. Apply weather filtering logic
    # If the day is COLD or HOT, we look for items matching that specific condition OR items tagged 'ALL'
    if weather_suitability in ['COLD', 'HOT']:
        filtered_queryset = queryset.filter(weather_suitability__in=[weather_suitability, 'ALL'])
    else:
        # If the day is mild ('ALL'), any item in the closet is technically fair game
        filtered_queryset = queryset

    # 3. Roll the dice!
    if filtered_queryset.exists():
        return random.choice(list(filtered_queryset))
    
    return None

def generate_weekly_wardrobe(user, schedule):
    """
    Loops through Monday-Friday, evaluates the forecast for each day,
    and assigns random matching clothing items to every open slot.
    """
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    categories = ['TOP', 'BOTTOM', 'SHOES', 'OUTERWEAR']

    # Iterate through each calendar day
    for day in days:
        # Fetch the day's pre-calculated weather string (e.g., 'ALL', 'COLD')
        day_weather = getattr(schedule, f"{day}_weather")
        
        # Roll an item for each category slot
        for category in categories:
            random_item = get_random_item_for_slot(user, category, day_weather)
            
            # Map categories to our specific database field names
            field_suffix = 'shoes' if category == 'SHOES' else category.lower()
            field_name = f"{day}_{field_suffix}"
            
            # Save the chosen clothing item reference directly into the schedule slot
            setattr(schedule, field_name, random_item)
            
    schedule.save()