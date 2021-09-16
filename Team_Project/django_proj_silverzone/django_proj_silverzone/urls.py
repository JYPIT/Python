from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# 이미지 관리
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('silverzone/', include('silverzone.urls')),
    path('', RedirectView.as_view(pattern_name="main_page"), name="root"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
