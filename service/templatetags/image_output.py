from django import template

register = template.Library()


# Создание тега
@register.simple_tag
def mymedia(data):
    if data:
        return f'/media/{data}'
    return '/media/blank.jpg'
