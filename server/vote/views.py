from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.


def main(request):
    return render(request, "vote/main.html")


def detail(request):
    return render(request, "vote/detail.html")


def result(request):
    return render(request, "vote/result.html")


def result_view(request):
    approval_percentage = 75
    disapproval_percentage = 25

    return render(
        request,
        "result.html",
        {
            "approval_percentage": approval_percentage,
            "disapproval_percentage": disapproval_percentage,
        },
    )
