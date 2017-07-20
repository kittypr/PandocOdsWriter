from odf.opendocument import load
from odf.style import Style
import sys

def_header1 = Style(name='header1', family='table-cell')
def_header2 = Style(name='header2', family='table-cell')
def_tablehead = Style(name='tablehead', family='table-cell')
def_tablebody = Style(name='tablebody', family='table-cell')
def_text = Style(name='text', family='table-cell')
st_dict = {'header1': def_header1,
           'header2': def_header2,
           'tablehead': def_tablehead,
           'tablebody': def_tablebody,
           'text': def_text
           }


def load_style(name):
    try:
        path = str(sys.argv[0])
        path = path.replace('odswritter.py','')
        path = path + 'styles.ods'
        source = load(path)
        try:
            style = source.getStyleByName(name)
            style.setAttribute(attr='family', value='table-cell')
        except AssertionError:
            style = None
    except FileNotFoundError:
        print('WARNING! There is no style file, create it and name "styles.ods"')
        style = None
    if style is None:
        try:
            style = st_dict[name]
        except KeyError:
            s = Style(name=name, family='table-cell')
            st_dict[name] = s
            style = st_dict[name]
    return style
