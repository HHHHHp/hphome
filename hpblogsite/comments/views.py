from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm
from blog.models import Post
from .forms import CommentForm
from django.views.decorators.http import require_POST


# Create your views here.


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        
        comment.post = post
        
        comment.save()
    # context = {
    #     "post":post,
    #     "form":form,
    #     "is_valid":False,
    # }
    return redirect(post)
    
    # return render(request,"comments/",context=context)
    
    pass