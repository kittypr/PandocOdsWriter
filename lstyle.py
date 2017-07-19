from odf.opendocument import load

import sys

# def_header1 = Style(name='header1', family='table-cell')
# def_header2 =
# def_tablehead =
# def_tablebody =
# def_text


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
    return style
