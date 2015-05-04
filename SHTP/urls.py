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

    #URL about User
    url(r'^users/register/$', 'users.views.register', name='user_register'),
    url(r'^users/save/$', 'users.views.save_user', name='save_user'),
    url(r'^users/captcha/$', 'users.views.refresh_captcha', name='refresh_captcha'),
    url(r'^users/login/$', 'users.views.user_login', name='user_login'),
    url(r'^users/logout/$', 'users.views.user_logout', name='user_logout'),
    url(r'^users/dashboard/$', 'users.views.dashboard',name='user_dashboard'),
    url(r'^users/$', 'users.views.index', name='user_index'),
                       
    #URL about goods
    url(r'^goods/list/(?P<filter_category>\d+)/', 'goods.views.list_goods', name='goods_list'),
    url(r'^goods/create/', 'goods.views.create_goods', name='goods_list'),
    url(r'^goods/(?P<goods_id>\d+)', 'goods.views.goods_details', name='goods_details'),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
