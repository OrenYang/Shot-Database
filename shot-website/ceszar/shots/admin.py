from django.contrib import admin
from .models import Gas, GasConfig, Shot, XrayDetector, Filter, XuvImage, Schlieren, Interferometer, Spectrometer

# Register your models here.
admin.site.register(Gas)
admin.site.register(GasConfig)
admin.site.register(Shot)
admin.site.register(XrayDetector)
admin.site.register(Filter)
admin.site.register(XuvImage)
admin.site.register(Schlieren)
admin.site.register(Interferometer)
admin.site.register(Spectrometer)
