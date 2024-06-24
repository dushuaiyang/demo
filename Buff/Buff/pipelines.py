import csv
import pymysql


class BuffPipeline:
    def open_spider(self, spider):
        self.file = open(file='arms.csv', mode='a', encoding='utf-8', newline='')
        self.csvwriter = csv.writer(self.file)
        self.csvwriter.writerow(
            ['biglabel', 'biglabel_link', 'id', 'name', 'market_name', 'price', 'exterior_wear', 'quality', 'rarity',
             'type', 'weapon_type'])

    def process_item(self, item, spider):
        self.csvwriter.writerow(
            [item['biglabel'], item['biglabel_link'], item['id'], item['name'], item['market_name'], item['price'],
             item['exterior_wear'], item['quality'], item['rarity'], item['type'], item['weapon_type']])
        return item

    def close_spider(self, spider):
        self.file.close()


class MysqlPipeline:
    def open_spider(self, spider):
        self.mysql = pymysql.connect(host='localhost', user='root', password='12345678', db='sys', port=3306,
                                     charset='utf8')
        self.cursor = self.mysql.cursor()


    def process_item(self, item, spider):
        insert_sql = '''insert into buff(biglabel, biglabel_link, id, name, market_name, price, exterior_wear, quality, rarity, type, weapon_type) value ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
        item['biglabel'], item['biglabel_link'], item['id'], item['name'], item['market_name'], item['price'],
        item['exterior_wear'], item['quality'], item['rarity'], item['type'], item['weapon_type'])
        self.cursor.execute(insert_sql)
        self.mysql.commit()  # Ã·Ωª
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.mysql.close()