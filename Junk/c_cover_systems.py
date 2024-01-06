
from fulltest import Store, Product
from bs4 import BeautifulSoup   
import requests
import json
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from project import Session
import time


cover_systems = Store("covers",
                            "coversystems",
                            "https://coversystems.co.nz/collections",
                            True,
                            {"marine-covers": 2, "bimini-tops": 1, "t-tops": 1, "rocket-launchers": 1, "rv-caravan-covers":1})




