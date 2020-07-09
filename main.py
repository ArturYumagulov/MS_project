
class MotulParse:
    import requests
    from bs4 import BeautifulSoup as bs

    def __init__(self, scan_url):
        product_import_template = {'items':
                                       [{'category_id': 17028760,
                                         'price': 'old_price',
                                         'vat': "0.2",
                                         'vendor': "MOTUL",
                                         'dimension_unit': "mm",
                                         'weight_unit': "g",
                                         'images': [{'file_name': "",
                                                     'defaut': True}]}]}
        self.scan_url = scan_url
        self.product_import_template = product_import_template



    # def run(self):
    #     for i in self.get_url():
    #         print(i)
    #     print("Save data? Y/N:")
    #     while True:
    #         x = input()
    #         if x == "Y":
    #             print("Saving...")
    #             break
    #         else:
    #             print("Программа завершена")
    #             break

    def run(self, volume):
        print(self.get_url())

    def save_data(self):
        pass

    def get_url(self):
        dct = {'items': [{'category_id': 17028760, 'price': 'old_price', 'vat': "0.2", 'vendor': "Motul",
                          'height': 300, 'depth': 250, 'width': 120, 'dimension_unit': "mm", 'weight': 4000,
                          'weight_unit': "g", 'images': [{'file_name': "", 'defaut': True}]}]}
        r = self.requests.get(self.scan_url)
        if r.status_code == 200:
                print("Соединение установлено ....")
                soup = self.bs(r.text, 'html.parser')
                divs = soup.find_all('div', attrs={'class': 'catalog_content_products-item'})
                for div in divs:
                    link = div.find('a', attrs={'class': 'catalog_content_products-item-href'})
                    clear_link = link.get('href')
                    dct['items'][0]['offer_id'] = div.find('p', attrs={'class': 'catalog-card__name'}).text
                    dct['items'][0]['old_price'] = div.find('span', attrs={'class': 'catalog_content_products-price-num'}).\
                        text.replace('руб', '').replace('.', '').strip()
                    descriptions_html = self.requests.get(f'https://motul.store{clear_link}')
                    descriptions_soup = self.bs(descriptions_html.text, 'html.parser')
                    image = descriptions_soup.find('a', attrs={'data-jbox-image': 'catalog-detail'})
                    dct['items'][0]['images'][0]['file_name'] = f"https://motul.store{image.get('href')}"
                    product_category = descriptions_soup.find('div', attrs={'class': 'product_description-category'}).text
                    name = descriptions_soup.find('h1', attrs={'class': 'product_description-title'}).text
                    dct['items'][0]['name'] = f"{product_category}{name}"
                    descriptions = descriptions_soup.find_all('div', attrs={'class': 'product_description-text'})
                    # yield descriptions_title.text, offer_id.text, price.text.replace('руб.', '').replace('/', '').\
                    #     replace('л', '').replace(' ', ''), clear_link, descriptions_list
                    return dct
        else:
            print("Connecting error")


if __name__ == '__main__':
    resp = MotulParse("https://motul.store/search/?q=109775")
    resp.run()
