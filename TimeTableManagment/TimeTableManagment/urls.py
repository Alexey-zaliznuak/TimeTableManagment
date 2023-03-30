from django.contrib import admin
from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.generic.base import TemplateView, RedirectView


frontend = False


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('schema-swagger-ui')), name='index')
]

if frontend:
    urlpatterns += path(
        'frontend/',
        TemplateView.as_view(template_name='index.html'), name='frontend')
    urlpatterns += static(
        settings.STATIC_FRONTEND_URL,
        document_root=settings.STATIC_FRONTEND_ROOT
    )
