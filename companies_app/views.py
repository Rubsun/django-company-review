from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import permissions, viewsets
from django.contrib import messages
from .forms import RegistrationForm, ReviewForm, CompanyForm, EquipmentForm
from .models import Company, Equipment, Review, Client, CompanyEquipment
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
    client = get_object_or_404(Client, user=request.user)
    reviews = Review.objects.filter(client=client)
    companies = Company.objects.filter(client=client)
    equipments = Equipment.objects.filter(client=client)
    context = {
        'client': client,
        'reviews': reviews,
        'companies': companies,
        'equipments': equipments,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def profile_view_by_id(request, user_id):
    client = get_object_or_404(Client, user_id=user_id)
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


@login_required
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

    all_companies = Company.objects.all()
    associated_companies = equipment.companies.all()
    unassociated_companies = all_companies.difference(associated_companies)

    context = {
        'equipment': equipment,
        'reviews': reviews,
        'form': form,
        'companies': unassociated_companies,
    }
    return render(request, 'pages/equipment_details.html', context)


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.client = request.user.client
            company.save()
            return redirect('company_detail', company.id)
    else:
        form = CompanyForm()
    return render(request, 'pages/create_company.html', {'form': form})


@login_required
def create_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.client = request.user.client
            equipment.save()
            return redirect('equipment_view', equipment.id)
    else:
        form = EquipmentForm()
    return render(request, 'pages/create_equipment.html', {'form': form})


@login_required
def add_equipment_to_company(request, equipment_id):
    if request.method == 'POST':
        equipment = get_object_or_404(Equipment, id=equipment_id)
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, id=company_id)

        if CompanyEquipment.objects.filter(equipment=equipment, company=company).exists():
            messages.warning(request, 'This equipment is already associated with the selected company.')
        else:
            CompanyEquipment.objects.create(equipment=equipment, company=company)
            messages.success(request, 'Equipment successfully added to the company.')

        return redirect('equipment_view', equipment_id=equipment.id)

    return redirect('equipment_view', equipment_id=equipment_id)


@login_required
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    next_url = request.GET.get('next', 'equipments')

    if equipment.client != request.user.client and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this equipment.')
        return redirect('equipment_view', equipment_id=equipment_id)

    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
        return redirect(next_url)

    return render(request, 'pages/equipment_details.html', {'equipment': equipment})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.client != request.user:
        messages.error(request, 'You do not have permission to delete this review.')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')

    return redirect('profile')

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    next_url = request.GET.get('next', 'companies')

    if company.client != request.user.client and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this company.')
        return redirect('company_detail', company_id=company_id)

    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully.')
        return redirect(next_url)

    return render(request, 'pages/company_detail.html', {'company': company})