from django.contrib import admin
from .models import Name, User, Member, Question, Data, Search

# Register your models here.
admin.site.register(Name)
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Question)
admin.site.register(Data)
admin.site.register(Search)
