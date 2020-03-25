from django.db import models

# Create your models here.

class Books(models.Model):
    name=models.CharField(max_length=64,verbose_name='书名')

    class Meta:
        verbose_name='books'
        verbose_name_plural='books'

    def __str__(self):
        return self.name