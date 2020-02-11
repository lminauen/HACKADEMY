from django.contrib import admin
from mainApp.models import attributesDefib, community, defibModels, items, type, UserProfileInfo

# Register your models here.

admin.site.register(attributesDefib)
admin.site.register(community)
admin.site.register(defibModels)
admin.site.register(items)
admin.site.register(type)
admin.site.register(UserProfileInfo)
