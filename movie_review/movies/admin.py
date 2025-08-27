from django.contrib import admin
from.models import Comment, Rating,Movie

# Register your models here.
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Movie)