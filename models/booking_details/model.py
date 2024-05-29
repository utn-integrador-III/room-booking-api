from models.area.model import AreaModel
from models.country.model import CountryModel
from models.site.model import SiteModel
from models.category.model import CategoryModel
from models.item.model import ItemModel


class BookingDetailsModel():
    def __init__(self, country_id=None, site_id=None, area_id=None, category_id=None, item_id=None, **kwargs):
        self.country = CountryModel.country_factory(country_id)
        self.site = SiteModel.site_factory(site_id)
        self.area = AreaModel.area_factory(area_id)
        self.category = CategoryModel.category_factory(category_id)
        self.item = ItemModel.item_factory(item_id)


