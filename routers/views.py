from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Router
from .serializers import RouterSerializer
from .tasks import monitor_router, reboot_router
from .forms import RouterForm

class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer


def add_router(request):
    """
    View to display the router form and handle POST request for adding a router.
    """
    if request.method == 'POST':
        form = RouterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new router to the database
            return redirect('router_list')  # Redirect to a page showing all routers
    else:
        form = RouterForm()

    return render(request, 'routers/add_router.html', {'form': form})


def router_list(request):
    """
    View to display all routers.
    """
    routers = Router.objects.all()
    return render(request, 'routers/router_list.html', {'routers': routers})

def router_details(request, id):
    """
    Display details of a specific router.
    """
    router = get_object_or_404(Router, id=id)
    router.status = monitor_router(router.mac_address)  # Fetch router status dynamically
    return render(request, 'routers/router_details.html', {'router': router})

@api_view(['GET'])
def check_router_status(request):
    """
    Check and return the status of all routers.
    """
    routers = Router.objects.all()
    results = []
    
    for router in routers:
        status = monitor_router(router.mac_address)  # Celery Task
        results.append({
            "mac_address": router.mac_address,
            "status": status
        })
    
    return Response(results)

@api_view(['POST'])
def reboot_router_endpoint(request, id):
    """
    Reboot a specific router using its ID.
    """
    router = get_object_or_404(Router, id=id)
    result = reboot_router(router.mac_address)
    return Response({"message": result})

