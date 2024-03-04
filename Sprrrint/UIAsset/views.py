# from django.shortcuts import render
# from .models import *
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.http import JsonResponse

# # Create your views here.


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product, Category
# from rest_framework import status

# @api_view(["GET"])
# def GetProductDetails(request):
#     if request.method == "GET":
#         category_name = request.GET.get("category_name")
        
#         try:
#             category = Category.objects.get(name=category_name)
#             products = Product.objects.filter(sub_category__categories=category)

#             serialized_data = []
#             for product in products:
#                 serialized_product = {
#                     "product_id": product.id,
#                     "product_title": product.title,
#                     "credits": product.credits,
#                     "creator": product.creator.id,
#                     "sub_category": product.sub_category.id,
#                     "product_type": product.product_type.id,
#                     "created_at": product.created_at,
#                     "updated_at": product.updated_at,
#                     "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
#                     "no_of_items": product.no_of_items
#                 }
#                 serialized_data.append(serialized_product)

#             return Response(serialized_data, status=status.HTTP_200_OK)
#         except Category.DoesNotExist:
#             return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
# @api_view(['POST'])
# def download_product(request):
#     if request.method == 'POST':
#         user_id = request.data.get('user_id')
#         product_id = request.data.get('product_id')
#         if not (user_id and product_id):
#             return Response({"msg": "User ID and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Save the product download record
#         try:
#             ProductDownload.objects.create(user_id=user_id, product_id=product_id)
#             return Response({"msg": "Asset downloaded successfully."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"msg": "Failed to record download: {}".format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# @api_view(['GET'])
# def get_subcategories(request):
#     if request.method == 'GET':
#         subcategories=Subcategory.objects.all()
#         subcategory_list = [{"subcategory_name": subcategory.name} for subcategory in subcategories]
#         return Response({"search_result": subcategory_list})
        