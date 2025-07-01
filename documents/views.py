from django.shortcuts import render, redirect
from django.db import transaction
from .forms import SellerForm, BuyerForm, RealEstateForm

'''def create_dkp(request):
    if request.method == 'POST':
        seller_form = SellerForm(request.POST)
        buyer_form = BuyerForm(request.POST)
        estate_form = RealEstateForm(request.POST)

        if seller_form.is_valid() and buyer_form.is_valid() and estate_form.is_valid():
            with transaction.atomic():
                seller = seller_form.save()
                buyer = buyer_form.save()
                estate = estate_form.save()
                # Здесь будет генерация документа
                return redirect('success_page')

    else:
        context = {
            'seller_form': SellerForm(),
            'buyer_form': BuyerForm(),
            'estate_form': RealEstateForm(),
        }
        return render(request, 'documents/create_dkp.html', context)

    # Если форма не валидна, покажем ошибки
    context = {
        'seller_form': seller_form,
        'buyer_form': buyer_form,
        'estate_form': estate_form,
    }
    return render(request, 'documents/create_dkp.html', context)'''

from django.http import FileResponse
from docx import Document
import io
import re


def create_dkp(request):
    if request.method == 'POST':
        seller_form = SellerForm(request.POST)
        buyer_form = BuyerForm(request.POST)
        estate_form = RealEstateForm(request.POST)

        if all([seller_form.is_valid(), buyer_form.is_valid(), estate_form.is_valid()]):
            seller = seller_form.save()
            buyer = buyer_form.save()
            estate = estate_form.save()

            # Путь к вашему шаблону DOCX
            template_path = "scamp/договор.docx"  # Укажите правильный путь

            # Загружаем документ
            doc = Document(template_path)

            # Данные для замены
            replacements = {
                '{ФИО продавца}': seller.full_name,
                '{пол продавца}': seller.get_gender_display(),
                '{паспорт продавца}': f"{seller.passport_series} № {seller.passport_number}",
                '{кем выдан продавца}': seller.issued_by,
                #дата выдачи
                '{адрес продавца}': seller.registration,
                '{ФИО покупателя}': seller.full_name,
                '{пол покупателя}': buyer.get_gender_display(),
                '{паспорт покупателя}': f"{buyer.passport_series} № {buyer.passport_number}",
                '{кем выдан покупателя}': buyer.issued_by,
                '{адрес покупателя}': buyer.registration,

                # Добавьте другие поля по аналогии
            }



            # Функция для замены текста в параграфах
            def replace_text(doc, replacements):
                for paragraph in doc.paragraphs:
                    for old_text, new_text in replacements.items():
                        if old_text in paragraph.text:
                            paragraph.text = paragraph.text.replace(old_text, new_text)
                return doc

            # Заменяем плейсхолдеры
            doc = replace_text(doc, replacements)

            # Сохраняем в буфер
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            # Отправляем файл пользователю
            return FileResponse(
                buffer,
                as_attachment=True,
                filename="Договор_купли_продажи.docx"
            )

    else:
        seller_form = SellerForm()
        buyer_form = BuyerForm()
        estate_form = RealEstateForm()

    return render(request, 'documents/create_dkp.html', {
        'seller_form': seller_form,
        'buyer_form': buyer_form,
        'estate_form': estate_form,
    })


from django.contrib.auth.decorators import login_required
from .models import GeneratedDKP


'''@login_required
def dkp_history(request):
    documents = GeneratedDKP.objects.filter(user=request.user).select_related(
        'seller', 'buyer', 'real_estate'
    ).order_by('-created_at')

    return render(request, 'documents/dkp_history.html', {'documents': documents})
'''
from django.core.paginator import Paginator

def dkp_history(request):
    documents = GeneratedDKP.objects.filter(user=request.user)
    paginator = Paginator(documents, 10)  # 10 документов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dkp_history.html', {'page_obj': page_obj})