from crawler.base.page_manager import PageManager
from crawler.constants import *
from crawler.utils import page_actions
import time
import pandas as pd

class SPPage():

    def __init__(self, page: PageManager):
        self.page = page

    def go_to_home_page(self):
        self.page.goto(SHOPEE_HOME_URL)
        time.sleep(1)
        page_actions.close_popup(self.page)
        return self.page

    def go_to_woman_clothes(self):
        try:
            self.go_to_home_page()
            time.sleep(1)
            element = page_actions.get_nth_element_by_selector(
                self.page, '.home-category-list__category-grid', 1)
            page_actions.click_element(element)
            time.sleep(1)
            print("Go to woman clothes success")
            return self.page

        except Exception as e:
            if "intercepts pointer events" in str(e):
                page_actions.close_popup(self.page)
                self.go_to_man_clothes()
            else:
                print(f"Error: {e}")

    def go_to_man_clothes(self):
        try:
            self.go_to_home_page()
            time.sleep(1)
            element = page_actions.get_nth_element_by_selector(
                self.page, '.home-category-list__category-grid', 0)
            page_actions.click_element(element)
            time.sleep(1)
            print("Go to man clothes success")
            return self.page

        except Exception as e:
            if "intercepts pointer events" in str(e):
                page_actions.close_popup(self.page)
                self.go_to_man_clothes()
            else:
                print(f"Error: {e}")

    def get_all_product(self):
        try:
            i = 1
            products = []
            while i <= MAX_PAGE:
                shopee_page_controller = page_actions.get_nth_element_by_selector(
                    self.page, '.shopee-page-controller', 0)
                _, y = page_actions.get_element_position(
                    self.page, shopee_page_controller)
                page_actions.smooth_scroll_with_mouse(self.page, 0, y, 500, 20)
                time.sleep(1)
                product_containers = page_actions.get_element_by_selector(
                    self.page, '.shopee-search-item-result__item[data-sqe="item"]')


                for container in product_containers:
                    product = {}

                    image = page_actions.get_image_url(container)
                    if (image):
                        product['image'] = image

                    name_box = page_actions.get_element_by_element(
                        container, '[data-sqe="name"]')
                    
                    parent = page_actions.get_parent_by_element(name_box)

                    childs = page_actions.get_all_element_by_element(parent, '>div')
                    product['name'] = page_actions.get_text(childs[0])
                    product['price'] = page_actions.get_text(childs[1])
                    product['sold_quantity'] = page_actions.get_text(childs[2])
                    product['location'] = page_actions.get_text(childs[3])
                    
                    products.append(product)
                print(f'Get all product on page {i}')
                i = i + 1
                next_page = page_actions.get_element_by_inner_text_from_element(shopee_page_controller, f'{i}')
                page_actions.click_element(next_page)

            return products

        except Exception as e:
            print(f"Error: {e}")

    def list_to_df(self, list_data, output):
        try:
            df = pd.DataFrame(list_data)
            df.to_csv(output, index=False)
            return df
        except Exception as e:
            print(f"Error:{e}")
