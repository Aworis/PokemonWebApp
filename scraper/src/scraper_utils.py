import requests
import xml.etree.ElementTree as ET
import re


def fetch_sitemap_xml(url: str) -> ET.Element:
    response = requests.get(url)
    response.raise_for_status()
    return ET.fromstring(response.content)

def extract_matching_urls(xml_root: ET.Element, pattern: str) -> list:
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    compiled_pattern = re.compile(pattern)
    urls = [elem.text for elem in xml_root.findall(f".//{namespace}loc")]
    return [url for url in urls if compiled_pattern.search(url)]
