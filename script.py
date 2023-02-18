import googletrans
from googletrans import Translator
from bs4 import BeautifulSoup
import os

def translate_html_tohindi(url):
    with open(url) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the elements on the page that contain text
    elements = soup.find_all(text=True)

    # Loop through each element and check if it can be translated
    translatable_text = []
    for element in elements:
        # Ignore certain types of elements that are unlikely to contain translatable text
        if element.parent.name in ['script', 'style', 'meta', '[document]']:
            continue
        # Ignore elements that are empty or only contain whitespace
        if not element.strip():
            continue
        # If the text is in a different language than the page language, it can be translated
        if element.parent.get('lang') != soup.html.get('lang'):
            translatable_text.append(element)

    translator = Translator()
    for text in translatable_text:
        try:
            translated_text = translator.translate(text, src='en', dest='hi').text
            text.replace_with(translated_text)
        except Exception as e:
            print(f"Error translating text: {text}. Exception: {e}")
            continue
    
    # Write the modified src
    with open(url, 'w') as f:
        f.write(str(soup))




directory = '/home/pdc-p180069/project'  # Replace this with the directory you want to iterate through
count=0
for root, dirs, files in os.walk(directory):
    for file in files:
        name=os.path.join(root, file)
        if "classCentral.html" in name:
            continue
            count+=1
        elif ".html" in name:
            translate_html_tohindi(name)
            count+=1
            print(count," :::: ",name)