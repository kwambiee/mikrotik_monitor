from django.db import models

# Create your models here.

class Router(models.Model):
    
    MAC_ADDRESS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('reset', 'Reset'),
    ]
    
    ROUTER_TYPE_CHOICES = [
        ('head', 'Head'),  # Root router of the network
        ('tail', 'Tail'),  # End of the network (leaf node)
        ('intermediate', 'Intermediate'),  # Routers in between
    ]
    mac_address = models.CharField(max_length=17, unique=True)
    username = models.CharField(max_length=50, unique=False)
    password = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=MAC_ADDRESS_CHOICES)
    description = models.TextField(blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)
    last_reset = models.DateTimeField(null=True, blank=True)
    router_type = models.CharField(max_length=50, choices=ROUTER_TYPE_CHOICES, default='intermediate')   
    parent_router = models.ForeignKey(
        'self',  # Referencing the same model
        on_delete=models.SET_NULL,  # Set null if the parent router is deleted
        null=True,  # Parent router can be null for head routers (root routers)
        blank=True,  # Parent router is optional for head routers
        related_name='children'  # This will allow easy access to child routers
    )

    def __str__(self):
        return f"{self.mac_address} - {self.location}"

