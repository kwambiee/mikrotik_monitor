from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouterViewSet, reboot_router_endpoint
from . import views

router = DefaultRouter()
router.register(r'routers', RouterViewSet)

urlpatterns = [
    # api endpoints and views
    path('api/', include(router.urls)),
    path('api/routers/<int:id>/reboot/', reboot_router_endpoint, name='api_reboot_router'),
    path('routers/add/', views.add_router, name='add_router'),
    path('routers/edit-router/<int:id>/', views.edit_router, name='edit_router'),
    path('routers/delete/<int:id>/', views.delete_router, name='delete_router'),
    path('routers/', views.router_list, name='router_list'),
    path('routers/<int:id>/', views.router_details, name='router_details'),
]



# urlpatterns += router.urls