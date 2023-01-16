import pathlib
import os

PATH = str(pathlib.Path(__file__).parent.resolve())


def make_directorys_and_files():
    dirs = ["/src", "/test", "/API"]
    for itm in dirs:
        path_to = PATH + itm
        os.mkdir(path_to)

    test_path = PATH + "/test"

    pathlib.Path(test_path + "/pytest.ini").touch()
    pathlib.Path(test_path + "/conftest.py").touch()
    pathlib.Path(test_path + "/pytest.ini").touch()






def make_ini():
    f = open("test/pytest.ini", 'w')

    to_write = "[pytest]\nlog_format = %(asctime)s %(levelname)s" \
               " %(message)s\nlog_date_format = %Y-%m-%d %H:%M:%S\nlog_cli = true" \
               "\nlog_cli_level = INFO"

    f.write(to_write)

    f.close()


def make_gitignore():
    f = open(".gitignore", 'w')
    to_write = "*\n!.py"
    f.write(to_write)
    f.close()


def make_conftest():

    f = open("test/conftest.py", 'w')
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
    f = open("requirements.txt", "w")
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

main()
