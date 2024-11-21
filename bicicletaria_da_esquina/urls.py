from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('ordens_servico/', include('ordens_servico.urls')),
    path('estoque/', include('estoque.urls')),
    path('admin/', admin.site.urls),
]
