import sys

from odf.opendocument import load
from odf.style import Style, TextProperties
import odf.style

# Build-in styles, used if there is no 'styles.ods'
default_header1 = Style(name='header1', family='table-cell')
default_header2 = Style(name='header2', family='table-cell')
default_tablehead = Style(name='tablehead', family='table-cell')
default_tablebody = Style(name='tablebody', family='table-cell')
default_text = Style(name='text', family='table-cell')
st_dict = {'header1': default_header1,
           'header2': default_header2,
           'tablehead': default_tablehead,
           'tablebody': default_tablebody,
           'text': default_text
           }


def bold():
    return TextProperties(fontweight='bold')


def italic():
    return TextProperties(fontstyle='italic')


def line_through():
    return TextProperties(textlinethroughstyle='solid', textlinethroughtype='single')


def load_style(name, file):
    """Load styles from file.

    This function loads style from file using stylename and filename. If user set reference to style file,
    this function will try to load style from it. If exception happened(no access, no such file) or user
    didn't set reference, this function will try to load styles from default style file ('styles.ods' from
    script directory). If exception happened(no access, no such file), this function will use build-in
    styles (just create all styles without any formatting).

    Args:
        name - style name
        file - file with styles definition

    Returns:
        style - loaded style

    """
    global st_dict

    styles_source = str(sys.argv[0])
    styles_source = styles_source.replace('odswriter.py', '')
    styles_source = styles_source + 'styles.ods'

    try:
        source = load(file)
        try:
            style = source.getStyleByName(name)
            style.setAttribute(attr='family', value='table-cell')
            st_dict[name] = style
        except AssertionError:
            style = None

    except FileNotFoundError:
        if file == styles_source:
            print('WARNING: There is no default style file, create it in script directory and name "styles.ods".\n'
                  'Build-in style will be used.')
            style = None
        else:
            print('WARNING: You entered invalid path to custom styles file, check it.\n'
                  'Default style will be used.')
            style = load_style(name, styles_source)

    except PermissionError as err:
        print(err.strerror)
        if file == styles_source:
            print('WARNING: There is no access to default style file. Check default style file settings.\n'
                  'Build-in style will be used.')
            style = None
        else:
            print('WARNING: There is no access to your style file. Check setings of your style file.\n'
                  'Default style will be used.')
            style = load_style(name, styles_source)

    if style is None:
        try:
            style = st_dict[name]
        except KeyError:
            s = Style(name=name, family='table-cell')
            st_dict[name] = s
            style = st_dict[name]

    return style


def add_fmt(style, key):
    """Creates new style with formatting.

    This function copies source style and adds necessary formatting.

    Args:
        style - source style
        key - formatting

    Returns:
        new_style - new style with formatting

    """
    global st_dict
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
        if key == 'Strong':
            new_element = bold()
        if key == 'Emph':
            new_element = italic()
        if key == 'Strikeout':
            new_element = line_through()
        new_style.addElement(new_element)
        st_dict[new_name] = new_style
    return new_style
