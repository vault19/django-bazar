import operator
from functools import reduce
from django.db.models import Q
# from django.shortcuts import render
from bazar.models import Listing, Profile, Category, City
from django.views.generic import ListView, CreateView, DetailView
# from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class AllListingsView(ListView):
    template_name = "landing_page.html"
    model = Listing

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        listing = Listing.objects.filter(status=Listing.OPEN)

        if sort:
            listings = listing.order_by(sort)
        else:
            listings = listing.order_by('category').order_by('city')

        return listings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TITLE'] = settings.TITLE
        context['CURRENCY'] = settings.CURRENCY
        context['breadcrumbs'] = [{'url': '', 'title': _('Home'), 'active': True},]
        context['cities'] = City.objects.all()
        context['city'] = 'all'
        context['categories'] = Category.objects.filter(parent=None).all()
        context['category'] = 'all'

        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user=self.request.user)
        else:
            context["profile"] = None

        return context


class CityListView(AllListingsView):

    def get_queryset(self):
        city_slug = self.kwargs.get('city_slug')
        sort = self.request.GET.get('sort')

        listings = Listing.objects.filter(status=Listing.OPEN).filter(city__slug=city_slug)

        if sort:
            listings = listings.order_by(sort)
        else:
            listings = listings.order_by('category').order_by('city')

        return listings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_slug = self.kwargs.get('city_slug')
        context['city'] = City.objects.get(slug=city_slug)
        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': '', 'title': context['city'].city, 'active': True},
        ]

        return context


class CityCategoryListView(CityListView):

    def get_queryset(self):
        city_slug = self.kwargs.get('city_slug')
        category_slug = self.kwargs.get('category_slug')
        sort = self.request.GET.get('sort')

        listings = Listing.objects.filter(status=Listing.OPEN).filter(city__slug=city_slug)\
            .filter(category__slug=category_slug)

        if sort:
            listings = listings.order_by(sort)
        else:
            listings = listings.order_by('category').order_by('city')

        return listings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = Category.objects.get(slug=category_slug)
        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': reverse('city_list_view', kwargs={'city_slug': context['city'].slug}),
             'title': context['city'].city},
            {'url': '', 'title': context['category'].name, 'active': True},
        ]

        return context


class CategoryListView(AllListingsView):

    def get_queryset(self, **kwargs):
        category_slug = self.kwargs.get('category_slug')
        sort = self.request.GET.get('sort')

        listings = Listing.objects.filter(status=Listing.OPEN).filter(category__slug=category_slug)

        if sort:
            listings = listings.order_by(sort)
        else:
            listings = listings.order_by('category').order_by('city')

        return listings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = Category.objects.get(slug=category_slug)
        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': '', 'title': context['category'].name, 'active': True},
        ]
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    model = User


class ListingCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Listing
    fields = ['category', 'city', 'title', 'price', 'description', 'type', 'status', 'photo']

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("listing_detail_view", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TITLE'] = settings.TITLE
        context['CURRENCY'] = settings.CURRENCY
        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': '', 'title': _('New Listing'), 'active': True},
        ]
        context["profile"] = Profile.objects.get(user=self.request.user)

        return context

class ListingUpdateView(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['city', 'title', 'price', 'description', 'photo']

    def get_success_url(self):
        return reverse("listing_detail_view", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True

        return context

class ListingDeleteView(LoginRequiredMixin, DeleteView):
    model = Listing
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        listing = super().get_object()

        if not listing.user == self.request.user:
            raise Http404

        return listing


class CategoryCreateView(CreateView):
    # model = Category
    fields = ['parent']
    template_name = 'bazar/category_form.html'

    def get_queryset(self):
        return Category.subcat.filter(parent=None)


class ListingDetailView(DetailView):
    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)

        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': reverse('city_list_view', kwargs={'city_slug': context['object'].city.slug}),
             'title': context['object'].city},
            {'url': '', 'title': context['object'].title, 'active': True},
        ]
        context['TITLE'] = settings.TITLE
        context['CURRENCY'] = settings.CURRENCY

        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ['profile_city', 'preferred_contact']
    success_url = reverse_lazy("index_view")

    # Why dont I have to declare a model here??
    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'url': reverse('index_view'), 'title': _('Home')},
            {'url': '', 'title': _('Profile'), 'active': True},
        ]
        context['TITLE'] = settings.TITLE
        context['CURRENCY'] = settings.CURRENCY
        context['user_listings'] = Listing.objects.filter(user=self.request.user)
        return context


# modified from https://www.calazan.com/adding-basic-search-to-your-django-site/
class SearchListView(ListView):
    model = Listing

    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(description__icontains=q) for q in query_list))
            )
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = _("search")
        context['TITLE'] = settings.TITLE
        context['CURRENCY'] = settings.CURRENCY
        return context
