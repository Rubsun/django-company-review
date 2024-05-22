from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import permissions, viewsets

from .forms import RegistrationForm, ReviewForm
from .models import Company, Equipment, Review, Client
from .serializers import CompanySerializer, ReviewSerializer, EquipmentSerializer


class APIPermission(permissions.BasePermission):
    _allowed_methods = ['GET', 'OPTIONS', 'HEAD']
    _not_allowed_methods = ['POST', 'PUT', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self._allowed_methods and (
                request.user.is_authenticated and request.user.is_authenticated):
            return True
        if request.method in self._not_allowed_methods and (request.user and request.user.is_superuser):
            return True
        return False


def create_view_set(model_class, serializer):
    class CustomViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [APIPermission]

    return CustomViewSet


CompanyViewSet = create_view_set(Company, CompanySerializer)
EquipmentViewSet = create_view_set(Equipment, EquipmentSerializer)
ReviewViewSet = create_view_set(Review, ReviewSerializer)


def homepage(request):
    return render(
        request,
        'index.html',
        context={
            'companies': Company.objects.count(),
            'equipments': Equipment.objects.count(),
            'reviews': Review.objects.count()
        }
    )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
        }
    )


@login_required
def profile_view(request):
    client = Client.objects.get(user=request.user)
    reviews = Review.objects.filter(client=client)
    context = {
        'client': client,
        'reviews': reviews,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def equipments_view(request):
    equipments = Equipment.objects.all()
    context = {
        'equipments': equipments,
    }
    return render(request, 'pages/equipments.html', context)


@login_required()
def companies_view(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'pages/companies.html', context)


@login_required()
def company_detail_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    context = {
        'company': company,
    }
    return render(request, 'pages/company_detail.html', context)


@login_required()
def equipment_view(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    reviews = equipment.reviews.select_related('client__user').all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.equipment = equipment
            review.client = request.user.client
            review.save()
            return redirect('equipment_view', equipment_id=equipment_id)
    else:
        form = ReviewForm()

    context = {
        'equipment': equipment,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'pages/equipment_details.html', context)



