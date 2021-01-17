import re

class IkeaProductsSpider:  

    def __init__(self, csv_filename): 
        if csv_filename is None:
            raise Exception('Filename fo rproduct csv is missing.')

        if re.search('\w+.csv', csv_filename):
            raise Exception('Filename for product csv fails to meet requirements.')

        self.product_search_url = 'https://sik.search.blue.cdtapps.com/ca/en/product-list-page/more-products?category={category_id}&start=0&end=99999999'
        self.csv_filename = csv_filename
        self.completed = False

    def crawl_products(self):
        for index, row in ikea_category_df.iterrows():
            try:
                product_search_url = self.product_search_url
                product_search_url = product_search_url.format(category_id=row['category_id'])
                
                with urllib.request.urlopen(product_search_url) as req_data:
                    data = json.loads(req_data.read().decode())
                    df = pd.DataFrame.from_dict(data['moreProducts']['productWindow'])
                    df.to_csv("something.csv", mode='a', index=False)
                    
                    print('Updated BigQuery data. Cateogory: {category_name}'.format(category_name=row['category_name']))

            except Exception as ex:
                print("Error in sending BigQuery Data: " + str(ex))
                break
        
        self.completed = True