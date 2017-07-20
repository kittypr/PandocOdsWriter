import json
import argparse
import sys
import io

from lstyle import load_style
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TableColumnProperties, TableRowProperties, TextProperties
from odf.table import Table, TableRow, TableCell, TableColumn
from odf.text import P

# use command - pandoc yourInputFile.yourExetention -t json | python ODSwriter.py yourOutputFile.ods
# DO NOT specify output file in last pandoc's command, because pandoc will rewrite it and 'kill'

# Header 0 - simple text, you can add another headers, of change names of this. If in file more, than two levels
# of headers next name will generate as name = "header" + str(level)
# If you'll change this names, for correct work, change them in "styles1.py" for default styles1
header = ['header0', 'header1', 'header2']

# Table headers and content
table_header = 'tablehead'
table_content = 'tablebody'
simple_text = 'text'
# Pandoc uses UTF-8 for both input and output; so must its filters.  This is
# handled differently depending on the python version.
if sys.version_info > (3,):
    # Py3 strings are unicode: https://docs.python.org/3.5/howto/unicode.html.
    # Character encoding/decoding is performed automatically at stream
    # interfaces: https://stackoverflow.com/questions/16549332/.
    # Set it to UTF-8 for all streams.
    STDIN = io.TextIOWrapper(sys.stdin.buffer, 'utf-8', 'strict')
    STDOUT = io.TextIOWrapper(sys.stdout.buffer, 'utf-8', 'strict')
    STDERR = io.TextIOWrapper(sys.stderr.buffer, 'utf-8', 'strict')
else:
    # Py2 strings are ASCII bytes.  Encoding/decoding is handled separately.
    # See: https://docs.python.org/2/howto/unicode.html.
    STDIN = sys.stdin
    STDOUT = sys.stdout
    STDERR = sys.stdout

# Read the command-line arguments
parser = argparse.ArgumentParser(description='Pandoc ODS writer. This is Pandoc filter, but there is no opportunity '
                                             'write .ods files easier way. So, use "out.ods" '
                                             'option to write .ods files with this filter')
parser.add_argument('output', help='Output file. Use .ods filename extension.', action='store')
parser.add_argument('--pandocversion', help='The Pandoc version.')
args = parser.parse_args()

# if you want to change width by default (10 cm), change it in "main" , count, how much symbols in a string look
# correctly for your length for auto-height, and change this tuple as you need.
# There are 7 numbers - count of symbols for different font size - 10pt, 11pt (header lvl 6), ... , 16pt (header lvl 1)

# I need this global variables, because there are two recursive functions call each other, so it would be very hard work
# without global "string_to_write"
# Moreover recursive functions are easier to read

ods = OpenDocumentSpreadsheet()
table = Table()
string_to_write = ''
header_level = 0
bullet = 0
ordered = 0
saved_styles = {}
PTINTENCM = 284

def write_sheet():
    widthwide = Style(name="Wwide", family="table-column")
    widthwide.addElement(TableColumnProperties(columnwidth="10cm"))
    ods.automaticstyles.addElement(widthwide)
    table.addElement(TableColumn(stylename='Wwide'))
    ods.spreadsheet.addElement(table)

def count_height(row, cell):
    style_name = cell.getAttribute('stylename')
    try:
        style = saved_styles[style_name]
        text_prop = style.getElementsByType(TextProperties)
        try:
            text_prop = text_prop[0]
            font_size = str(text_prop.getAttribute('fontsize'))
            font_size = font_size.replace('pt', '')
            font_size = int(font_size)
        except IndexError:
            font_size = 10
    except KeyError:
        font_size = 10
    symbols_in_string = PTINTENCM // font_size + 1
    height = font_size*(len(string_to_write) // symbols_in_string + 1) + 4
    height = str(height) + 'pt'
    new_name = 'heightsuit' + height
    height_suit = Style(name=new_name, family='table-row')
    height_suit.addElement(TableRowProperties(rowheight=height))
    ods.automaticstyles.addElement(height_suit)
    row.setAttribute(attr='stylename', value=new_name)


def add_style(cell, name):
    global table
    style = load_style(name)
    if style is not None:
        global ods
        global saved_styles
        saved_styles[name] = style
        ods.styles.addElement(style)
        cell.setAttribute(attr='stylename', value=name)


def write_text():
    """Write to output file non-table elements

    This function is called every tame, we collect whole paragraph or block of elements in "string_to+write"
    We write every block or paragraph in it's own cell in the first column of output file.
    After writing we shift down "current_row" and clean "string_to_write" in order to collect next elements.
    """
    global string_to_write
    global header_level
    global ordered
    global bullet
    global table
    row = TableRow()
    cell = TableCell()
    if header_level != 0 and header_level > 0:
        if header_level > (len(header) - 1):
            for i in range(len(header), header_level+1):
                header.append('header' + str(i))
        add_style(cell, header[header_level])
        if header_level == 1:
            if table.hasChildNodes():
                write_sheet()
            table = Table(name=string_to_write)
    else:
        add_style(cell, simple_text)
    if bullet:
        string_to_write = '- ' + string_to_write
    if ordered > 0:
        string_to_write = str(ordered) + ') ' + string_to_write
        ordered = ordered + 1
    content = P(text=string_to_write)
    cell.addElement(content)
    count_height(row, cell)
    row.addElement(cell)
    table.addElement(row)
    string_to_write = ''


def write_bullet(bull_list, table_indicate):
    global bullet
    bullet = 1
    list_parse(bull_list['c'],  table_indicate)
    bullet = 0


def write_ord(ord_list,  table_indicate):
    global ordered
    ordered = 1
    list_parse(ord_list['c'],  table_indicate)
    ordered = 0


def write_code(code):
    """Write to output file code elements

    Since, element with title "Code" or "CodeBlock" has special structure of 'c'(Content) field, that looks like:
    [[0], "code"]
    where:
    [0] - list of attributes: identifier, classes, key-value pairs
    "code" - string with code
    we should parse it especially.
    """
    global string_to_write
    string_to_write = string_to_write + code['c'][1]


def write_link(link):
    global string_to_write
    string_to_write = string_to_write + link['c'][2][0]


def write_math(math):
    """Write to output file code elements

    Since, element with title "Math" has special structure of 'c'(Content) field, that looks like:
    [{0}, "math"]
    where:
    {0} - dictionary contains type of math
    "math" - string with math
    we should parse it especially.
    TeX Math format.
    """
    global string_to_write
    string_to_write = string_to_write + math['c'][1]


def write_raw(raw):
    """Write to output file raw elements

    Since, element with title "RawBlock" or "RawInline" has special structure of 'c'(Content) field, that looks like:
    [format, "raw text"]
    we should parse it especially.
    """
    global string_to_write
    string_to_write = string_to_write + raw['c'][1]


def write_special_block(block,  table_indicate):
    """Write special blocks with attributes

    Since, element with title "Div" or "Span" or "Header" has special structure of 'c'(Content) field, that looks like:
    [[0], [1]]
    where:
    [0] - list of attributes: identifier, classes, key-value pairs
    [1] - list with objects (list of dictionaries) - content
    *with "Headers" title - [level, [0], [1]] - level - int, [0], [1] - the same as above
    we should parse it especially.
    """
    global string_to_write
    global header_level
    content = 1
    if block['t'] == 'Header':
        header_level = block['c'][0]
        content = 2
    if (not table_indicate) and string_to_write:
        write_text()
    list_parse(block['c'][content], True)
    if not table_indicate:
        write_text()
    header_level = 0


def write_table(tab):
    """Write to output file table elements

    This function is called every time, we meet "Table" dictionary's title.
    Firstly, if we have some information in "string_to_write" we record it, because we'll use this
    variable to collect information from table's cells.
    After that we found right edge if our table:
        I don't kow why, but We cant write righter then we already have wrote in one row.
    Table in pandoc's json has following structure:
    dict: { t: "Table"
            c: [ [0] [1] [2] [3] [4] ]
          }
    Where:
    [0] - caption
    [1] - is list of aligns by columns, looks like: [ { t: "AlignDefault" }, ... ]
    [2] - widths of columns
    [3] - is list of table's headers (top cell of every column), can be empty
    [4] - list of rows, and row is list of cells
    Since every cell's structure is the same as text's one, we just parse them as list and write one by one
    """
    global table
    global string_to_write
    if string_to_write:
        write_text()
    global current_row
    # Add empty line before table
    row = TableRow()
    table.addElement(row)
    row = TableRow()
    headers = tab['c'][3]
    if headers:
        # Add empty first cell in row (first column in document - text column).
        cell = TableCell()
        row.addElement(cell)
        for col in headers:
            cell = TableCell()
            list_parse(col, table_indicate=True)
            content = P(text=string_to_write)
            cell.addElement(content)
            add_style(cell, table_header)
            string_to_write = ''
            row.addElement(cell)
        table.addElement(row)
    t_content = tab['c'][4]
    for line in t_content:
        row = TableRow()
        # Add empty first cell in row (first column in document - text column).
        cell = TableCell()
        row.addElement(cell)
        for col in line:
            cell = TableCell()
            list_parse(col, table_indicate=True)
            content = P(text=string_to_write)
            cell.addElement(content)
            add_style(cell, table_content)
            string_to_write = ''
            row.addElement(cell)
        table.addElement(row)
    row = TableRow()
    # Add empty line after table
    table.addElement(row)


# This two functions - "dict_parse" and "list_parse", has purpose to extract readable information
# from json object.
# Since, pandoc's json object in it's field 'blocks' has list with dictionaries,
# that represent another objects and this dictionaries has the following structure:
# { t: "*Name of objects type, for example 'Str'"
#   c: "*Content of object, in this case any string*" }
# (sometimes there can be no 'c'-field (f.e. "Space" - object)
# So, 'c'-field - content, can be a list of dictionaries, or a string, or a list of lists,
# so we should parse list again and etc.
# That's why we have there two functions - for parsing lists and for parsing dictionaries - that should call each other

def dict_parse(dictionary,  table_indicate=False):
    """Parse dictionaries"""

    global string_to_write
    if dictionary['t'] == 'Table':
        write_table(dictionary)
    elif dictionary['t'] == 'CodeBlock' or dictionary['t'] == 'Code':
        write_code(dictionary)
    elif dictionary['t'] == 'Div' or dictionary['t'] == 'Span' or dictionary['t'] == 'Header':
        write_special_block(dictionary, table_indicate)
    elif dictionary['t'] == 'Math':
        write_math(dictionary)
    elif dictionary['t'] == 'Link':
        write_link(dictionary)
    elif dictionary['t'] == 'BulletList':
        write_bullet(dictionary, table_indicate)
    elif dictionary['t'] == 'OrderedList':
        write_ord(dictionary, table_indicate)
    elif 'c' in dictionary:
        if type(dictionary['c']) == str:
            string_to_write = string_to_write + dictionary['c']
        if type(dictionary['c']) == list:
            list_parse(dictionary['c'], table_indicate)
    else:
        if dictionary['t'] == 'Space':
            string_to_write = string_to_write + ' '
        elif dictionary['t'] == 'SoftBreak':
            string_to_write = string_to_write + '\n'
        elif dictionary['t'] == 'LineBreak':
            string_to_write = string_to_write + '\n\n'
            if not table_indicate:
                write_text()
        else:
            string_to_write = string_to_write
    if dictionary['t'] == 'Para':
        string_to_write = string_to_write + '\n'
        if not table_indicate:
            write_text()


def list_parse(content_list, table_indicate=False):
    """Parse lists"""
    for item in content_list:
        if type(item) == dict:
            dict_parse(item, table_indicate)
        if type(item) == list:
            list_parse(item, table_indicate)
        else:
            continue


def main():
    """Main function

    Get JSON object from pandoc, parse it, save result
    """
    global table
    output = args.output
    # Read json object and decode it to python dictionary.
    # It has representation like: { pandoc-version: ...
    #                               meta: ...
    #                               blocks: .......}
    # in blocks we have all file-content, that's why we will parse it
    doc = json.loads(STDIN.read())
    if type(doc) == dict:
        list_parse(doc['blocks'])
    else:
        list_parse(doc[1])
    write_sheet()
    try:
        ods.save(output)
    except PermissionError as err:
        print("No access to ", output)
        print(err.strerror)


if __name__ == '__main__':
    main()
