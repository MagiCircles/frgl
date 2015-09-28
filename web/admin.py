from django.contrib import admin
from web import models

admin.site.register(models.Card)
admin.site.register(models.Performer)
admin.site.register(models.UserPreferences)
admin.site.register(models.Account)
admin.site.register(models.UserLink)
admin.site.register(models.OwnedCard)
admin.site.register(models.Activity)

