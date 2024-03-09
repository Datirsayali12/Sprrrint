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
def get_video_details(request):
    video_id = request.GET.get('video_id')
    try:
        video = Video.objects.get(pk=video_id)
        video_details = {
            'video_title': video.video_title,
            'asset': video.hero_video_url,
            'video_overview': video.video_overview,
            'resource_id': video.pk,
            'creator_id': video.creator_id,
            'total_likes': video.total_likes,
            'total_dislikes': video.total_dislikes,
            'total_shares': video.total_shares
        }
        return Response(video_details)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=404)