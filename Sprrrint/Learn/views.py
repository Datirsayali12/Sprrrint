from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.http import JsonResponse
from rest_framework import status
from .models import *
# Create your views here.

@api_view(['GET'])
def get_course_requirements(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        requirement_id = request.GET.get('requirement_id')  # Added line

        if course_id is None:
            return Response({"error": "Missing course_id in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        if requirement_id:  # Added block
            try:
                requirement = Requirement.objects.get(id=requirement_id)
            except Requirement.DoesNotExist:
                return Response({"error": "Requirement not found"}, status=status.HTTP_404_NOT_FOUND)

            if requirement not in course.requirements.all():
                return Response({"error": "Requirement does not belong to this course"}, status=status.HTTP_400_BAD_REQUEST)

            requirement_data = {
                "requirement_id": requirement.id,
                "requirement_name": requirement.requirement_name,
                # Add more fields as needed
            }

            return Response(requirement_data)

        requirements = course.requirements.all()
        requirements_list = [{"requirement_id": requirement.id, "requirement_name": requirement.requirement_name} for requirement in requirements]

        return Response({"course_requirements": requirements_list})

    return Response({"error": "Only GET requests are allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_video_details(request,id):
    video = Video.objects.get(pk=id)
    try:
        video_details = {
            'title': video.title,
            'asset': video.hero_video_url,
            'overview': video.overview,
            'creator': video.creator,
            'category': video.category,
            'created_at': video.created_at,
            'updated_at': video.updated_at,
        }
        return Response(video_details)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=404)