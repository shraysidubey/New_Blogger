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
        url(r'^follows/(?P<userprofile_id>[\w\-]+)/(?P<loggedin_userprofile_id>[\w\-]+)/$', views.follow, name='follow'),
        url(r'^Like/(?P<user_id>[\w\-]+)/(?P<blog_id>[\w\-]+)/$', views.like_blog, name='like_blog'),
        url(r'^delete/(?P<comment_id>[\w\-]+)/(?P<blog_slug>[\w\-]+)/$', views.delete_comment, name='delete_comment'),
)