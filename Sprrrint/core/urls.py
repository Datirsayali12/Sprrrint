"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from UIAsset import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('getproduct/',views.GetProductDetails),
    path('download-product/',views.download_product),
    path('get-subcategories/',views.get_subcategories),
    path('get-singleproduct/<int:product_id>/',views.get_singleproduct_detail, name='product_detail'),
    #path('add-to-cart/',views.add_to_cart),
    path('get-most-downloaded',views.get_most_downloaded_products),
    path('saved-product',views.save_for_later),
    path('learn/',include('Learn.urls'))
    
]
