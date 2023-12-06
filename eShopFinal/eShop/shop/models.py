from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# ADDED TO DEAL WITH SLUG ISSUES
class YourModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True)
    
    def __str__(self):
        return f"{self.name} {self.description} {self.price} {self.category} {self.image}"

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(choices=((1, '1 stars'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')))
    
    class Meta:
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.product}"
    
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')

    def __str__(self):
        return f"Cart for {self.user.username}"

    



