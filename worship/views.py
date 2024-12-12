from django.shortcuts import render

def sermons(request):
    return render(request, 'worship/sermons.html')
