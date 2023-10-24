from django import template
from cart.models import Order
from wishlist.models import Wishlist


register = template.Library()


@register.filter
def cart_item_count(user):
    """Generate Cart item count for base.html

    Args:
        user (int): count

    Returns:
        int: count
    """

    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def wishlist_item_count(user):
    """generate wishlist item count for base.html header

    Args:
        user (int): count
    """
    if user.is_authenticated:
        qs = Wishlist.objects.filter(user=user)
        if qs.exists():
            return qs[0].items.count()
    return 0
