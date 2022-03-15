from modeltranslation.translator import translator, TranslationOptions
from bazar.models import City, Category, Listing


class CityTranslationOptions(TranslationOptions):
    fields = ('description',)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class ListingTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


translator.register(City, CityTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Listing, ListingTranslationOptions)
