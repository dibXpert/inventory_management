from django.db import models
from django.contrib.auth.models import User

# UserProfile to manage roles.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Inventory(models.Model):
    category = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255)
    
    #name
    def __str__(self):
        return  f"{self.sku} - {self.name}"
    
    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
    
class Inbound(models.Model):
    product_sku = models.ForeignKey(Inventory, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True,null=True)
    remarks = models.TextField(blank=True, null=True)
    date_received = models.DateField(null=True, blank=True)  # editable
    supplier_name = models.CharField(max_length=255)

    
    def __str__(self):
        return f"{self.product_sku.name} - {self.quantity} received"
    

class Outbound(models.Model):
    product_sku = models.ForeignKey(Inventory, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    destination = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True,null=True)
    remarks = models.TextField(blank=True, null=True)
    date_shipped =  models.DateField(null=True, blank=True)  # editable
    customer_name = models.CharField(max_length=255)
    
    def __str__(self):
        return (f"{self.product_sku.name} - {self.quantity} shipped")
    



