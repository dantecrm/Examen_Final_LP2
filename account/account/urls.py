from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from userprofile.views import UserProfileList, UserProfileDetail, UserProfileUpdate, UserProfileDelete
from userprofile import views
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    # Examples:
    # url(r'^$', 'project_name.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$', LoginIn.as_view(), name='login'),
    url(r'^userprofile/list/$', UserProfileList.as_view(), name='user_profile_list'),
    url(r'^userprofile/detail(?P<pk>\d+)$', UserProfileDetail.as_view(), name='user_profile_detail'),
    # url(r'^userprofile/create/$', UserProfileCreate.as_view(), name='user_profile_create'),
    url(r'^userprofile/update(?P<pk>\d+)$', UserProfileUpdate.as_view(), name='user_profile_update'),
    url(r'^userprofile/delete(?P<pk>\d+)$', UserProfileDelete.as_view(), name='user_profile_delete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.Cerrar, name='logout'),
    url(r'^usuarios/$', views.Usuarios, name='usuarios'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
    )
