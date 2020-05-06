#reference https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group

from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False