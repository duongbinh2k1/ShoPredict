from playwright.sync_api import Page, ElementHandle

def get_element_by_selector(page: Page, selector: str) -> ElementHandle:
    try:
        element = page.query_selector_all(selector)
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

def click_element(element: ElementHandle):
    if element:
        element.click()

def fill_input(element: ElementHandle, text: str):
    if element:
        element.fill(text)

def get_element_by_inner_text(page: Page, text: str) -> ElementHandle:
    try:
        element = page.get_by_text(text)
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_element_by_inner_text_from_element(parent_element: ElementHandle, text: str) -> ElementHandle:
    try:
        element = parent_element.query_selector(f':text("{text}")')
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_nth_element_by_selector(page: Page, selector: str, n: int) -> ElementHandle:
    try:
        elements = page.query_selector_all(selector)
        if n < len(elements):
            return elements[n]
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_page_title(page: Page) -> str:
    try:
        return page.title()
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def scroll_into_view(page: Page, element):
    element.scroll_into_view_if_needed()

def close_popup(page: Page):
    try: 
        close_btn = get_nth_element_by_selector(page, '.shopee-popup__close-btn', 0)
        if close_btn:
            click_element(close_btn)
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_element_by_element(element: ElementHandle, selector: str):
    try:
        element = element.query_selector(selector)
        return element
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_image_url(element: ElementHandle):
    try:
        image_element = element.query_selector('img')
        if image_element:
            image_url = image_element.get_attribute('src')
        else:
            image_url = None

        return image_url
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_text(element: ElementHandle):
    try:
        return element.inner_text()
    except Exception as e: 
        print(f"Error{e}")
        return None

def get_element_position(page: Page, element: ElementHandle):
    if element:
        bounding_box = element.bounding_box()
        return bounding_box["x"],bounding_box["y"]
    else:
        return None
    
def scroll_with_mouse(page: Page, x: int, y: int):
    mouse = page.mouse
    mouse.wheel(x, y)

def smooth_scroll_with_mouse(page: Page, delta_x: int, delta_y: int, duration_ms: int, num_steps: int):
    dx = delta_x / num_steps
    dy = delta_y / num_steps
    mouse = page.mouse

    for _ in range(num_steps):
        mouse.wheel(dx, dy)


def locate_element(page: Page, selector: str):
    try:
        element = page.locator(selector)
        if element:
            return element
    except Exception as e:
        print(f'Error:{{e}}')
        return None
    
def get_parent_by_element(element: ElementHandle):
    try:
        parent = element.query_selector('xpath=..')
        if parent:
            return parent
    except Exception as e:
        print(f'Error:{e}')
        return None
    
def get_nth_element_by_selector_from_element(element: ElementHandle, selector: str, n: int) -> ElementHandle:
    try:
        elements = element.query_selector_all(selector)
        if n < len(elements):
            return elements[n]
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def locate_all_element(page: Page, selector: str):
    try:
        element = page.locator(selector).all()
        if element:
            return element
    except Exception as e:
        print(f'Error:{{e}}')
        return None
    
def get_all_element_by_element(element: ElementHandle, selector: str):
    try:
        elements = element.query_selector_all(selector)
        return elements
    except Exception as e:
        print(f"Error: {e}")
        return None
