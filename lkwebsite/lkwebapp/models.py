from django.db import models

# Create your models here.
class lkModelType(models.Model):
    model_type=models.CharField(max_length=30)
    
    def __str__(self):
        return self.model_type


class lkModel(models.Model):
    title=models.CharField(max_length=50)
    model_type=models.ForeignKey(lkModelType,on_delete=models.DO_NOTHING)
    request_url=models.TextField()
    
    def __str__(self):
        return self.title
    

