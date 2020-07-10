
class MotulParse:
    import requests
    from bs4 import BeautifulSoup as bs
    from template import product_attributes

    def __init__(self, scan_url):

        self.volume = 4
        self.weight = ''
        self.product_sizes = ''

        product_import_template = {'items': [{'category_id': 17028760, 'price': 'old_price', 'vat': "0.2",
                                              'vendor': "MOTUL", 'dimension_unit': "mm", 'weight_unit': "g",
                                              'images': [{'file_name': "", 'defaut': True}], 'attributes': [
                {"id": 7194,  # объем
                 "value": f'{self.volume}'},
                {"id": 8084,    # срок годности
                 "value": "1095"},
                {'id': 9048,  # навзание модели
                 'value': ""},
                {"id": 4382,  # Размеры
                 "value": self.product_sizes},
                {"id": 4383,  # Вес товара, г
                 "value": self.weight},
                {"id": 4386,  # Упаковка
                 "collection": [
                     "96"]},
                {"id": 4389,  # Страна изготовитель
                 "value": "10"},
                {"id": 7206,  # Тип тех
                 "collection": [
                     "7"
                 ]},
                {"id": 7290,  # тип двигателя
                 "collection": [
                     ""]},
            ]}
        ]}
        self.scan_url = scan_url
        self.product_import_template = product_import_template

    def add_descriptions(self, descriptions):
        import re
        for i in descriptions:
            try:
                if re.search(r'[0-9]-тактный', i.text).group(0) in self.product_attributes['attributes'][0]['engine_type']:
                    item = self.product_attributes['attributes'][0]['engine_type'][re.search(r'[0-9]-тактный',
                                                                                             i.text).group(0)]
                    self.product_import_template['items'][0]['attributes'][8]['collection'][0] = f'{item}'
                    print("first if")
                    continue
                elif re.search(r'10W40|5W40', i.text) in self.product_attributes['attributes'][0]['sae']:
                    print(self.product_attributes['attributes'][0]['sae'])


            except AttributeError:
                print("No data")

    def get_url(self):
        r = self.requests.get(self.scan_url)
        if r.status_code == 200:
            print("Соединение установлено ....")
            soup = self.bs(r.text, 'html.parser')
            return self.parse_info(soup)
        else:
            print("Connecting error")

    def add_attribute(self, dict_template):
        if self.volume == 4:
            self.product_sizes = "300x250x120"
            self.weight = "400"
        elif self.volume == 5:
            self.product_sizes = '290x210x90'
        elif self.volume == 1:
            pass

    def parse_info(self, soup):
        divs = soup.find_all('div', attrs={'class': 'catalog_content_products-item'})
        for div in divs:
            link = div.find('a', attrs={'class': 'catalog_content_products-item-href'})
            clear_link = link.get('href')
            self.product_import_template['items'][0]['offer_id'] = div.find('p', attrs={'class': 'catalog-card__name'}).text
            self.product_import_template['items'][0]['old_price'] = div.find('span', attrs={
                'class': 'catalog_content_products-price-num'}).text.replace('руб', '').replace('.', '').strip()
            descriptions_html = self.requests.get(f'https://motul.store{clear_link}')
            descriptions_soup = self.bs(descriptions_html.text, 'html.parser')
            image = descriptions_soup.find('a', attrs={'data-jbox-image': 'catalog-detail'})
            self.product_import_template['items'][0]['images'][0]['file_name'] = f"https://motul.store{image.get('href')}"
            product_category = descriptions_soup.find('div', attrs={'class': 'product_description-category'}).text
            name = descriptions_soup.find('h1', attrs={'class': 'product_description-title'}).text
            self.product_import_template['items'][0]['name'] = f"{product_category}{name}"
            self.product_import_template['items'][0]['attributes'][2]['value'] = name
            descriptions = descriptions_soup.find_all('div', attrs={'class': 'product_description-text'})
            self.add_descriptions(descriptions)
            # for i in descriptions:
            #     print(i.text)

    def run(self):
        print(self.get_url())
        # print(self.product_import_template)


if __name__ == '__main__':
    resp = MotulParse("https://motul.store/search/?q=109775")
    resp.run()
