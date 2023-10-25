from crawler.shopee.sp_page import SPPage
from crawler.base.browser_manager import BrowserManager
from crawler.base.page_manager import PageManager
from crawler.utils.gg_drive import GGDrive

import time
from playwright.sync_api import sync_playwright
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

def crawl_man_clothes_shopee():
    with sync_playwright() as p:

        gg_drive = GGDrive()
        gg_drive.authenticate()

        browser = BrowserManager(p)
        browser.launch_browser()

        page_manager = PageManager(browser)
        page = page_manager.new_page()

        sp_page = SPPage(page)
        sp_page.go_to_man_clothes()
        time.sleep(1)
        products =  sp_page.get_all_product()

        sp_df = sp_page.list_to_df(products)
        sp_page.df_to_csv(sp_df, f'./files/woman_clothes_shopee_{today}.csv')

        gg_drive.upload_df(sp_df, f'man_clothes_shopee_{today}.csv')

        browser.close_browser()

def crawl_woman_clothes_shopee():
    with sync_playwright() as p:
        browser = BrowserManager(p)
        browser.launch_browser()

        gg_drive = GGDrive()
        gg_drive.authenticate()


        page_manager = PageManager(browser)
        page = page_manager.new_page()

        sp_page = SPPage(page)
        sp_page.go_to_woman_clothes()
        products = sp_page.get_all_product()

        sp_df = sp_page.list_to_df(products)
        sp_page.df_to_csv(sp_df, f'./files/woman_clothes_shopee_{today}.csv')

        gg_drive.upload_df(sp_df, f'woman_clothes_shopee_{today}.csv')

        browser.close_browser()
