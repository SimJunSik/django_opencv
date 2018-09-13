from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
#router.register(r'versions', views.VersionViewSet)
#router.register(r'users', views.UserViewSet)
router.register(r'thumbnail', views.ThumbnailViewSet, base_name='thumbnail')
router.register(r'getframe', views.GetframeViewSet, base_name='getframe')
router.register(r'clients', views.ClientViewSet)
router.register(r'post', views.PassIdViewSet)

"""
thumbnail = views.ThumbnailViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
"""

"""
snippet_detail = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
"""

 
urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^$', views.index),
    
    #url(r'^thumbnail/', csrf_exempt(views.ThumbnailViewSet), name = 'thumbnail'),
    #url(r'^thumbnail/.+$', views.ThumbnailViewSet, name = 'thumbnail'),
    url(r'^v_list/$', views.version_list),
    #url(r'^test/$', views.test_list),
    url(r'^video_test/$', views.video_get_frame),
    url(r'^stream/$', views.stream_test),
    url(r'^api-v1/', include('rest_framework.urls', namespace='rest_framework_category')),

    url(r'^test/.+$', views.upload_file),
    url(r'^test2/.+$',views.show_file),
    url(r'^friendadd/.+$',views.friend_add),
    url(r'^friendadd2/.+$',views.friend_list),
    url(r'^friendadd/',views.friend_add),
    #url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^friendlist/', views.friend_list),
    url(r'^ajaxpass/', views.ajaxpass),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
urlpatterns = [
	url(r'^$', views.index),
	url(r'^opencv/', views.opencv),
]
"""