from django.contrib import admin
from .models import Users, Company, Geo, Address, Posts
# Register your models here.
admin.site.register(Geo)
admin.site.register(Users)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(Posts)
