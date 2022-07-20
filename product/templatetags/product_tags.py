from django import template
from product.models import CartItem

register = template.Library()


@register.filter
def stock_select(product_id):
    item = CartItem.objects.filter(product__id=product_id).first()

    options = ''
    for i in range(1, item.product.count_in_stock+1):
        options += f'<option value="{i}">{i}</option>\n'

    '''<option value="1" selected="">1</option>
                            <option value="2">2</option>
'''

    return options
