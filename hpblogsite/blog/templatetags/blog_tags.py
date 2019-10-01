# -*- coding: UTF-8 -*-
# by Hp

from ..models import Post,Tag,Category
from django import template

register = template.Library()

@register.simple_tag
def get_tags():
    return Tag.objects.all()

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_most_view_post():
    return Post.objects.all().order_by('-views')[:5]

