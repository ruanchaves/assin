
from google.cloud import translate_v2 as translate
import six
import os
import xml.etree.ElementTree as ET
import json 

# https://cloud.google.com/translate/docs/basic/setup-basic
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

dct = 'dictionary.json'

files = [
    "assin-ptbr-dev.xml",
    "assin-ptbr-test.xml",
    "assin-ptbr-train.xml",
    "assin-ptpt-dev.xml",
    "assin-ptpt-test.xml",
    "assin-ptpt-train.xml",
    "assin2-dev.xml",
    "assin2-train-only.xml",
    "assin2-blind-test.xml",
    "assin2-train.xml"
]

class Translator(object):

    def __init__(self, target):
        self.target = target
        self.translate_client = translate.Client()

    def translate(self, text):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        result = self.translate_client.translate(text, target_language=self.target)
        return {
            "original": result['input'],
            "translation": result['translatedText']
        }

def read(flist):
    for fname in flist:
        tree = ET.parse(fname)
        root = tree.getroot()
        for pair in root.iter('pair'):
            yield pair.find('t').text
            yield pair.find('h').text

t = Translator('en')
try:
    open(dct).close()
except:
    with open(dct, 'w+') as f:
        json.dump({}, f)
for item in read(files):
    with open(dct, 'r') as f:
        loaded_dct = json.load(f)
    try:
        loaded_dct[item]
    except:
        result = t.translate(item)
        print(result)
        loaded_dct[result['original']] = result['translation']
        with open(dct, 'w+') as f:
            json.dump(loaded_dct, f)
