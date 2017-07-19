from odf.opendocument import load


def load_style(name):
    try:
        source = load('D:\ODSprodject\ODS3\styles.ods')
        try:
            style = source.getStyleByName(name)
            style.setAttribute(attr='family', value='table-cell')
        except AssertionError:
            style = None
    except FileNotFoundError as err:
        print('WARNING! There is no style file, create it and name "styles.ods"')
    return style
