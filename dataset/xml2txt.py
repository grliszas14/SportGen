from lxml import etree
from itertools import chain

with open("../dataset/HMN.xml") as file:
    data = file.read()
    root = etree.fromstring(data)
    words = []
    for child in root.getchildren():
        if child.tag == 'stext':
            for utag in child.getchildren():
                for sentence in utag.getchildren():
                    if sentence.tag == 's':
                        for word in sentence.getchildren():
                            if word.tag == 'w':
                                words.append(f"{word.text.strip()} ")
    contents = ''.join(chain.from_iterable(words))
    with open("../dataset/HMN.txt", 'w+') as file_txt:
        file_txt.write(contents)


