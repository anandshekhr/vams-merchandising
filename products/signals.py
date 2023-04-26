from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductReviewAndRatings,Products
from django.db.models import Avg
from django.contrib.auth import get_user_model
from Home.models import Notification


User = get_user_model()

@receiver(post_save, sender=ProductReviewAndRatings)
def update_product_average_rating(sender, instance, **kwargs):
    # Get the product associated with this rating
    product = instance.product

    # Calculate the average rating for this product
    average_rating = ProductReviewAndRatings.objects.filter(product=product).aggregate(
        avg_rating=Avg('ratings'))['avg_rating']

    # Update the product's rating field with the new value
    product.average_rating = average_rating
    product.save()


# @receiver(post_save, sender=User)
# def create_notification(sender, instance, created, message,**kwargs):
#     if created:
#         Notification.objects.create(
#             recipient=instance,
#             sender=User.objects.get(username='admin'),
#             message=message
#         )
