from flask_restful import Resource
from controllers.site.controller import SiteController
from controllers.site.site_by_id.controller import SiteById
from controllers.site.site_by_filters.controller import SiteByFilters
from controllers.country.controller import Country
from controllers.country.country_by_id.controller import CountryById
from controllers.area.controller import Area
from controllers.area.area_by_id.controller import AreaById 
from controllers.area.area_by_filters.controller import AreaByFilters
from controllers.category.controller import CategoryController
from controllers.category.category_by_id.controller import CategoryByIdController
from controllers.category.category_by_filters.controller import CategoryByFilters
from controllers.item.controller import Item
from controllers.item.item_by_id.controller import ItemById
from controllers.item.item_by_filters.controller import ItemByFilters
from controllers.booking.controller import BookingAvailableTimesController, BookingController
from controllers.booking.booking_by_id.controller import BookingById

from flask_restful import Api

def addServiceLayer(api: Api):
    # Site
    api.add_resource(SiteController, SiteController.route)
    api.add_resource(SiteById, SiteById.route)
    api.add_resource(SiteByFilters, SiteByFilters.route)
    # Country
    api.add_resource(Country, Country.route)
    api.add_resource(CountryById, CountryById.route)
    # Area
    api.add_resource(Area, Area.route)
    api.add_resource(AreaById, AreaById.route)
    api.add_resource(AreaByFilters, AreaByFilters.route)
    # Category
    api.add_resource(CategoryController, CategoryController.route)
    api.add_resource(CategoryByIdController, CategoryByIdController.route)
    api.add_resource(CategoryByFilters, CategoryByFilters.route)
    # Item
    api.add_resource(Item, Item.route)
    api.add_resource(ItemById, ItemById.route)
    api.add_resource(ItemByFilters, ItemByFilters.route)
    # Booking
    api.add_resource(BookingAvailableTimesController, BookingAvailableTimesController.route)
    api.add_resource(BookingController, BookingController.route)
    api.add_resource(BookingById, BookingById.route)
