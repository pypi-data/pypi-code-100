from django.urls import include, path


app_name = 'report_designer'


urlpatterns = [
    path('tables/', include('report_designer.tables.urls', namespace='tables')),
    path('formats/', include('report_designer.formats.urls', namespace='formats')),
    path('groups/', include('report_designer.groups.urls', namespace='groups')),
    path('reports/', include('report_designer.reports.urls', namespace='reports')),
]
