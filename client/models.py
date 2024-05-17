from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from photographer.models import Package   


class ClientManager(BaseUserManager):
    def create_user(self, name, phone, email, password=None, is_client=False,is_staff=False,is_superuser=False, is_photographer=False, is_admin=False):
        if not email:
            raise ValueError('Clients must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            is_client=is_client,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_photographer=is_photographer,
            is_admin=is_admin,
        )   

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            phone=phone,
            is_admin=True,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Client(AbstractBaseUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_client = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_photographer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

class HiringDetails(models.Model):
    package = models.ForeignKey('photographer.Package', on_delete=models.CASCADE)
    # photographer_id = models.ForeignKey('photographer.Package', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Using string reference
    client_name = models.CharField(max_length=100)
    client_email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    starting_date = models.DateField()
    detail_message = models.TextField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.client_name} hiring {self.package_id.photographerName}"