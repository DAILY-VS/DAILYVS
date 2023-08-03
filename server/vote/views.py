from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
=======
from django.http import HttpResponse

# Create your views here.


def main(request):
    return render(request, "vote/main.html")
>>>>>>> d03d232f3d0dfb687aada7d1ee4e66a86dd38b04
