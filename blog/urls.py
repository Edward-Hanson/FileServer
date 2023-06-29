from django.urls import path
from .views import listfiles, download, query_set, send_email,detailfile,upload

urlpatterns = [
    path('',listfiles,name='list'),
    path('detail/<int:pk>/',detailfile, name= 'detail'),
    path('files/download/<int:file_id>/', download, name='file_download'),
    path('results/',query_set,name='search_results'),
    path('blog/detail/<int:pk>/',send_email, name='share_mail'),
    path('blog/upload',upload,name='upload'),

]