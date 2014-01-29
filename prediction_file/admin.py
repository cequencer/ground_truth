from prediction_file.models import PredictionFile
from django.contrib import admin

class PredictionFileAdmin(admin.ModelAdmin):
    list_display=('researcher', 'version',)

admin.site.register(PredictionFile, PredictionFileAdmin)