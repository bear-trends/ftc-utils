# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FtcScrapyItem(scrapy.Item):
    es_index = 'items'

    id = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    city = scrapy.Field()
    color1 = scrapy.Field()
    color2 = scrapy.Field()
    country = scrapy.Field()
    created_at = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    photo_ids = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()
    updated_at = scrapy.Field()
    view_count = scrapy.Field()
    url = scrapy.Field()
    user_id = scrapy.Field()
    sku = scrapy.Field()
    platform = scrapy.Field()
    sourced_at = scrapy.Field()
    like_count = scrapy.Field()
    negotiable = scrapy.Field()


class FtcScrapyUser(scrapy.Item):
    es_index = 'users'

    id = scrapy.Field()
    login = scrapy.Field()
    gender = scrapy.Field()
    item_count = scrapy.Field()
    forum_msg_count = scrapy.Field()
    followers_count = scrapy.Field()
    following_count = scrapy.Field()
    photo_id = scrapy.Field()
    created_at = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    business_id = scrapy.Field()
    total_items_count = scrapy.Field()
    description = scrapy.Field()
    updated_at = scrapy.Field()
    url = scrapy.Field()
    platform = scrapy.Field()
    sourced_at = scrapy.Field()
    ebay_evaluation_score = scrapy.Field()
    positive_evaluations_percentage = scrapy.Field()
    items_bought = scrapy.Field()
    items_wished = scrapy.Field()
    items_sold = scrapy.Field()


class FtcScrapyBrand(scrapy.Item):
    es_index = 'brands'

    id = scrapy.Field()
    title = scrapy.Field()
    favourite_count = scrapy.Field()
    item_count = scrapy.Field()
    is_luxury = scrapy.Field()
    url = scrapy.Field()
    platform = scrapy.Field()
    sourced_at = scrapy.Field()


class FtcScrapyAccounts(scrapy.Item):
    es_index = 'accounts'

    id = scrapy.Field()
    name = scrapy.Field()
    legal_code = scrapy.Field()
    email = scrapy.Field()
    phone_number = scrapy.Field()
    legal_name = scrapy.Field()
    nationality = scrapy.Field()
    entity_type = scrapy.Field()
    status = scrapy.Field()
    country = scrapy.Field()
    platform = scrapy.Field()
    sourced_at = scrapy.Field()


class FtcScrapyPhotos(scrapy.Item):
    es_index = 'photos'

    id = scrapy.Field()
    image_no = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    dominant_color = scrapy.Field()
    dominant_color_opaque = scrapy.Field()
    url = scrapy.Field()
    is_main = scrapy.Field()
    platform = scrapy.Field()
    sourced_at = scrapy.Field()
