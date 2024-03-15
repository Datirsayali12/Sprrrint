from django.contrib import admin
from django.urls import path,include
from UIAsset import views


urlpatterns=[
    path('get-products/<int:category_id>',views.GetProductDetails),
    path('download-product/',views.download_product),
    path('get-subcategories/',views.get_subcategories),
    path('get-singleproduct/<int:product_id>',views.get_singleproduct, name='product_detail'),
    path('get-contain-images/<int:product_id>',views.get_product_contain_imgaes),
    #path('get-most-downloaded',views.get_most_downloaded_products),
    path('saved-product/',views.save_for_later),

    ]