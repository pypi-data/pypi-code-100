from django.contrib import admin

from .models import ViewTrack


class ViewTrackAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "timestamp",
        "request_method",
        "request_url",
        "response_status_code",
    ]
    list_select_related = ["user"]
    date_hierarchy = "timestamp"
    search_fields = [
        "user__username",
        "request_method",
        "request_url",
        "response_status_code",
    ]
    raw_id_fields = ["user"]
    readonly_fields = ["timestamp"]
    show_full_result_count = False


admin.site.register(ViewTrack, ViewTrackAdmin)
