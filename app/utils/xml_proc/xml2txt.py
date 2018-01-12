# import modules & set up logging
from gensim.models import word2vec
import xml.etree.ElementTree as ET
import logging
f = open('subject.txt','w')

for event,elem in ET.iterparse("small_sample.xml", events=(['end'])):
    # if elem.tag in ['subject', 'content', 'answer_item']:
    if elem.tag in ['subject']:
        f.write(elem.text.replace('<br />','')+'\n')
        elem.clear()

f.flush()
f.close()
