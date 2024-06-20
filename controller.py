import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from model import Service, get_all_services
from __init__ import BASE_URL 
from sqlmodel import Session, select
import model

def get_web_data(url):
    # Fetches data using HTTP requests
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch data")


def parse_web_data(raw_data):
    # Parses the data into a Python-readable format
    return BeautifulSoup(raw_data, "html.parser")


def get_service_metadata(soup):
    # Extract metadata from services
    metadata = []

    # Find the parent div
    parent_div = soup.find("div", class_="modul-azlist", id="toplist")

    if not parent_div:
        raise Exception("Parent div not found")

    # Find all the li elements within the parent div
    li_elements = parent_div.find_all("li")

    # Extract the href attribute and the text from each a tag inside the li elements
    letter_links = [(li.find("a").text, li.find("a")["href"]) for li in li_elements]
    metadata = []

    for letter , link in letter_links:
        service = Service()
        # Extract metadata
        # 1. title
        service.title = letter
        if len(link.split("/")) < 2:
            continue
        else: 
            service.id = int(link.split("/")[-2])
        
            
        # 2. description
        service_url = urljoin(BASE_URL, link)
        service_data = get_web_data(service_url)
        service_soup = parse_web_data(service_data)
        description_text1 = service_soup.find("div", class_="block").text
        description_text2 = service_soup.find("ul", class_="list")
        
        # description_text2_1 = [li.text for li in description_text2.find("li")]

        if description_text1:
             description = description_text1
        else:
             description_text2_1 = [li.text for li in description_text2.find("li")]
             description = description_text2_1
        service.description = description

        # 3. is_digital
        is_digital = service_soup.find("h2", class_="title").text,
        if "Online-Abwicklung" in is_digital:
            is_digital = True
        else:
            is_digital = False
        service.is_digital = is_digital

        # 4.responsible_office
        Hinweise_zur_Zuständigkeit = service_soup.find_all("div", class_="block")
        found_responsibility = False

        for hinweis in Hinweise_zur_Zuständigkeit:
            h2_tag = hinweis.find("h2")
            if h2_tag is None:
                continue
            elif h2_tag.text.strip() == "Hinweise zur Zuständigkeit":
                p_tag = hinweis.find("p")
                if p_tag is not None:
                    service.responsible_office = p_tag.text.strip()
                    found_responsibility = True
                
            elif h2_tag.text.strip() == "Für Sie zuständig":
                strong_tag = hinweis.find("strong")
                if strong_tag is not None:
                        service.responsible_office = strong_tag.text.strip()
                        found_responsibility = True
            
        if not found_responsibility:
            service.responsible_office = "Es gibt keine Zuständigkeit für alle Hinweise"


        
        # 5. form_link
        link_formulare = service_soup.find_all("div", class_="block")
        form_links = {}
        for link in link_formulare:
            if link.find("h2") is None:
                continue
            elif link.find("h2").text.strip() == "Formulare":
                a_tags = link.find_all("a")
                for a in a_tags:
                    form_links[a["title"]] = a["href"]
        import json
        json.dumps(form_links)
        form_links_json = json.dumps(form_links)           
        service.form_link = form_links_json

        metadata.append(service)

    return metadata

def get_service():
    raw_data = get_web_data(BASE_URL)
    soup = parse_web_data(raw_data)
    services: list[Service] = get_service_metadata(soup)

    for service in services:
        print(service)  
        model.create(service)  

def get_service_from_db():
    return get_all_services()
