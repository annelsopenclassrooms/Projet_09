"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

import authentication.views
import reviews.views

from django.conf import settings
from django.conf.urls.static import static

import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', reviews.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket-post/', reviews.views.post_ticket, name='post_ticket'),
    path('flux/', reviews.views.flux, name='flux'),
    path('posts/', reviews.views.posts, name='posts'),
    path('abonnements/', reviews.views.abonnements, name='abonnements'),
    path('logout/', reviews.views.logout_view, name='logout'),
    path('edit-ticket/<int:ticket_id>/', reviews.views.edit_ticket, name='edit_ticket'),
    path('delete-ticket/<int:ticket_id>/', reviews.views.delete_ticket, name='delete_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



