"""
This file defines the message codes for multilanguage in the frontend
Using i18n standard, please check multilanguage folder to add or modify messages
assets/i18n/<lang>
"""



# Common Messages
OK_MSG = 'OK_MSG'
CREATED_MSG = 'CREATED_MSG'
NOT_FOUND_MSG = 'NOT_FOUND_MSG'
CONFLICT_MSG = 'CONFLICT_MSG'
UNPROCESSABLE_ENTITY_MSG = 'UNPROCESSABLE_ENTITY_MSG'
INTERNAL_SERVER_ERROR_MSG = 'INTERNAL_SERVER_ERROR_MSG'
SERVER_TIMEOUT_MSG = 'SERVER_TIMEOUT_MSG'

# Common Validations Messages
INVALID_ID = 'INVALID_ID' # Invalid Id


# Booking Validations Messages
BOOKING_ITEM_NOT_FOUND = 'BOOKING_ITEM_NOT_FOUND' # Item not found
BOOKING_USER_NOT_FOUND = 'BOOKING_USER_NOT_FOUND' # Item not found
BOOKING_ITEM_RELATION_CONFLICT = 'BOOKING_ITEM_RELATION_CONFLICT' # Item has conflicts with parent relationships
BOOKING_ITEM_NOT_AVAIL_DAY = 'BOOKING_ITEM_NOT_AVAIL_DAY' # Item is not available in the selected day
BOOKING_DATE_INVALID = 'BOOKING_DATE_INVALID'# Date must be equal or greater than today
BOOKING_INVALID_TIME_RANGE = 'BOOKING_INVALID_TIME_RANGE' # One or more time ranges do not have the correct format
BOOKING_TIME_LOWER_THAN_ACTUAL = 'BOOKING_TIME_LOWER_THAN_ACTUAL' #One or more times are lower than the current time
BOOKING_TIMES_NOT_AVAIL = 'BOOKING_TIMES_NOT_AVAIL' # Some selected times are not available
BOOKING_CREATED = 'BOOKING_CREATED' # Booking created successfully
BOOKING_NOT_FOUND = 'BOOKING_NOT_FOUND' # Booking not found
BOOKING_UPDATED = "BOOKING_UPDATED" # Booking updated successfully

# Area Validations Message
AREA_ITEM_NOT_FOUND = "AREA_ITEM_NOT_FOUND" # Area not found
AREA_ALREADY_EXIST = "AREA_ALREADY_EXIST" # Area aready exist for the selected site
AREA_SUCCESSFULLY_UPDATED = "AREA_SUCCESSFULLY_UPDATED" # Area successfully updated
AREA_SUCCESSFULLY_DELETED = "AREA_SUCCESSFULLY_DELETED" # Area successfully deleted
AREA_SUCCESSFULLY_CREATED = "AREA_SUCCESSFULLY_CREATED" # Area created successfully
AREA_DELETE_HAS_RELATIONS = "AREA_DELETE_HAS_RELATIONS" # Area cannot be deleted, has relationships with some categories


# Country Validations Message
COUNTRY_ITEM_NOT_FOUND = "COUNTRY_ITEM_NOT_FOUND" # Country not found
COUNTRY_ALREADY_EXIST = "COUNTRY_ALREADY_EXIST" # Country already exist
COUNTRY_SUCCESSFULLY_CREATED = "COUNTRY_SUCCESSFULLY_CREATED" # Country successfully created
COUNTRY_SUCCESSFULLY_UPDATED = "COUNTRY_SUCCESSFULLY_UPDATED" # Country successfully updated
COUNTRY_SUCCESSFULLY_DELETED = "COUNTRY_SUCCESSFULLY_DELETED" # Country successfully deleted
COUNTRY_DELETE_HAS_RELATIONS = "COUNTRY_DELETE_HAS_RELATIONS" # Country cannot be deleted, has relationships with some sites

# Category Validators Messages
CATEGORY_ITEM_NOT_FOUND = "CATEGORY_ITEM_NOT_FOUND" # Category not found
CATEGORY_ALREADY_EXIST = "CATEGORY_ALREADY_EXIST" # Category already exists for the selected area
CATEGORY_DAYS_INVALID = "CATEGORY_DAYS_INVALID" # One or more days are invalid
CATEGORY_OPEN_TIME_HIGHER = "CATEGORY_OPEN_TIME_HIGHER" # Open time can not be higher than close time
CATEGORY_SUCCESSFULLY_CREATED = "CATEGORY_SUCCESSFULLY_CREATED" # Category created successfully
CATEGORY_SUCCESSFULLY_UPDATED = "CATEGORY_SUCCESSFULLY_UPDATED" # Category updated successfully
CATEGORY_SUCCESSFULLY_DELETED = "CATEGORY_SUCCESSFULLY_DELETED" # Category deleted successfully
CATEGORY_DELETE_HAS_RELATIONS = "CATEGORY_DELETE_HAS_RELATIONS" # Category cannot be deleted, has relationships with some items

# Item Validations Message
ITEM_NOT_FOUND = "ITEM_NOT_FOUND" # Item not found
ITEM_ALREADY_EXIST = "ITEM_ALREADY_EXIST" # Item already exist
ITEM_SUCCESSFULLY_CREATED = "ITEM_SUCCESSFULLY_CREATED" # Item successfully created
ITEM_SUCCESSFULLY_UPDATED = "ITEM_SUCCESSFULLY_UPDATED" # Item successfully updated
ITEM_SUCCESSFULLY_DELETED = "ITEM_SUCCESSFULLY_DELETED" # Item successfully deleted

# Site Validations Message
SITE_NOT_FOUND = "SITE_NOT_FOUND" # SITE not found
SITE_ALREADY_EXIST = "SITE_ALREADY_EXIST" # Site aready exist for the selected country
SITE_SUCCESSFULLY_CREATED = "SITE_SUCCESSFULLY_CREATED" # SITE successfully created
SITE_SUCCESSFULLY_UPDATED = "SITE_SUCCESSFULLY_UPDATED" # SITE successfully updated
SITE_SUCCESSFULLY_DELETED = "SITE_SUCCESSFULLY_DELETED" # SITE successfully deleted
SITE_DELETE_HAS_RELATIONS = "SITE_DELETE_HAS_RELATIONS" # Site cannot be deleted, has relationships with some areas