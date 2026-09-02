import pickle
import os
import sys
from pathlib import Path
from DrissionPage import ChromiumOptions, ChromiumPage
from DrissionPage._elements.chromium_element import ChromiumElement
from DrissionPage._functions.elements import ChromiumElementsList

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings.base import BASE_DIR

COOKIES_PATH = BASE_DIR / 'data' / 'Cookies'
DATA_DOWNLOAD = BASE_DIR / 'data' / 'Downloads'
DATA_USER = BASE_DIR / 'data' / 'User_data'

class Scraper:
    def __init__(self):
        self._co = ChromiumOptions()
        self._co.set_browser_path('/usr/bin/brave-browser')
        self._co.auto_port()
        self.page = ChromiumPage(self._co)
        
    def save_full_cookies(self, filenames='cookies.pkl'):
        # Default filenames is 'cookies.pkl'
        cookies_list = self.page.cookies()   # list dict
        path = COOKIES_PATH / filenames
        with open(path, 'wb') as f:
            pickle.dump(cookies_list, f)
            
    def load_cookies(self, url, filenames='cookies.pkl'):
        
        self.page.get(url)
        path = COOKIES_PATH / filenames
        if os.path.exists(path):
            with open(path, 'rb') as f:
                cookies_list = pickle.load(f)
            
            for cookie in cookies_list:
                self.page.set.cookies(cookie)
            print("Loaded cookies")
            self.page.refresh()
            
    def go_to(self, url):
        self.page.get(url)
        
    def get_one(self, css:str) -> ChromiumElement:
        return self.page.ele(css)
    
    def get_many(self, css:str) -> ChromiumElementsList:
        return self.page.eles(css)             
    
    def close(self):
        self.save_full_cookies()
        self.page.close()
        self.page.quit()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()