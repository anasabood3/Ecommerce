from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import UserBase
from .unique_slugify import unique_slugify
from django_resized import ResizedImageField


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )

    cover = ResizedImageField(
        size=[1080, 1920],
        crop=['top', 'left'],
        verbose_name=_("image"),
        help_text=_("Upload an Offer image"),
        upload_to="images/",
        default="images/default.png",
    )

    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True,blank=True, related_name="children")
    
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    # Management URLS
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def get_management_url(self):
        return reverse("management:edit_category", args=[self.slug])
        
    def get_delete_url(self):
        return reverse("management:delete_category",args=[self.slug])

    def save(self,*args, **kwargs):
        unique_slugify(self,self.name)
        super().save(*args, **kwargs)


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name

    # Management URLs
    def get_edit_url(self):
        return reverse("management:edit_product_type",args=[self.pk]) 
    def get_delete_url(self):
        return reverse("management:delete_product_type",args=[self.pk])

class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table contining all product items.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="user_wishlist",blank=True)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return self.title

    # Management URLs
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def get_management_url(self):
        return reverse("management:edit_product", args=[self.slug])
    
    def get_delete_url(self):
        return reverse("management:delete_product",args=[self.slug])

    def added_to_wishlist(self,user_id):
        product_state = (Product.users_wishlist.through.objects.filter(product_id = self.id, userbase_id = user_id).exists())
        return product_state

    def save(self,*args, **kwargs):
        unique_slugify(self,self.title)
        super().save(*args, **kwargs)

    
    

class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """
# ,limit_choices_to={'id__in':list(ProductSpecification.objects.filter(product_type=Product.objects.get(id=3).product_type).values_list('id', flat=True))}
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    # image = models.ImageField(
    #     verbose_name=_("image"),
    #     help_text=_("Upload a product image"),
    #     upload_to="images/",
    #     default="images/thumbnail.jpg",
    # )
    image = ResizedImageField(size=[200, 500],  verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/thumbnail.jpg",)

    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")




class Offer(models.Model):
    # Caroussel Offers
    title = models.CharField(verbose_name=_("Title"), help_text=_("Required"), max_length=40)
    description = models.CharField(verbose_name=_("Description"),help_text=_("Short As Possiable"),max_length=90)
    image = ResizedImageField(
        size=[1080, 1920],
        verbose_name=_("image"),
        help_text=_("Upload an Offer image"),
        upload_to="images/",
        default="images/default.png",
    )
    slug = models.SlugField(max_length=40,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        verbose_name=_("Offer visibility"),
        help_text=_("Change Offer visibility"),
        default=False,
    )
    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")
    def __str__(self):
        return self.title
        #Management URLs
    def get_edit_url(self):
        return reverse("management:edit_offer", args=[self.slug])
    
    def get_delete_url(self):
        return reverse("management:delete_offer",args=[self.slug])
        
    def save(self,*args, **kwargs):
        unique_slugify(self,self.title)
        super().save(*args, **kwargs)






class Comment(MPTTModel):
    '''
    User Comments on a Specific product
    '''
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="comments")
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='chilren')
    user = models.ForeignKey(UserBase,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30,default="Unknown")
    content = models.CharField(max_length=255)
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by=['publish_date']

    def __str__(self):
        return f"Comment By{self.user}"
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def save(self,*args, **kwargs):
        self.user_name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)





class Rate(models.Model):
    '''
    User Rates for a Specific product
    '''
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="rates")
    user = models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name="rates")

    user_name = models.CharField(max_length=30,default="Unknown")
    
    rate_value = models.IntegerField(default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    
    rating_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} Rated {self.rate_value} By{self.user_name}"

    def save(self,*args, **kwargs):
        self.user_name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('product', 'user')
    
