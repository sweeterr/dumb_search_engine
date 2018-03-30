__authors__ = 'Marija Aleksejeva, Daniil Kolomeitsev, Jevgenij Mozajev,' \
              ' Nina Mustafina, Svetlana Pavlova'


import os
import re
import platform


re_lemma = re.compile('{(.*?)=')
re_clr = re.compile('[{?=]')


# This function parses text from input file using mystem and
# writes the parsed text to output file. Mystem should be in
# the same directory as the main module.
def mystem_parsing(input_path, output_path,
                   options='-d -e utf-8 -i --eng-gr'):
    if platform.system() == 'Windows':
        x_file = 'mystem.exe'
    else:
        x_file = 'mystem'
    mystem_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            x_file)
    os.system(mystem_dir + ' '
              + options + ' '
              + input_path + ' '
              + output_path)


# This function takes the path to a directory of clean text files and
# initiates mystem lemmatization and clean up for each file. The
# resulting files are saved to a separate _lemmatized folder.
def lemmatize_text(path):
    for i in os.walk(path):
        self_path = i[0]
        files = i[2]
        output_path = self_path.replace(path, path + '_lemmatized')
        try:
            os.makedirs(output_path)
        except:
            pass
        for j in files:
            mystem_parsing(os.path.join(self_path, j),
                           os.path.join(output_path, j))
            clear_file(os.path.join(output_path, j))


# This function cleans up lemmatized files,
# removing everything except the lemmas.
def clear_file(path, one_on_string=True, is_return=False):
    o_file = open(path, encoding = 'utf-8')
    tagged_text = o_file.read()
    result = re_lemma.findall(tagged_text[1:])
    if one_on_string:
        splitter = '\n'
    else:
        splitter = ' '
    lemmatized_text = splitter.join(result)
    lemmatized_text = lemmatized_text.replace('?', '')
    o_file.close()
    o_file = open(path, 'w', encoding = 'utf-8')
    o_file.write(lemmatized_text)
    o_file.close()
    if is_return:
        return lemmatized_text


# This function lemmatizes search query.
def lemmatize_req(request):
    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'reqestflag.txt'), 'w', encoding = 'utf-8')
    file.write(request)
    file.close()
    mystem_parsing(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reqestflag.txt'),
                   os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reqestflag_lemmatized.txt'))
    text = clear_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reqestflag_lemmatized.txt'),
                      is_return = True)
    return text
