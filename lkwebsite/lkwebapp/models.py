from django.db import models

class lkModelType(models.Model):
# Create your models here.
    model_type=models.CharField(max_length=30)
    
    def __str__(self):
        return self.model_type


class lkModel(models.Model):
    title=models.CharField(max_length=50)
    model_type=models.ForeignKey(lkModelType,on_delete=models.DO_NOTHING)
    reques_parame=models.TextField()
    request_url=models.TextField()
    
    def __str__(self):
        return self.title
    

