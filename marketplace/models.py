import os
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def marketplaceDirectoryPath( instance, filename ):
  bannerName = 'marketplace/products/{0}/{1}'.format( instance.name, filename )
  fullPath = os.path.join( settings.MEDIA_ROOT, bannerName )
  
  if os.path.exists( fullPath ):
    os.remove( fullPath )
  
  return bannerName


# Create your models here.
class Product( models.Model ):
  user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="products" )
  name = models.CharField( max_length= 100 )
  description = models.TextField()
  thumbnail   = models.ImageField(blank=True, null=True, upload_to=marketplaceDirectoryPath)
  slug = models.SlugField( unique=True )
  
  content_url = models.URLField( blank=True, null=True )
  content_file = models.FileField( blank=True, null=True )
  
  active = models.BooleanField( default= False )
  price  = models.PositiveIntegerField( default = 100 ) #cents can be lower than 50 centens
  
  def __str__(self):
    return self.name
  
  def price_display( self ):
    return "{0:.2f}".format( self.price / 100 )



class PurchasedProduct( models.Model ):
  email   = models.EmailField()
  product = models.ForeignKey( Product, on_delete=models.CASCADE )
  date_purchase = models.DateTimeField( auto_now_add = True)
  
  def __str__(self):
    return self.email
  