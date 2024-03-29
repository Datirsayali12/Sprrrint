from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# from Learn.models import Course,Video,Ebook


# Create your models here.

# -----------------For product---------------------------------

class Category(models.Model):  # Changed to inherit from models.Model
    name = models.CharField(max_length=255, unique=True, help_text="this will store category name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):  # Changed to inherit from models.Model
    name = models.CharField(max_length=255, help_text="this will store sub category name")
    categories = models.ManyToManyField(Category)  # Corrected ManyToManyField to ManyToManyField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, help_text="this for tag name")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    type = models.CharField(max_length=100, unique=True,
                            help_text="this will store product type like: single, pack, kit,template")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.type


class AssetType(models.Model):
    type = models.CharField(max_length=255, help_text="this will store Asset type like:jpg,png,mp4 ")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.type


class Product(models.Model):
    title = models.CharField(max_length=255, help_text="this will store product title")
    credits = models.IntegerField(help_text="this for credits")
    # hero_image_url = models.URLField(help_text="for product_card main image") # s3 bucket file url
    creator = models.ForeignKey(User, on_delete=models.CASCADE, help_text="this for creator of product")
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, help_text="for sub_category of product")
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                     help_text="for type of product i.e single ,pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)
    no_of_items = models.IntegerField()
    

    def __str__(self):
        return self.title


class Asset(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL,
                                help_text="this indicate that asset relate to particular product")
    asset = models.URLField(help_text="for product asset URLs")
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE,
                                   help_text='This will store file like - jpg, mp4')
    meta_tag = models.CharField(max_length=255, help_text="meta description/tag etc for seo")
    is_hero = models.BooleanField(help_text="to check if asset is hero image or video")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="this refer particular user that saved items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                help_text="this refers particular product that saved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="refer to user that download product")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="refer to product that download")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SortType(models.Model):
    name = models.CharField(max_length=100, help_text="for type of sort like relevant, popular etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# ------------------------------------------------------

# -------------for billing and payment--------------------------

class BillingType(models.Model):
    name = models.CharField(max_length=255, help_text="type of billing i.e renewal etc ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BillingHistory(models.Model):
    billing_type = models.ForeignKey(BillingType, on_delete=models.CASCADE, help_text="refer to billingType table")
    amount = models.FloatField(help_text="for billing amount")
    invoice = models.URLField(help_text="for Invoice PDFs")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="refer to user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="for refer user")
    card_number = models.BigIntegerField(help_text="for card number")
    expiry_date = models.DateField(help_text="for card expiary date")
    security_code = models.CharField(max_length=4, help_text="cvv code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Country(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=56)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=256)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BillingPersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="for refer user")
    first_name = models.CharField(max_length=100, help_text="for first name")
    last_name = models.CharField(max_length=100, help_text="for last name")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text="for country name")
    address1 = models.TextField(max_length=200, help_text="for address1")
    address2 = models.TextField(blank=True, null=True, help_text="for address2")
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text="for city name")
    state = models.ForeignKey(State, on_delete=models.CASCADE, help_text="for state")
    postal_code = models.IntegerField(help_text="for postal code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionType(models.Model):
    name = models.CharField(max_length=255, help_text="for transaction type i.e sale,purchasse etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductTransaction(models.Model):
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        help_text="for credit amount of product")
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       help_text="for debit amount record for product")
    tran_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
                                  help_text="refer transaction type i.e purchase ,sale etc.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="refer particular user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                help_text="for refer product", )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# -----------------------------------------


