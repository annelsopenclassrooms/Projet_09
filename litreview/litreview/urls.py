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
    #path('home/', reviews.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket-post/', reviews.views.ticket_post, name='ticket_post'),
    path('flux/', reviews.views.flux, name='flux'),
    path('posts/', reviews.views.posts, name='posts'),
    path('subscribe/', reviews.views.subscribe, name='subscribe'),
    path('logout/', reviews.views.logout_view, name='logout'),
    path('ticket-edit/<int:ticket_id>/', reviews.views.ticket_edit, name='ticket_edit'),
    path('ticket-delete/<int:ticket_id>/', reviews.views.ticket_delete, name='ticket_delete'),
    path('review-post/', reviews.views.review_post, name='review_post'),
    path('review-delete/<int:review_id>/', reviews.views.review_delete, name='review_delete'),
    path('review-edit/<int:review_id>/', reviews.views.review_edit, name='review_edit'),
    path('unfollow_user/<int:user_id>/', reviews.views.unfollow_user, name='unfollow_user'), 
    path('create-ticket-and-review/', reviews.views.create_ticket_and_review, name='create_ticket_and_review'),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



