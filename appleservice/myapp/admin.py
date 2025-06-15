from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *
from django.utils.html import format_html
import pprint

# Register your models here.refis
admin.site.register(Lokacja)
admin.site.register(Klient)
admin.site.register(Pracownik)
admin.site.register(Zlecenie)
admin.site.register(Usluga)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'decoded_data', 'expire_date']

    def decoded_data(self, obj):
        try:
            data = obj.get_decoded()
            return format_html("<pre>{}</pre>", pprint.pformat(data))
        except Exception as e:
            return f"Error decoding: {e}"

    decoded_data.short_description = 'Session Data'