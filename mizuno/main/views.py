
from django.shortcuts import render


def main(request):
    return render(request, 'main/Main.html')

def crm(request):
    return render(request, 'main/CRM.html')

def om(request):
    return render(request, 'main/OM.html')
