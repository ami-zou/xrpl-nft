from django.db import models

# Create your models here.
class FileModel(models.Model):
 
    title = models.CharField(max_length = 80)
    description = models.TextField(max_length = 200)
    metadata = models.CharField(max_length = 100)
    file = models.FileField(upload_to='files/')
    
    class Meta:
        ordering = ['title']
     
    def __str__(self):
        return f"{self.title}"