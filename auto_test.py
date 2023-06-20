import pathlib
import os
import sys

PATH = ""

if len(sys.argv) > 1:
    PATH = sys.argv[1]
else:
    PATH = str(pathlib.Path(__file__).parent.resolve())

def make_init_py(path):
    pathlib.Path(path + "/__init__.py").touch()

def make_base_obj():
    f = open(rf"{PATH}\src\models\baseObj.py", "w")
    to_write = """
import json

class baseObj:

    def to_json(self) -> str:
        
        result = {}
        for key, val  in self.__dict__.items():
            if val is not None:
                if key.startswith("_"):
                    result[key[1:]] = val
                else:
                    result[key] = val
        return result

    def __str__(self):
        return json.dumps(self.to_json())
    
    """

    f.write(to_write)
    f.close()


def make_base_page():

    f = open(rf"{PATH}\src\pages\base.py", "w")
    to_write = """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class Base_page:
    def __init__(self, driver: webdriver):
        self._driver = driver

    def find_element(self, by_find, token, wait=5):
        elem = WebDriverWait(self._driver, wait).until(EC.presence_of_element_located((by_find, token)))
        return elem

    def find_elements(self, by_find, token):
        elements = self._driver.find_elements(by_find, token)
        return elements

    def close(self):
        self._driver.quit()
    """
    f.write(to_write)
    f.close()


def make_directorys_and_files():
    make_init_py(PATH)
    dirs = ["/src", "/test", "/API"]
    for itm in dirs:
        path_to = PATH + itm
        os.mkdir(path_to)
        make_init_py(path_to)

    test_path = PATH + "/test"
    src_path = PATH + "/src"

    pathlib.Path(test_path + "/pytest.ini").touch()
    pathlib.Path(test_path + "/conftest.py").touch()
    pathlib.Path(test_path + "/pytest.ini").touch()

    pages_dir = src_path + "/pages"
    os.mkdir(pages_dir)
    make_init_py(pages_dir)

    pathlib.Path(pages_dir + "/base.py").touch()
    make_base_page()

    models_dir = src_path + "/models"
    os.mkdir(models_dir)
    make_init_py(models_dir)
    pathlib.Path(models_dir + "/baseObj.py").touch()
    make_base_obj()

def make_ini():
    f = open(f"{PATH}/test/pytest.ini", 'w')

    to_write = "[pytest]\nlog_format = %(asctime)s %(levelname)s" \
               " %(message)s\nlog_date_format = %Y-%m-%d %H:%M:%S\nlog_cli = true" \
               "\nlog_cli_level = INFO"

    f.write(to_write)

    f.close()


def make_gitignore():
    f = open(f"{PATH}/.gitignore", 'w')
    to_write = """
*
!*.py
!*.gitignore
!*.txt
!*.md
    
    """
    f.write(to_write)
    f.close()


def make_conftest():
    f = open(f"{PATH}/test/conftest.py", 'w')
    to_write = """
import requests
import pytest
import logging
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


logging.basicConfig(level=logging.INFO)
my_logger = logging.getLogger()

chrome_options = Options()
chrome_options.add_experimental_option("detach", False)

# The URL can be changed
def pytest_addoption(parser):
    parser.addoption("--u", action="store", default="http://localhost/")
    parser.addoption("--s", action="store", default="http://localhost:7017/api")
    


@pytest.fixture(scope="session")
def get_url(pytestconfig):
    return pytestconfig.getoption("u")


@pytest.fixture(scope='session')
def get_swagger(pytestconfig):
    return pytestconfig.getoption("s")



@pytest.fixture
def setup(get_url):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get(get_url)
    yield driver

# You can add more fixtures here
"""
    f.write(to_write)
    f.close()

def make_requirements():
    f = open(f"{PATH}/requirements.txt", "w")
    to_write = """
selenium
pytest
requests
allure-pytest        
allure-python-commons 
webdriver-manager
"""
    f.write(to_write)
    f.close()


def main():
    make_directorys_and_files()
    make_gitignore()
    make_requirements()
    make_ini()
    make_conftest()

if __name__ == '__main__':
    main()
