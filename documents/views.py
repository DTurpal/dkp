from django.shortcuts import render, redirect
from .forms import SellerForm, BuyerForm, RealEstateForm


def create_dkp(request):
    if request.method == 'POST':
        seller_form = SellerForm(request.POST)
        buyer_form = BuyerForm(request.POST)
        estate_form = RealEstateForm(request.POST)

        if all([seller_form.is_valid(), buyer_form.is_valid(), estate_form.is_valid()]):
            seller = seller_form.save()
            buyer = buyer_form.save()
            estate = estate_form.save()
            # Здесь будет генерация документа
            return redirect('success_page')

    else:
        seller_form = SellerForm()
        buyer_form = BuyerForm()
        estate_form = RealEstateForm()

    return render(request, 'documents/create_dkp.html', {
        'seller_form': seller_form,
        'buyer_form': buyer_form,
        'estate_form': estate_form,
    })