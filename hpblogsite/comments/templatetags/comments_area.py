# -*- coding: UTF-8 -*-
# by Hp

from django import template
from ..forms import CommentForm
from blog.models import Post

register = template.Library()

@register.inclusion_tag('comments/inclusions.html',takes_context=True)
def show_comment_form(context,post,form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post
    }

@register.inclusion_tag("comments/comment_list.html",takes_context=True)
def show_comments(context,post):
    comment_list = post.comment_set.all().order_by("-created_time")
    comment_count = comment_list.count()
    
    return {
        "comment_list": comment_list,
        "comment_count": comment_count,
    }
@register.inclusion_tag("comments/comments_count.html",takes_context=True)
def show_comments_count(context,post):
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        "comment_count": comment_count,
    }