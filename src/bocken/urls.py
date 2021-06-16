"""Bocken URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from bocken.admin import admin_site
from django.urls import include, path
from bocken import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.StartPage.as_view(), name='start-page'),
    path('admin/', admin_site.urls),
    path('add_entry/', include([
        path('', views.JournalEntryCreate.as_view(), name='add-entry'),
        path(
            'success',
            views.JournalEntryCreateSuccess.as_view(),
            name='add-entry-success'
        )
    ])),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
