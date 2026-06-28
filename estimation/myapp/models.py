from django.db import models
from django.contrib.auth.models import User



class UserLogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} ({self.utype})"


# Extended user profile if needed
class UserProfile(models.Model):
    USER_TYPES = [
        ('user', 'user'),
        ('contractor', 'Contractor'),
        ('service provider', 'service provider'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Labour(models.Model):
    labour_head = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    number_of_workers = models.IntegerField()
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return self.labour_head


class ContractorInfo(models.Model):
    contractor_name = models.CharField(max_length=50)
    experience = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    document = models.FileField(upload_to='images/')
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.contractor_name


class ContractorRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    request_by = models.CharField(max_length=20)
    contractor = models.CharField(max_length=20)
    description = models.TextField(max_length=500)
    contact = models.CharField(max_length=15)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cost_estimation = models.IntegerField()

    def __str__(self):
        return f"Request by {self.request_by.username} to {self.contractor.contractor_name}"


class OTPCode(models.Model):
    otp_code = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.otp_code)


class MarketPrice(models.Model):
    raw_material = models.CharField(max_length=50)
    company_name = models.CharField(max_length=20)
    uom = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.raw_material} - {self.company_name}"


class UploadBlueprints(models.Model):
    construction_type = models.CharField(max_length=30)
    blueprint_title = models.CharField(max_length=100)
    approx_cost = models.CharField(max_length=50)
    image_1 = models.FileField(upload_to='images/')
    image_2 = models.FileField(upload_to='images/')

    def __str__(self):
        return self.blueprint_title




class SaleHouse(models.Model):
    SALE_STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    house_type = models.CharField(max_length=30)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    facilities = models.TextField(max_length=200)
    cost = models.IntegerField()
    added_by = models.CharField(max_length=100)
    sale_status = models.CharField(max_length=10, choices=SALE_STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.house_type} in {self.city}"

class HouseImage(models.Model):
    house = models.ForeignKey(SaleHouse, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_images/')



class BookRequest(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    house = models.ForeignKey(SaleHouse, on_delete=models.CASCADE)
    user = models.CharField(max_length=40,null=True,blank=True)
    contractor = models.CharField(max_length=40,null=True,blank=True)
    cost = models.IntegerField(null=True,blank=True)
    book_date = models.DateField(auto_now_add=True,null=True,blank=True)
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS_CHOICES, default='pending',null=True,blank=True)
    sale_status = models.CharField(max_length=10, choices=SaleHouse.SALE_STATUS_CHOICES, default='available',null=True,blank=True)

    def __str__(self):
        return f"Booking by {self.user.username}"


class ServiceProvider(models.Model):
    service_type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    pincode = models.IntegerField()
    contact = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.name} ({self.service_type})"


class UploadImage(models.Model):
    name = models.CharField(max_length=30)
    image = models.FileField(upload_to='images/')

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    user_id=models.CharField(max_length=100,null=True,blank=True)
    contractor=models.CharField(max_length=100,null=True,blank=True)
    request_date=models.DateField(auto_now_add=True,null=True,blank=True)
    message=models.CharField(max_length=1000,null=True,blank=True)
    request_status=models.CharField(max_length=100,default='pending',null=True,blank=True)
    reply = models.CharField(max_length=1000,null=True,blank=True)
