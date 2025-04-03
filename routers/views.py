from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Router
from .serializers import RouterSerializer
from .tasks import monitor_router, reboot_router
from .forms import RouterForm
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

# Custom Pagination Class
class RouterPagination(PageNumberPagination):
    page_size = 10  # Default number of routers per page
    page_size_query_param = 'page_size'  # Allows clients to set page size
    max_page_size = 50  # Maximum limit for page size

class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all().order_by('-id')  # Order by latest
    serializer_class = RouterSerializer
    pagination_class = RouterPagination  # Enable pagination


def add_router(request):
    """
    View to display the router form and handle POST request for adding a router.
    Also prevents duplicate routers based on MAC address.
    """
    if request.method == 'POST':
        form = RouterForm(request.POST)
        if form.is_valid():
            mac_address = form.cleaned_data['mac_address']

            # Check if router already exists
            if Router.objects.filter(mac_address=mac_address).exists():
                messages.error(request, "Router with this MAC Address already exists.")
            else:
                form.save()
                messages.success(request, "Router added successfully!")
                return redirect('router_list')  # Redirect to router list page

    else:
        form = RouterForm()

    return render(request, 'routers/add_router.html', {'form': form})

def router_list(request):
    routers = Router.objects.all().order_by('-id')  # Fetch routers and order them

    # Paginate with 10 routers per page
    paginator = Paginator(routers, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'routers/router_list.html', {
        'page_obj': page_obj,
        'total_count': routers.count(),  # Total number of routers
    })

def router_details(request, id):
    """
    Display details of a specific router.
    """
    router = get_object_or_404(Router, id=id)
    router.status = monitor_router(router.mac_address)  # Fetch router status dynamically
    return render(request, 'routers/router_details.html', {'router': router})

def edit_router(request, id):
    # Get the router by ID, or return 404 if not found
    router = get_object_or_404(Router, id=id)
    

    # If the request method is POST, we want to update the router
    if request.method == 'POST':
        form = RouterForm(request.POST, instance=router)  # Bind the form to the router instance
        # print(form, "---- form ")
        if form.is_valid():
            print(form.is_valid(), "---- form it is valide.... ")
            form.save()  # Save the updated router data
            messages.success(request, "Router updated successfully!")
            return redirect('router_details', id=router.id)  # Redirect to the updated router details page
        else:
            print(form.errors, "---- form errors.... ")
            messages.error(request, "Invalid form submission.")
            # form = RouterForm(instance=router)  # Pre-populate the form with the current router data
    else:
        print("---- form is not valid.... ")
        messages.error(request, "Invalid form submission.")
        form = RouterForm(instance=router)  # Pre-populate the form with the current router data

    return render(request, 'routers/edit_router.html', {'form': form, 'router': router})

def delete_router(request, id):
    """
    View to delete a router.
    """
    router = get_object_or_404(Router, id=id)
    
    if request.method == 'POST':
        router.delete()
        messages.success(request, "Router deleted successfully!")
        return redirect('router_list')  # Redirect to router list page
    


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

@api_view(['GET'])
def get(request):
    """
    Fetch and return paginated list of routers.
    """
    routers = Router.objects.all().order_by('-id')  # Order by latest

    # Setup pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of routers per page
    paginated_routers = paginator.paginate_queryset(routers, request)

    # Serialize the paginated data
    serializer = RouterSerializer(paginated_routers, many=True)
    
    # Return paginated response
    return paginator.get_paginated_response(serializer.data)