from django.urls import path
from .views import listfiles, Download, preview_file, query_set, send_email,detailfile

urlpatterns = [
    path('list/',listfiles,name='file_home'),
    path('detail/<int:pk>/',detailfile, name= 'detail'),
    path('file/preview/<int:file_id>/',preview_file,name = 'file_preview'),
    path('files/download/<int:file_id>/', Download.as_view(), name='file-download'),
    path('results/',query_set,name='search_results'),
    path('send-email/<int:pk>/', send_email, name='send_email'),
]