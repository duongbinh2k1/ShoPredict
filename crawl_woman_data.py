from crawler.shopee.run import crawl_woman_clothes_shopee
from process_data.run import clean_and_store_data, delete_file

woman_clothes_file =  crawl_woman_clothes_shopee()
clean_and_store_data(f'{woman_clothes_file}')
delete_file(f'{woman_clothes_file}')