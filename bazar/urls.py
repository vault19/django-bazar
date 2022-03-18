from django.urls import path

from bazar.views import AllListingsView, RegisterView, ProfileView, SearchListView, ListingCreateView, \
    ListingUpdateView, ListingDetailView, ListingDeleteView, CategoriesListView, CategoryListView, CityListView, \
    CityCategoryListView


urlpatterns = [
    path('', AllListingsView.as_view(), name='index_view'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('register/profile/', ProfileView.as_view(), name='profile_view'),
    path('search/', SearchListView.as_view(), name='search_list_view'),
    path('listing/create/<str:category_slug>/', ListingCreateView.as_view(), name='listing_create_category_view'),
    path('listing/create/', ListingCreateView.as_view(), name='listing_create_view'),
    path('listing/<uuid:pk>/update/', ListingUpdateView.as_view(), name='listing_update_view'),
    path('listing/<uuid:pk>/delete/', ListingDeleteView.as_view(), name='listing_delete_view'),
    path('listing/<uuid:pk>/', ListingDetailView.as_view(), name='listing_detail_view'),
    path('categories/', CategoriesListView.as_view(), name='categories_list_view'),
    path('catergory/<str:category_slug>/', CategoryListView.as_view(), name='category_list_view'),
    path('city/<str:city_slug>/', CityListView.as_view(), name='city_list_view'),
    path('city/<str:city_slug>/<str:category_slug>/', CityCategoryListView.as_view(), name='city_category_list_view'),
]
