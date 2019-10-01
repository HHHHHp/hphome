# -*- coding: UTF-8 -*-
# by Hp
from django.urls import path
from . import views
from .views import Welcome,IndexPage,CategoryPage,TagPage,DetailPage,SearchPage
app_name = 'blog'
urlpatterns = [
    path('',Welcome.as_view(), name = 'welcome'),
    path('index/',IndexPage.as_view(), name='index'),
    path('post/<int:pk>',DetailPage.as_view(), name='detail'),
    path('category/<str:cat>', CategoryPage.as_view(), name='category'),
    path('tag/<str:t>',TagPage.as_view(),name='tag'),
    path('search/',SearchPage.as_view(),name='search'),
    path('increase_like',views.increase_like,name='like'),
]