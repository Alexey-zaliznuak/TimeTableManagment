from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('frontend/', TemplateView.as_view(template_name='index.html'), name='frontend')
]

urlpatterns += static(settings.STATIC_FRONTEND_URL, document_root=settings.STATIC_FRONTEND_ROOT)
