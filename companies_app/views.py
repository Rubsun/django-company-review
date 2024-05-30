"""Contains views for rendering HTML templates and processing user requests."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (AddressForm, CompanyForm, EquipmentForm, RegistrationForm,
                    ReviewForm)
from .models import Client, Company, CompanyEquipment, Equipment, Review
from .serializers import (CompanySerializer, EquipmentSerializer,
                          ReviewSerializer)
from .viewsets import create_view_set

METHOD_POST = 'POST'
CONTEXT_COMPANIES = 'companies'
CONTEXT_EQUIPMENTS = 'equipments'
CONTEXT_REVIEWS = 'reviews'
VIEW_EQUIPMENT = 'equipment_view'

CompanyViewSet = create_view_set(Company, CompanySerializer)
EquipmentViewSet = create_view_set(Equipment, EquipmentSerializer)
ReviewViewSet = create_view_set(Review, ReviewSerializer)


def homepage(request):
    """
    View function for rendering the homepage.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    return render(
        request,
        'index.html',
        context={
            CONTEXT_COMPANIES: Company.objects.count(),
            CONTEXT_EQUIPMENTS: Equipment.objects.count(),
            CONTEXT_REVIEWS: Review.objects.count(),
        },
    )


def register(request):
    """
    View function for rendering the registration page and processing registration requests.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    if request.method == METHOD_POST:
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
        {'form': form},
    )


@login_required
def profile_view(request):
    """
    View function for rendering the user profile page.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    client = get_object_or_404(Client, user=request.user)
    reviews = Review.objects.filter(client=client)
    companies = Company.objects.filter(client=client)
    equipments = Equipment.objects.filter(client=client)
    context = {
        'client': client,
        CONTEXT_REVIEWS: reviews,
        CONTEXT_COMPANIES: companies,
        CONTEXT_EQUIPMENTS: equipments,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def profile_view_by_id(request, user_id):
    """
    View function for rendering the user profile page by user ID.

    Args:
        request: Request object.
        user_id (int): User ID.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    client = get_object_or_404(Client, user_id=user_id)
    reviews = Review.objects.filter(client=client)

    context = {
        'client': client,
        CONTEXT_REVIEWS: reviews,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def equipments_view(request):
    """
    View function for rendering the equipments page.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    equipments = Equipment.objects.all()
    context = {
        CONTEXT_EQUIPMENTS: equipments,
    }
    return render(request, 'pages/equipments.html', context)


@login_required()
def companies_view(request):
    """
    View function for rendering the companies page.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    companies = Company.objects.all()
    context = {
        CONTEXT_COMPANIES: companies,
    }
    return render(request, 'pages/companies.html', context)


@login_required()
def company_detail_view(request, company_id):
    """
    View function for rendering the company detail page.

    Args:
        request: Request object.
        company_id (int): Company ID.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    company = get_object_or_404(Company, id=company_id)
    context = {
        'company': company,
    }
    return render(request, 'pages/company_detail.html', context)


@login_required
def equipment_view(request, equipment_id):
    """
    View function for rendering the equipment detail page.

    Args:
        request: Request object.
        equipment_id (int): Equipment ID.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    reviews = equipment.reviews.select_related('client__user').all()
    if request.method == METHOD_POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.equipment = equipment
            review.client = request.user.client
            review.save()
            return redirect(VIEW_EQUIPMENT, equipment_id=equipment_id)
    else:
        form = ReviewForm()

    all_companies = Company.objects.all()
    associated_companies = equipment.companies.all()
    unassociated_companies = all_companies.difference(associated_companies)

    context = {
        'equipment': equipment,
        CONTEXT_REVIEWS: reviews,
        'form': form,
        CONTEXT_COMPANIES: unassociated_companies,
    }
    return render(request, 'pages/equipment_details.html', context)


@login_required
def create_company(request):
    """
    View function for rendering the create company page and processing company creation requests.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    if request.method == METHOD_POST:
        company_form = CompanyForm(request.POST)
        address_form = AddressForm(request.POST)
        if company_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            company = company_form.save(commit=False)
            company.client = request.user.client
            company.address = address
            company.save()
            return redirect('company_detail', company.id)
    else:
        company_form = CompanyForm()
        address_form = AddressForm()
    return render(
        request,
        'pages/create_company.html',
        {'company_form': company_form, 'address_form': address_form},
    )


@login_required
def create_equipment(request):
    """
    View func for rendering the create equipment page and processing equipment creation requests.

    Args:
        request: Request object.

    Returns:
        HttpResponse: Rendered HTML template.
    """
    if request.method == METHOD_POST:
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.client = request.user.client
            equipment.save()
            return redirect(VIEW_EQUIPMENT, equipment.id)
    else:
        form = EquipmentForm()
    return render(request, 'pages/create_equipment.html', {'form': form})


@login_required
def add_equipment_to_company(request, equipment_id):
    """
    View function for adding equipment to a company.

    Args:
        request: Request object.
        equipment_id (int): Equipment ID.

    Returns:
        HttpResponseRedirect: Redirects to the equipment detail page.
    """
    if request.method == METHOD_POST:
        equipment = get_object_or_404(Equipment, id=equipment_id)
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, id=company_id)

        if CompanyEquipment.objects.filter(equipment=equipment, company=company).exists():
            messages.warning(
                request,
                'This equipment is already associated with the selected company.',
            )
        else:
            CompanyEquipment.objects.create(equipment=equipment, company=company)
            messages.success(request, 'Equipment successfully added to the company.')

        return redirect(VIEW_EQUIPMENT, equipment_id=equipment.id)

    return redirect(VIEW_EQUIPMENT, equipment_id=equipment_id)


@login_required
def delete_equipment(request, equipment_id):
    """
    View function for deleting equipment.

    Args:
        request: Request object.
        equipment_id (int): Equipment ID.

    Returns:
        HttpResponse: Rendered HTML template or Redirects to the previous page.
    """
    equipment = get_object_or_404(Equipment, id=equipment_id)
    next_url = request.GET.get('next', CONTEXT_EQUIPMENTS)

    if equipment.client != request.user.client and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this equipment.')
        return redirect(VIEW_EQUIPMENT, equipment_id=equipment_id)

    if request.method == METHOD_POST:
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
        return redirect(next_url)

    return render(request, 'pages/equipment_details.html', {'equipment': equipment})


@login_required
def delete_review(request, review_id):
    """
    View function for deleting a review.

    Args:
        request: Request object.
        review_id (int): Review ID.

    Returns:
        HttpResponseRedirect: Redirects to the equipment detail page.
    """
    review = get_object_or_404(Review, id=review_id)
    next_url = request.GET.get('next', VIEW_EQUIPMENT)

    if review.client.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this review.')
        return redirect(VIEW_EQUIPMENT, equipment_id=review.equipment.id)

    if request.method == METHOD_POST:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect(next_url, equipment_id=review.equipment.id)

    return redirect(VIEW_EQUIPMENT, equipment_id=review.equipment.id)


@login_required
def delete_company(request, company_id):
    """
    View function for deleting a company.

    Args:
        request: Request object.
        company_id (int): Company ID.

    Returns:
        HttpResponse: Rendered HTML template or Redirects to the previous page.
    """
    company = get_object_or_404(Company, id=company_id)
    next_url = request.GET.get('next', CONTEXT_COMPANIES)

    if company.client != request.user.client and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this company.')
        return redirect('company_detail', company_id=company_id)

    if request.method == METHOD_POST:
        company.delete()
        messages.success(request, 'Company deleted successfully.')
        return redirect(next_url)

    return render(request, 'pages/company_detail.html', {'company': company})
