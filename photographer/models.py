from django.db import models
from client.models import Client


class Package(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    photographerName = models.CharField(max_length=100)
    packageName = models.CharField(max_length=100)
    img = models.ImageField(upload_to='package_images/')
    cover_img = models.ImageField(upload_to='package_images/')
    duration = models.CharField(max_length=50)
    type = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.photographerName} - {self.duration}"
