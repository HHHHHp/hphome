from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Post, Category, Tag
import markdown
from django.core.paginator import Paginator
# Create your views here.
from django.db.models import Q
from django.http.response import JsonResponse

from django.views.generic import ListView, TemplateView, DetailView


class Welcome(TemplateView):
    template_name = 'blog/welcome.html'


class IndexPage(ListView):
    model = Post
    template_name = 'blog/new_index.html'
    context_object_name = 'articles'
    paginate_by = 4
    
    def get(self, request, *args, **kwargs):
        a = request.META.get('HTTP_USER_AGENT')
        if 'Mobile' in a:
            self.mobile = 1
        else:
            self.mobile = 0
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({'mobile': self.mobile})
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get("is_paginated")
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context
    
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            
            if left[0] > 1:
                first = True
        
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            
            if right[-1] < total_pages:
                last = True
            
            if left[0] > 2:
                left_has_more = True
            
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }
        return data


class SearchPage(IndexPage):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('search')
        a = request.META.get('HTTP_USER_AGENT')
        if 'Mobile' in a:
            self.mobile = 1
        else:
            self.mobile = 0
        self.object_list = Post.objects.filter(Q(title__contains=keyword) | Q(excerpt__contains=keyword))
        context = self.get_context_data()
        print(context)
        return self.render_to_response(context)
    
    # def get_queryset(self):
    #
    #     print(self.keyword)
    #     return super(SearchPage,self).get_queryset().filter(Q(title__icontains=self.keyword)|Q(body__icontains=self.keyword))


class CategoryPage(IndexPage):
    model = Post
    template_name = 'blog/new_category.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        cat = get_object_or_404(Category, name=self.kwargs.get('cat'))
        print(cat)
        return super(CategoryPage, self).get_queryset().filter(category=cat)


class TagPage(IndexPage):
    model = Post
    template_name = 'blog/new_tag.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        t = get_object_or_404(Tag, name=self.kwargs.get('t'))
        return super(TagPage, self).get_queryset().filter(tags=t)


class DetailPage(DetailView):
    model = Post
    template_name = 'blog/new_detail.html'
    context_object_name = 'article'
    
    def get(self, request, *args, **kwargs):
        a = request.META.get('HTTP_USER_AGENT')
        if 'Mobile' in a:
            self.mobile = 1
        else:
            self.mobile = 0
        response = super(DetailPage, self).get(request, *args, **kwargs)
        
        self.object.increase_views()
        
        return response
    
    def get_object(self, queryset=None):
        post = super(DetailPage, self).get_object(queryset=None)
        post.body = markdown.markdown(
            post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        
        return post
    
    def get_context_data(self, **kwargs):
        context = super(DetailPage, self).get_context_data(**kwargs)
        tag = Tag.objects.all()
        category = Category.objects.all()
        context.update({"tags": tag, "categories": category, 'mobile': self.mobile})
        return context


def increase_like(request):
    if request.method == 'GET':
        post_id = request.GET.get("id")
        article_obj = Post.objects.filter(id=post_id)[0]
        article_obj.like += 1
        article_obj.save()
        return JsonResponse({'like': str(article_obj.like)})


