import scrapy
import time
import json
import jsonpath
from ..items import BuffItem


class ArmsSpider(scrapy.Spider):
    name = 'arms'
    allowed_domains = ['buff.163.com']
    start_urls = ['https://buff.163.com/market/csgo']

    def parse(self, response):
        node_list = response.xpath('//*[@class="h1z1-selType type_csgo"]/div')
        for node in node_list:
            base_data = {}
            base_data['biglabel'] = node.xpath('.//p/text()').get()
            base_data['value'] = node.xpath('.//p/@value').get()
            base_data[
                'biglable_link'] = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&category_group={}&use_suggestion=0&trigger=undefined_trigger&_={}'.format(
                base_data['value'], int(time.time() * 1000))
            cookie = '_ntes_nuid=705c6237507628f135f84c3ec5c4310e; _ntes_nnid=705c6237507628f135f84c3ec5c4310e,1703047176973; Device-Id=aTd2ZErepzk3RoD2Z61o; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=ZFzs08mzyq2f.yDLALHesi8CCGsJhip2VdHvyZOYCrmSl.DwlvG8Q0U9L1tVOpOQLhvNqQAWS0phFU4z02pAhxp9RCVSPT76QbFuhCFK_46fn76SgcVsiEJIusIqJqCzwFDwmJb7Nt0wDqe5Lo8bnu5DU7MjHUK9VmiK.WmIn4eK0_ki3xEuiOhjZKQvYtW9z_GYPuT9SpFnvZx5rHwnzYjE_oqNQnMYrNaWrdjS.mkuI; S_INFO=1717680670|0|0&60##|15537072693; P_INFO=15537072693|1717680670|1|netease_buff|00&99|null&null&null#hen&410700#10#0|&0|null|15537072693; qr_code_verify_ticket=13d0MDgad60cb44246bcbe4e7cfa402f5aa3; remember_me=U1081646103|2G0UDommjclge4YX8xg29ziYvhWiAlvM; session=1-Opau8q88YUZZCrKVpm4P3R11iVlUkaFplDGwW185AQLn2025194319; csrf_token=IjkxMjQ5ZDJkYzAyZDdhNjBiZTc3YTU5ODJhOGYyMzg1MDQzYjVlZjEi.GUNSFA.hghOUIwkw2vwok4aKIYDi6eO4JM'

            cookies = {data.split('=')[0]: data.split('=')[1] for data in cookie.split(';')}
            yield scrapy.Request(
                url=base_data['biglable_link'],
                callback=self.parse_img,
                meta={'base_data': base_data},
                cookies=cookies
            )

    def parse_img(self, response):
        base_data = response.meta['base_data']
        json_data = json.loads(response.text)
        id = jsonpath.jsonpath(json_data, '$..items[*].id')
        # for item in json_data['data']['items']:
        #     id =item['goods_info']['info']['tags']['category']['id'])
        name = jsonpath.jsonpath(json_data, '$..items[*].name')
        market_name = jsonpath.jsonpath(json_data, '$..items[*].market_hash_name')
        price = jsonpath.jsonpath(json_data, '$..items[*].sell_min_price')
        exterior_wear = jsonpath.jsonpath(json_data, '$..info.tags.exterior.localized_name')
        quality = jsonpath.jsonpath(json_data, '$..info.tags.quality.localized_name')
        rarity = jsonpath.jsonpath(json_data, '$..info.tags.rarity.localized_name')
        type = jsonpath.jsonpath(json_data, '$..info.tags.type.localized_name')
        weapon_type = jsonpath.jsonpath(json_data, '$..info.tags.weapon.localized_name')
        for i in range(len(id)):
            item = BuffItem()
            item['biglabel'] = base_data['biglabel']
            item['biglabel_link'] = base_data['biglable_link']
            item['id'] = id[i]
            item['name'] = name[i]
            item['market_name'] = market_name[i]
            item['price'] = price[i]
            if not exterior_wear:
                item['exterior_wear'] = ''
            else:
                item['exterior_wear'] = exterior_wear[i]
            if not quality:
                item['quality'] = ''
            else:
                item['quality'] = quality[i]
            if not rarity:
                item['rarity'] = ''
            else:
                item['rarity'] = rarity[i]
            if not type:
                item['type'] = ''
            else:
                item['type'] = type[i]
            if not weapon_type:
                item['weapon_type'] = ''
            else:
                item['weapon_type'] = weapon_type[i]
            yield item

        page = jsonpath.jsonpath(json_data, '$.data.page_num')[0] + 1
        pages = jsonpath.jsonpath(json_data, '$.data.total_page')[0]
        if page <= pages:
            # print(base_data['value'])
            next_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num={}&category_group={}&use_suggestion=0&trigger=undefined_trigger&_={}'.format(
                page, base_data['value'], int(time.time() * 1000))
            cookie = '_ntes_nuid=705c6237507628f135f84c3ec5c4310e; _ntes_nnid=705c6237507628f135f84c3ec5c4310e,1703047176973; Device-Id=aTd2ZErepzk3RoD2Z61o; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=ZFzs08mzyq2f.yDLALHesi8CCGsJhip2VdHvyZOYCrmSl.DwlvG8Q0U9L1tVOpOQLhvNqQAWS0phFU4z02pAhxp9RCVSPT76QbFuhCFK_46fn76SgcVsiEJIusIqJqCzwFDwmJb7Nt0wDqe5Lo8bnu5DU7MjHUK9VmiK.WmIn4eK0_ki3xEuiOhjZKQvYtW9z_GYPuT9SpFnvZx5rHwnzYjE_oqNQnMYrNaWrdjS.mkuI; S_INFO=1717680670|0|0&60##|15537072693; P_INFO=15537072693|1717680670|1|netease_buff|00&99|null&null&null#hen&410700#10#0|&0|null|15537072693; qr_code_verify_ticket=13d0MDgad60cb44246bcbe4e7cfa402f5aa3; remember_me=U1081646103|2G0UDommjclge4YX8xg29ziYvhWiAlvM; session=1-Opau8q88YUZZCrKVpm4P3R11iVlUkaFplDGwW185AQLn2025194319; csrf_token=IjkxMjQ5ZDJkYzAyZDdhNjBiZTc3YTU5ODJhOGYyMzg1MDQzYjVlZjEi.GUNSFA.hghOUIwkw2vwok4aKIYDi6eO4JM'

            cookies = {data.split('=')[0]: data.split('=')[1] for data in cookie.split(';')}
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_img,
                meta={'base_data': base_data},
                cookies=cookies
            )