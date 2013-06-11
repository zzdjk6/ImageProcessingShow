from django.db import models

class Operation(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100,blank=True,null=True)
    explain = models.TextField(blank=True,null=True)
    label = models.CharField(max_length=50,blank=True,null=True)
    
    def __unicode__(self):
        return ' '.join([self.name, self.url])