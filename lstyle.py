from odf.opendocument import load
from odf.style import Style, TextProperties
import odf.style
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

bold = TextProperties(fontweight='bold')
italic = TextProperties(fontstyle='italic')
line_through = TextProperties(textlinethroughstyle='solid', textlinethroughtype='single')


fmt_dict = {'Strong': bold,
            'Emph': italic,
            'Strikeout': line_through}


def load_style(name):
    global st_dict
    try:
        path = str(sys.argv[0])
        path = path.replace('odswritter.py','')
        path = path + 'styles.ods'
        source = load(path)
        try:
            style = source.getStyleByName(name)
            style.setAttribute(attr='family', value='table-cell')
            st_dict[name] = style
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


def add_fmt(style, key):
    global st_dict
    print(style.getAttribute('name'))
    new_name = style.getAttribute('name') + key
    try:
        new_style = st_dict[new_name]
    except KeyError:
        new_style = Style(name=new_name, family='table-cell')
        for child in style.childNodes:
            kind = child.qname[1]
            if kind == 'text-properties':
                copy_child = odf.style.TextProperties()
            elif kind == 'paragraph-properties':
                copy_child = odf.style.ParagraphProperties()
            elif kind == 'section-properties':
                copy_child = odf.style.SectionProperties()
            elif kind == 'table-cell-properties':
                copy_child = odf.style.TableCellProperties()
            elif kind == 'table-row-properties':
                copy_child = odf.style.TableRowProperties()
            elif kind == 'table-column-properties':
                copy_child = odf.style.TableColumnProperties()
            elif kind == 'table-properties':
                copy_child = odf.style.TableProperties()
            elif kind == 'drawing-page-properties':
                copy_child = odf.style.DrawingPageProperties()
            elif kind == 'graphic-properties':
                copy_child = odf.style.GraphicProperties()
            elif kind == 'chart-properties':
                copy_child = odf.style.ChartProperties()
            elif kind == 'ruby-properties':
                copy_child = odf.style.RubyProperties()
            else:
                continue
            for doc, attr in child.attributes:
                attr = attr.replace('-', '')
                try:
                    copy_child.setAttribute(attr=attr, value=child.getAttribute(attr))
                except ValueError:
                    continue
            new_style.addElement(copy_child)
            new_style.addElement(fmt_dict[key])
        st_dict[new_name] = new_style
    return new_style
