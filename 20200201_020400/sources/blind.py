import xml.etree.ElementTree as ET

def write_blind(fnames):
    for item in fnames:
        tree = ET.parse(item['source'])
        root = tree.getroot()
        for pair in root.iter('pair'):
            pair.set('similarity', '-1.0')
            pair.set('entailment', 'Unknown')
        tree.write(item['target'])

if __name__ == '__main__':
    fnames = [
        {
        "source": "assin-ptpt-test.xml",
        "target": "assin-ptpt-blind-test.xml"
        },
        {
        "source": "assin-ptbr-test.xml",
        "target": "assin-ptbr-blind-test.xml"
        },
        {
        "source": "assin2-test.xml",
        "target": "assin2-blind-test.xml"
        }
    ]
    write_blind(fnames)