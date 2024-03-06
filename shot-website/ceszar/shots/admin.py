from django.contrib import admin
from .models import Gas, GasConfig, Shot, DiagnosticImage

# Register your models here.
admin.site.register(Gas)
admin.site.register(GasConfig)
admin.site.register(Shot)
admin.site.register(DiagnosticImage)
