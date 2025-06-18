import pathlib
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
from html.parser import HTMLParser

TABLE_TAGS = ['table', 'tbody', 'tr', 'td']

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.table_context = []
        self.write_table = False
        self.table_buffer = ''
        self.tables = []

    def handle_starttag(self, tag, attrs):
        if (tag in TABLE_TAGS):
            self.table_context.append(tag)
            if tag == 'tbody':
                self.tables.append([])
            elif tag == 'tr':
                self.tables[-1].append([])
            elif tag == 'td':
                self.write_table = True


    def handle_endtag(self, tag):
        if (tag in TABLE_TAGS):
            if self.table_context[-1] == tag:
                self.table_context.pop()
                print(self.table_context)
            else:
                raise RuntimeError('table-related uh oh')
            if tag == 'td':
                self.write_table = False
                self.tables[-1][-1].append(self.table_buffer)
                self.table_buffer = ''

    def handle_data(self, data):
        if self.write_table:
            self.table_buffer += data


# https://docs.python.org/3/library/xml.etree.elementtree.html
# tree = ET.parse('country_data.xml')
# root = tree.getroot()
# root = ET.fromstring(country_data_as_string)

# https://docs.python.org/3/library/xml.dom.minidom.html
# dom1 = parse('c:\\temp\\mydata.xml')  # parse an XML file by name
# dom3 = parseString('<myxml>Some data<empty/> some more data</myxml>')

# ElementTree
# xml.dom.minidom

file_name_rel = '~/websites/exrx-skeleton/exrx.net/WeightExercises/Brachioradialis/BBReverseCurl.html'
test_file = pathlib.Path(file_name_rel).expanduser()

with open(test_file, encoding='utf-8') as f:
    file_contents = f.read()

parser = MyParser()
parser.feed(file_contents)

print(parser.tables)


