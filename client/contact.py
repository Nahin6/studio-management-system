# client/models.py

from django.db import models
from photographer.models import Package  # Import the Package model from the photographer app
from client.models import Client  # Import the Package model from the photographer app

class HiringDetails(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    photographer_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)  # Using string reference
    client_name = models.CharField(max_length=100)
    client_email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    starting_date = models.DateField()
    detail_message = models.TextField()

    def __str__(self):
        return f"{self.client_name} hiring {self.package_id.photographerName}"
