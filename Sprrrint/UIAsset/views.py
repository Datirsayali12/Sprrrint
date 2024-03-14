from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from Learn.models import Video,Ebook,Course

# Create your views here.

@api_view(['GET'])
def GetProductDetails(request, category_id):
    if request.method == "GET":
        category = Category.objects.get(id=category_id)
        category_name = category.name.lower()

        if category_name == "video":
            videos = Video.objects.filter(category=category)
            serialized_data = []
            for video in videos:
                serialized_product = {
                    "title": video.title,
                    "overview": video.overview,
                    "creator": video.creator.id,
                    "category": video.category.id,
                    "created_at": video.created_at,
                    "updated_at": video.updated_at,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        elif category_name == "course":
            courses = Course.objects.filter(category=category)
            serialized_data = []
            for course in courses:
                serialized_product = {
                    "course_name": course.course_name,
                    "course_short_desc": course.course_short_desc,
                    "creator": course.creator.id,
                    "category": course.category.id,
                    "created_at": course.created_at,
                    "updated_at": course.updated_at,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        elif category_name == "ebook":
            ebooks = Ebook.objects.filter(category=category)
            serialized_data = []
            for ebook in ebooks:
                serialized_product = {
                    "name": ebook.name,
                    "no_of_chapters": ebook.no_of_chapters,
                    "no_of_pages": ebook.no_of_pages,
                    "description": ebook.description,
                    "creator": ebook.creator.id,
                    "category": ebook.category.id,
                    "created_at": ebook.created_at,
                    "updated_at": ebook.updated_at,
                    "ebook_desc": ebook.ebook_desc,
                    "level": ebook.level.id,
                }
                serialized_data.append(serialized_product)
            return Response(serialized_data, status=status.HTTP_200_OK)

        else:
            # Filter products based on category and is_pack
            products = Product.objects.filter(category=category)

            serialized_data = []
            for product in products:
                serialized_product = {
                    "product_id": product.id,
                    "product_title": product.title,
                    "credits": product.credits,
                    "creator": product.creator.id,
                    "category": product.category.id,
                    "product_type": product.product_type.id,
                    "created_at": product.created_at,
                    "updated_at": product.updated_at,
                    "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
                    "no_of_items": product.no_of_items,
                    "is_free": product.is_free
                }
                serialized_data.append(serialized_product)

            return Response(serialized_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def download_product(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        if not (user_id and product_id):
            return Response({"msg": "User ID and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)
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
        
@api_view(["GET"])
def get_singleproduct(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        serialized_product = {
            "product_id": product.id,
            "product_title": product.title,
            "credits": product.credits,
            "creator": product.creator.id,
            "category": product.category.id,
            "product_type": product.product_type.id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "tags": [{"tag_id": tag.id, "tag_name": tag.name} for tag in product.tag.all()],
            "no_of_items": product.no_of_items,
            "is_free": product.is_free
        }
        return JsonResponse(serialized_product, status=200)
    except  ObjectDoesNotExist:
        return JsonResponse({"message": "Product not found"}, status=404)



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