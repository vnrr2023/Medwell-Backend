from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from .models import Expense
import httpx
from .apps import PatientConfig


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_expense(request):
    try:
        user=request.user
        data=request.data
        query_type=data["query_type"]
        if query_type=="normal":
            PatientConfig.redis_client.delete(f"expense_data:{user.id}")
            exp=Expense.objects.create(user=user,expense_type=data["expense_type"],amount=data["amount"])
            exp.save()
        return JsonResponse({"message":"Expense Added Successfully..."},status=200)
    except Exception as e:
        return JsonResponse({"message":e},status=400)

