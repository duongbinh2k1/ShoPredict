from crawler.shopee.run import crawl_man_clothes_shopee
from process_data.run import clean_and_store_data, delete_file

man_clothes_file = crawl_man_clothes_shopee()
clean_and_store_data(f'{man_clothes_file}')
delete_file(f'{man_clothes_file}')
