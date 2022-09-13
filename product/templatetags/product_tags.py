from django import template
from product.models import CartItem, Product, Category

register = template.Library()


@register.filter
def stock_select(product_id):
    product = Product.objects.get(id=product_id)
    item = CartItem.objects.filter(product__id=product_id).first()

    options = ''
    for i in range(1, product.count_in_stock+1):
        if i == 1 and item is None:
            options += f'<option value="{i}" selected="">{i}</option>'
        elif item and item.quantity == i:
            options += f'<option value="{i}" selected="">{i}</option>'
        else:
            options += f'<option value="{i}">{i}</option>\n'

    return options


@register.filter
def cat_length(cat):
    # return 5
    return Product.objects.filter(category=cat).count()
