__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'


import os
import justext
import re


# This function cleans up the pages using justext. A new directory
# with clean pages is created. The link is saved in the first line
# of each file.
def clean_text(dirty_path, clean_path):
    link_reg = re.compile('(.+?)\n')
    if not os.path.exists(clean_path):
        os.makedirs(clean_path)
    for root, dirs, files in os.walk(dirty_path):
        for dir in dirs:
            if not os.path.exists(os.path.join(clean_path, dir)):
                os.makedirs(os.path.join(clean_path, dir))
        for name in files:
            if name.endswith('.txt'):
                with open(os.path.join(root, name), 'r',
                          encoding='utf-8') as f:
                    text = f.read()
                    link = link_reg.search(text).group(1)
                    try:
                        paragraphs = justext.\
                            justext(text, justext.get_stoplist('Russian'))
                        new_path = os.path.join(root, name).replace(dirty_path,
                                                                    clean_path)
                        with open(new_path, 'w', encoding='utf-8') as f1:
                                f1.write(link + '\n')
                                for paragraph in paragraphs:
                                    if not paragraph.is_boilerplate:
                                        f1.write(paragraph.text + '\n')
                    except SyntaxError:
                        #print('error: ' + name)
                        pass
