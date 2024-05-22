from django.db import models

class Package(models.Model):
    user = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, blank=True)
    photographerName = models.CharField(max_length=100)
    packageName = models.CharField(max_length=100)
    img = models.ImageField(upload_to='package_images/')
    cover_img = models.ImageField(upload_to='package_images/')
    duration = models.CharField(max_length=50)
    type = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.photographerName} - {self.duration}"

class Income(models.Model):
    photographer = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} from {self.package.packageName if self.package else 'Expense'} by {self.photographer.username}"

    @classmethod
    def total_income_for_photographer(cls, photographer):
        total_credit = cls.objects.filter(photographer=photographer, transaction_type='credit').aggregate(total_income=models.Sum('credit'))['total_income'] or 0
        total_debit = cls.objects.filter(photographer=photographer, transaction_type='debit').aggregate(total_expense=models.Sum('debit'))['total_expense'] or 0
        return total_credit - total_debit
    @classmethod
    def total_send(cls, photographer):  
        total_debit = cls.objects.filter(photographer=photographer, transaction_type='debit').aggregate(total_expense=models.Sum('debit'))['total_expense'] or 0
        return total_debit
