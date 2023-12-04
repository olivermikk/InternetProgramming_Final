from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='images')


    # Add other fields as needed for your product model

    def __str__(self):
        return self.name
