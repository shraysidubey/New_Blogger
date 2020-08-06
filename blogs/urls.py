from django.conf.urls import patterns, url
from blogs import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^add_blog/$', views.add_blog, name='add_blog'),
        url(r'^user/(?P<alias>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^blog/(?P<blog_slug>[\w\-]+)/$', views.blog_detail, name='blog_detail'),
)