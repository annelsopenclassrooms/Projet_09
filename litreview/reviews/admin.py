from django.contrib import admin

# Register your models here.
from reviews.models import Ticket
from reviews.models import Review
from reviews.models import UserFollows

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)