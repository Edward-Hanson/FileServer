from django.db import models

# Create your models here.
class FilesAdmin(models.Model):
    adminupload= models.FileField(upload_to='media')
    title = models.CharField(max_length=50)
    description = models.TextField()
    downloadcount = models.IntegerField(default=0,blank=True)
    emailcount= models.IntegerField(default=0,blank=True)
    
    
    def __str__(self):
        return self.title