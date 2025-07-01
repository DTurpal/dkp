from django import forms
from .models import Seller, Buyer, RealEstate

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'
        widgets = {
            'gender': forms.RadioSelect(choices=Seller.GENDER_CHOICES),
            'registration': forms.Textarea(attrs={'rows': 3}),
        }

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
        widgets = {
            'gender': forms.RadioSelect(choices=Seller.GENDER_CHOICES),
            'registration': forms.Textarea(attrs={'rows': 3}),
        }

class RealEstateForm(forms.ModelForm):
    class Meta:
        model = RealEstate
        fields = '__all__'

