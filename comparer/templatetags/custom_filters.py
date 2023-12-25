# custom_filters.py
from django import template

register = template.Library()
@register.filter(name='dict_filter')
def filter_dict(data):
    for i in range(len(data['Title'])):
        yield {
            'Title': data['Title'][i],
            'Price': data['Price'][i],
            'Seller_Type': data['Seller_Type'][i],
            'Product_Links': data['Product_Links'][i],
            'Image_URLs': data['Image_URLs'][i],
            'Website': data['Website'][i],
            
        }



register.filter(name='filter_walmart')
def filter_walmart(data):
    for i in data:
        yield {
            'Title': i['Title'],
            'Price': i['Price'],
            'Seller_Type': i['Seller_Type'],
            'Product_Links': i['Product_Links'],
            'Image_URLs': i['Image_URLs'],
            'Website': i['Website'],
            }






