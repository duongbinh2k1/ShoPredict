from crawler.shopee.run import crawl_man_clothes_shopee, crawl_woman_clothes_shopee
from process_data.run import clean_and_store_data

man_clothes_file = crawl_man_clothes_shopee()
clean_and_store_data(f'{man_clothes_file}')

woman_clothes_file =  crawl_woman_clothes_shopee()
clean_and_store_data(f'{woman_clothes_file}')