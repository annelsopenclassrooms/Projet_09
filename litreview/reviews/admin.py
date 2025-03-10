# Register your models here.

from django.contrib import admin
from reviews.models import Ticket
from reviews.models import Review
from reviews.models import UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
