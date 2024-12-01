from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler403
from django.shortcuts import render


urlpatterns = [
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('ordens_servico/', include(('ordens_servico.urls', 'ordens_servico'), namespace='ordens_servico')),
    path('estoque/', include(('estoque.urls', 'estoque'), namespace='estoque')),
    path('admin/', admin.site.urls),
]


def custom_403_view(request, exception=None):
    return render(request, 'accounts/403.html', {
        'mensagem': "Você não tem permissão para acessar esta funcionalidade."
    }, status=403)

handler403 = custom_403_view