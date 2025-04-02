from django import forms
from .models import Router

class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        fields = [
            'mac_address', 'username', 'password', 'location', 'phone_number', 
            'status', 'description', 'router_type', 'parent_router'
        ]
        widgets = {
            'mac_address': forms.TextInput(attrs={'placeholder': 'Enter MAC Address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter Location'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'status': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description'}),
            'router_type': forms.Select(),
            'parent_router': forms.Select()
        }
        labels = {
            'mac_address': 'MAC Address',
            'username': 'Username',
            'password': 'Password',
            'location': 'Location',
            'phone_number': 'Phone Number',
            'status': 'Status',
            'description': 'Description',
            'router_type': 'Router Type',
            'parent_router': 'Parent Router'
        }
        help_texts = {
            'mac_address': 'Format: XX:XX:XX:XX:XX:XX',
            'username': 'Login username for the router',
            'password': 'Login password for the router',
            'location': 'Physical location of the router',
            'phone_number': 'Contact phone number of the router admin',
            'status': 'Current status of the router',
            'description': 'Any additional notes about the router',
            'router_type': 'Specify if it is a head, intermediate, or tail router',
            'parent_router': 'Select the parent router (if applicable)'
        }
        error_messages = {
            'mac_address': {
                'required': 'MAC Address is required',
                'invalid': 'Invalid MAC Address format',
                'unique': 'This MAC Address already exists'
            },
            'username': {
                'required': 'Username is required',
            },
            'password': {
                'required': 'Password is required',
            },
            'location': {
                'required': 'Location is required',
            },
            'phone_number': {
                'required': 'Phone Number is required',
            },
            'status': {
                'required': 'Status is required',
            },
            'router_type': {
                'required': 'Router Type is required',
            },
        }
