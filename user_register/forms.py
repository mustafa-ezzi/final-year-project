from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'delivery_type', 'address']
        widgets = {
            'delivery_type': forms.RadioSelect,  # buttons instead of dropdown
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially hide address
        self.fields['address'].widget.attrs['style'] = 'display:none;'

        # Add JS dynamically in template to show/hide address based on delivery_type
