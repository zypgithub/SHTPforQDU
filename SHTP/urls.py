from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SHTP.views.home', name='home'),
    # url(r'^SHTP/', include('SHTP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #URL about Homepage


    #URL about User
    url(r'^users/register/$', 'users.views.register', name='user_register'),
    url(r'^users/save/$', 'users.views.save_user', name='save_user'),
    url(r'^users/captcha/$', 'users.views.refresh_captcha', name='refresh_captcha'),
    url(r'^users/login/$', 'users.views.user_login', name='user_login'),
    url(r'^users/logout/$', 'users.views.user_logout', name='user_logout'),
    url(r'^users/dashboard/$', 'users.views.dashboard',name='user_dashboard'),
    url(r'^users/$', 'users.views.index', name='user_index'),
    url(r'^users/modify/(?P<school_id>\d+)$', 'users.views.user_modify', name='user_modify'),
    url(r'^users/profile/(?P<school_id>\d+)$', 'users.views.user_profile', name='user_profile'),
    url(r'^users/changepsw/$', 'users.views.changepsw', name='changepsw'),
    url(r'^users/retrievepsw/$', 'users.views.retrievepsw', name='retrievepsw'),
   
                       
    #URL about goods
    url(r'^goods/list/(?P<filter_category>\d*)$', 'goods.views.list_goods', name='goods_list'),
    url(r'^goods/create/$', 'goods.views.create_goods', name='create_goods'),
    url(r'^goods/delete/(?P<goods_id>\d+)$', 'goods.views.delete_goods', name='delete_goods'),
    url(r'^goods/(?P<goods_id>\d+)$', 'goods.views.goods_details', name='goods_details'),
    url(r'^goods/modify/(?P<goods_id>\d+)$', 'goods.views.modify_goods', name='modify_goods'),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
