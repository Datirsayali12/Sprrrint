from django.contrib import admin
from django.urls import path,include
from UIAsset import views


urlpatterns=[
    path('getproduct/',views.GetProductDetails),
    path('download-product/',views.download_product),
    path('get-subcategories/',views.get_subcategories),
    path('get-singleproduct/<int:product_id>/',views.get_singleproduct_detail, name='product_detail'),
    #path('add-to-cart/',views.add_to_cart),
    #path('get-most-downloaded',views.get_most_downloaded_products),
    path('saved-product/',views.save_for_later),

    ]