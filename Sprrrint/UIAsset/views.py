from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# Create your views here.

@api_view(["GET"])
def GetProductDetails(request):
    if request.method == "GET":
        category_name = request.GET.get("category_name")
        
        try:
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(sub_category__categories=category)

            serialized_data = []
            for product in products:
                serialized_product = {
                    "product_id": product.id,
                    "product_title": product.title,
                    "credits": product.credits,
                    "creator": product.creator.id,
                    "sub_category": product.sub_category.id,
                    "product_type": product.product_type.id,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                    "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
                    "no_of_items": product.no_of_items
                }
                serialized_data.append(serialized_product)

            return Response(serialized_data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def download_product(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        if not (user_id and product_id):
            return Response({"msg": "User ID and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the product download record
        try:
            ProductDownload.objects.create(user_id=user_id, product_id=product_id)
            return Response({"msg": "Asset downloaded successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": "Failed to record download: {}".format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['GET'])
def get_subcategories(request):
    if request.method == 'GET':
        subcategories=Subcategory.objects.all()
        subcategory_list = [{"subcategory_name": subcategory.name} for subcategory in subcategories]
        return Response({"search_result": subcategory_list})
        
#single product info APIS
@api_view(['POST'])
def get_singleproduct_detail(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            response_data = {
                "product_title": product.title,
                "credits": product.credits,
                "hero_image_url": product.hero_image_url,
                "creator_id": product.creator_id,
                "asset": product.asset,
                "tag": product.tag,
            }
            return JsonResponse(response_data)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        
@api_view(['POST'])        
def add_to_cart(request):
    if request.method == 'POST':
        try:
            credit_amount = int(request.POST.get('credit_amount'))
            user_id = int(request.POST.get('user_id'))
            product_id = int(request.POST.get('product_id'))
            transaction = ProductTransaction.objects.create(
                credit_amount=credit_amount,
                user_id=user_id,
                product_id=product_id,
                tran_type_id=1  
            )
            return JsonResponse({'message': 'Added to cart successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    
@api_view(['GET'])      
def get_most_downloaded_products(request):
    if request.method == 'GET':
        most_downloaded_product_ids = ProductDownload.objects.values('product_id').annotate(download_count=models.Count('product_id')).order_by('-download_count')[:10]
        search_results = []
        for product_info in most_downloaded_product_ids:
            product_id = product_info['product_id']
            product = Product.objects.get(pk=product_id)
            search_results.append({
                'title': product.title,
                'credits': product.credits,
                'hero_img_url': product.hero_img_url,
                'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': product.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'no_of_items': product.no_of_items
            })

        return JsonResponse({'search_result': search_results}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@api_view(['POST'])
def save_for_later(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        
        if user_id is None or product_id is None:
            return Response({"error": "Missing user_id or product_id in request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        SavedProduct.objects.create(user_id=user_id, product_id=product_id)
        return Response({"message": "Items saved in library successfully"}, status=status.HTTP_201_CREATED)
    
    return Response({"error": "Only POST requests are allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)