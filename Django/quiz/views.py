from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import choice

from .models import Question
from .serialize import QuestionSerializer
# Create your views here.


# ============================================= GET REQUEST SECTION ============================================= #
def home_page(request):
    return JsonResponse({
        "Greeting": {
            "Message": "Welcome to Quiz REST API",
            "Status Code": 200
        }
    })


@api_view(["GET"])
def all_page(request):
    if request.method == "GET":
        all_data = Question.objects.all()
        serialized = QuestionSerializer(all_data, many=True)
        return JsonResponse({
            "data": serialized.data
        })


@api_view(["GET"])
def random_page(request):
    if request.method == "GET":
        all_data = Question.objects.all()
        serialized = QuestionSerializer(all_data, many=True)
        return JsonResponse({
            "data": choice(serialized.data)
        })


@api_view(["GET"])
def filter_category(request, category):
    if request.method == "GET":
        if category.lower() == "fastapi":
            all_data = Question.objects.filter(category="FastAPI").all()
        else:
            all_data = Question.objects.filter(
                category=category.capitalize()).all()
        serialized = QuestionSerializer(all_data, many=True)
        return JsonResponse({
            "data": serialized.data
        })


@api_view(["GET"])
def filter_level(request, level):
    if request.method == "GET":
        all_data = Question.objects.filter(
            level=level.capitalize()).all()
        serialized = QuestionSerializer(all_data, many=True)
        return JsonResponse({
            "data": serialized.data
        })


@api_view(["GET"])
def filter_id(request, id):
    try:
        data = Question.objects.get(pk=id)
    except data.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serialized = QuestionSerializer(data)
        return Response(serialized.data)


# ============================================= POST REQUEST SECTION ============================================= #
@api_view(["POST"])
def add_page(request):
    if request.method == "POST":
        serialized = QuestionSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse({
                "success": {
                    "Message": "Congratulations, New Question Has Been Added!",
                    "Status Code": status.HTTP_201_CREATED
                }
            })
        else:
            return JsonResponse({
                "error": {
                    "Message": "Method Not Allowed!",
                    "Status Code": status.HTTP_406_NOT_ACCEPTABLE
                }
            })


# ============================================= PUT REQUEST SECTION ============================================= #
@api_view(["GET", "PUT"])
def change_page(request):
    question_id = request.GET.get("id")
    api_key = request.GET.get("api_key")
    try:
        chosen_question = Question.objects.get(pk=question_id)
    except chosen_question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        if api_key == "TommyShelby":
            serialized = QuestionSerializer(chosen_question, data=request.data)
            if serialized.is_valid():
                serialized.save()
                return JsonResponse({
                    "success": {
                        "Message": "Congratulations, Question has been changed successfully!",
                        "Status code": status.HTTP_200_OK
                    }
                })
            else:
                return JsonResponse({
                    "error": {
                        "Message": "NO VALID DATA",
                        "Status Code": status.HTTP_400_BAD_REQUEST
                    }
                })
        else:
            return JsonResponse({
                "error": {
                    "Message": "Wrong Api Key - FORBIDDEN!",
                    "Status Code": status.HTTP_403_FORBIDDEN
                }
            })
    else:
        return JsonResponse({
            "error": {
                "Message": "Method Not Allowed!",
                "Status Code": status.HTTP_405_METHOD_NOT_ALLOWED
            }
        })

# ============================================= PATCH REQUEST SECTION ============================================= #


@api_view(["GET", "PATCH"])
def update_page(request, id):
    api_key = request.GET.get("api_key")
    field_name = request.GET.get("field_name").lower()
    new_value = request.GET.get("new_value")
    try:
        chosen_question = Question.objects.get(pk=id)
    except chosen_question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        if api_key == "TommyShelby":
            if field_name == "question":
                chosen_question.question = new_value
            elif field_name == "answer":
                chosen_question.answer = new_value
            elif field_name == "category":
                chosen_question.category = new_value
            elif field_name == "level":
                chosen_question.level = new_value
            elif field_name == "wrong_answers":
                chosen_question.wrong_answers = new_value
            chosen_question.save()
            return JsonResponse({
                "success": {
                    "Message": "Congratulations, Question has been updated successfully!",
                    "Status code": status.HTTP_200_OK
                }
            })

        else:
            return JsonResponse({
                "error": {
                    "Message": "Wrong Api Key - FORBIDDEN!",
                    "Status Code": status.HTTP_403_FORBIDDEN
                }
            })
    else:
        return JsonResponse({
            "error": {
                "Message": "Method Not Allowed!",
                "Status Code": status.HTTP_405_METHOD_NOT_ALLOWED
            }
        })

# ============================================= DELETE REQUEST SECTION ============================================= #


@api_view(["GET", "DELETE"])
def delete_page(request, id):
    api_key = request.GET.get("api_key")
    try:
        chosen_question = Question.objects.get(pk=id)
    except chosen_question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        if api_key == "TommyShelby":
            chosen_question.delete()
            return JsonResponse({
                "success": {
                    "Message": "Congratulations, Question has been deleted successfully!",
                    "Status code": status.HTTP_200_OK
                }
            })

        else:
            return JsonResponse({
                "error": {
                    "Message": "Wrong Api Key - FORBIDDEN!",
                    "Status Code": status.HTTP_403_FORBIDDEN
                }
            })
    else:
        return JsonResponse({
            "error": {
                "Message": "Method Not Allowed!",
                "Status Code": status.HTTP_405_METHOD_NOT_ALLOWED
            }
        })
