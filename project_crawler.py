__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'


# This module creates a collection of links and respective page files
# from source link using breadth-first algorithm with adjustable depth.


from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os


# This function prints a set of links to file.
def links_to_file(link_list, path):
    with open(path, 'w', encoding='utf-8') as f:
        for link in link_list:
            f.write(link + '\n')


# This function prints pages to files. The link to the page is in
# the first row.
def page_to_file(file_name, dir_name, path, link, text):
    if not os.path.exists(os.path.join(path, dir_name)):
        os.makedirs(os.path.join(path, dir_name))
    with open(os.path.join(path, dir_name, str(file_name) + '.txt'),
              'w', encoding='utf-8') as f:
        new_text = (link + '\n' + text)
        f.write(new_text)


# This function creates a set of links with distance = depth from
# the source link. For each link, it initializes a save of the page
# code to a file.
def crawler(current_level, depth):
    file_counter = 0
    dir_counter = 0
    files_in_dir = 0
    link_list = set()
    while depth > 0:
        next_level = []
        for link in current_level:
            page = requests.get(link, allow_redirects=False)
            text = page.text

            page_to_file(str(file_counter), str(dir_counter),
                         'collection_pages', link, text)
            files_in_dir += 1
            file_counter += 1
            if files_in_dir == 100:
                dir_counter += 1
                files_in_dir = 0
            soup = BeautifulSoup(text, 'html.parser')
            for child_link in soup.find_all('a'):
                new_link = urljoin(link, child_link.get('href'))
                if not new_link.startswith('https://'):
                    if not new_link in link_list:
                        link_list.add(new_link)
                        next_level.append(new_link)
            if file_counter == 500:
                break
        current_level = next_level
        depth -= 1
    return link_list