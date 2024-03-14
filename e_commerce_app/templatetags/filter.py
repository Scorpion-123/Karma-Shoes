from django import template
import pickle
from datetime import datetime
from e_commerce_app.models import *

register = template.Library()

@register.filter
def calculate_range(min = 5):
    return range(min)


@register.filter
def get_shoes_from_binary(binary_data):
    data = pickle.loads(binary_data)
    return data

@register.filter
def get_weekday(current_time_instance):
    weekday_list = ['Monday', 'Tuesday', 'Wednessday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    return weekday_list[datetime.weekday(current_time_instance)]


@register.filter
def get_count_of_brands(brand_name):

    brand_count = 0
    if (brand_name == ''):
        brand_count = Shoe.objects.all()
    else:
        brand_count = Shoe.objects.filter(brand__brand_name = brand_name)

    return len(brand_count)



# Note: Create a filter tag and register it, and also don't forget to load the filter tag in the template that you're going to use.
# syntax {% load filename %} 