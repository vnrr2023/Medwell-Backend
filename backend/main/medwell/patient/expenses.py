from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from .models import Expense
import httpx
PATIENT_SERVER_URL="http://127.0.0.1:5000/"
AI_SERVER_URL="http://localhost:8888/"

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_expense(request):
    user=request.user
    data=request.data
    query_type=data["query_type"]
    if query_type=="normal":
        exp=Expense.objects.create(user=user,expense_type=data["expense_type"],amount=data["amount"])
        exp.save()
        return JsonResponse({"message":"Expense Added Successfully..."},status=200)
    elif query_type=="natural_language":
        resp=httpx.post(AI_SERVER_URL+"process_expense_query/",json={"data":data["query"]})
        if resp.status_code==200:
            data=resp.json()
            if data["status"]:
                exp=Expense.objects.create(user=user,expense_type=data["expenditure"],amount=str(data["amount"]))
                exp.save()
                return JsonResponse({"message":"Expense Added Successfully..."},status=200)
            return JsonResponse({"message":f"Enter Relevant Expense.."},status=200)
        return JsonResponse({"message":f"Service unavailable..Try Manual addition"},status=503)

# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def show_expenses(request):
#     user=request.user
#     resp=httpx.post(PATIENT_SERVER_URL+"get_expense_data/",json={"user_id":str(user.id)})
#     if resp.status_code==200:
#         return JsonResponse(data=resp.json(),safe=False,status=200)
#     return JsonResponse(data={"mssg":"Server down.."},status=503)


# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def expenses_dashboard(request):
#     user=request.user
#     resp=httpx.post(PATIENT_SERVER_URL+"expenses_dashboard/",json={"user_id":str(user.id)})
#     if resp.status_code==200:
#         return JsonResponse(data=resp.json(),safe=False,status=200)
#     return JsonResponse(data={"mssg":"Server down.."},status=503)

# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def delete_expense(request):
#     user=request.user
#     id=request.data["expense_id"]
#     exp=Expense.objects.get(id=int(id))
#     exp.delete()
#     return JsonResponse({"mssg":"Expense Deleted Successfully..."},status=200)



