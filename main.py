class MotulParse:
    import requests
    from bs4 import BeautifulSoup as bs
    from template import product_attributes

    def __init__(self, scan_url, volume):

        self.volume = volume  # объем
        self.weight = ''  # вес
        self.height = ''  # высота
        self.depth = ''  # глубина
        self.width = ''  # ширина
        self.product_sizes = f"{self.height} x {self.width} x {self.depth}"

        product_import_template = {'items': [{'category_id': 17028760, 'price': 'old_price', 'vat': "0.2",
                                              'vendor': "MOTUL", 'dimension_unit': "mm", 'weight_unit': "g",
                                              'height': self.height, 'depth': self.depth, 'width': self.width,
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
                {
                    "id": 7284,
                    "value": ""},
                {"id": 7286,  # type
                 "value": "3"}
            ]}
        ]}
        self.scan_url = scan_url
        self.product_import_template = product_import_template

    def add_descriptions(self, descriptions_list: list) -> dict:
        descriptions_dict = {}
        try:
            for item in descriptions_list:
                descriptions_dict[item[0]] = item[1]
        except IndexError:
            print("Переполнение")
        for i in descriptions_dict:
            if descriptions_dict[i] in self.product_attributes['attributes'][0]['engine_type']:
                self.product_import_template['items'][0]['attributes'][8]['collection'] = \
                    self.product_attributes['attributes'][0]['engine_type'][descriptions_dict[i]]
            elif descriptions_dict[i] in self.product_attributes['attributes'][0]['sae']:
                self.product_import_template['items'][0]['attributes'][9]['value'] = \
                    self.product_attributes['attributes'][0]['sae'][descriptions_dict[i]]
        return self.product_import_template

    def get_url(self):
        """Выполняет запрос и передает строку в фунцкию parse_info"""
        r = self.requests.get(self.scan_url)
        if r.status_code == 200:
            print("Соединение установлено ....")
            soup = self.bs(r.text, 'html.parser')
            return self.parse_info(soup)
        else:
            print("Connecting error")
            return False

    def run(self):
        """фунцкция для заполнения словаря значений в зависимости от объема. Возвращает ф-ю get_url"""
        if self.volume == 4:
            self.product_import_template['items'][0]['weight'] = 3610
            self.product_import_template['items'][0]['depth'] = 290
            self.product_import_template['items'][0]['width'] = 200
            self.product_import_template['items'][0]['height'] = 80
        elif self.volume == 5:
            self.product_import_template['items'][0]['weight'] = 4495
            self.product_import_template['items'][0]['depth'] = 300
            self.product_import_template['items'][0]['width'] = 190
            self.product_import_template['items'][0]['height'] = 150
        elif self.volume == 1:
            self.product_import_template['items'][0]['weight'] = 980
            self.product_import_template['items'][0]['depth'] = 230
            self.product_import_template['items'][0]['width'] = 90
            self.product_import_template['items'][0]['height'] = 130
        return self.get_url()

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
            descriptions_list = [i.text.replace("  ", '').replace('\n', '').split(":") for i in descriptions]
            if "8100" and "6100" in name:  # тип масла
                self.product_import_template['items'][0]['attributes'][10]['value'] = "4"
            return self.add_descriptions(descriptions_list)


if __name__ == '__main__':
    resp = MotulParse("https://motul.store/search/?q=107947", 1)
    print(resp.run())
