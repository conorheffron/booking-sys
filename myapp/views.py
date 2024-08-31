from django.shortcuts import render

# Create your views here. 
def ratings(request): 
      
    # render function takes argument  - request 
    # and return HTML as response 
    return render(request, "myapp\home.html") 
