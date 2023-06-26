from django.db import models
import os

# Create your models here.
class FilesAdmin(models.Model):
    adminupload= models.FileField(upload_to='media/')
    title = models.CharField(max_length=50)
    description = models.TextField()
    downloadcount = models.IntegerField(default=0,blank=True)
    emailcount= models.IntegerField(default=0,blank=True)
    
    def get_file_type(self):
        file_extension = os.path.splitext(self.adminupload.name)[1]
        file_type = file_extension.lower().lstrip('.')
        if file_type in ['jpg','png','gif','jpeg']:
            return 'image'
        elif file_type in ['mp4','mkv','webm']:
            return 'video'
        
        elif file_type == 'pdf':
            return 'pdf'
        elif file_type in ['mp3','wav','aac']:
            return 'audio'
        else:
            return None
        
    
    def __str__(self):
        return self.title