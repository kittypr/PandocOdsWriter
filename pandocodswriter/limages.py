from subprocess import Popen, PIPE
import sys

from odf.opendocument import load

img_dict = {}


def load_images(input_file, ods):
    """Load images from input file.

    Cause we work with pandoc's input, we will get different extensions of files. In purpose of not to
    extract images ourselves, we make pandoc create .odt file pandoc does all hard work),
    that we can easy to work with.

    Args:
        input_file - our input from start.
        ods - our ods document, we will insert images in it here.

    Returns:
        hr_list - list of hard references to images, that already inside our file.
        [] - empty list, if we faced with some issues (e.g.: we can't create temporary .odt file).

    """
    cur_dir = str(sys.argv[0])
    cur_dir = cur_dir.replace('odswriter.py', '')
    output_file = cur_dir + 'tmp.odt'
    command = 'pandoc ' + input_file + ' -o ' + output_file
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    res = proc.communicate()
    if res[0]:
        print('Images can not be loaded, Error:\n', res[0])
        return []

    odffile = load(output_file)
    for k in odffile.Pictures.keys():
        img_dict[k] = odffile.Pictures[k][1]

    # To save right order of images we should inverse img_dict we got, cause we load items from the end.
    # The order is very important, because it's only way we identify images
    # (our input and tmp.ods have different filenames).
    hr_list = [i for i in range(0, len(img_dict))]
    hr_index = len(img_dict) - 1
    for img_name in img_dict:
        hr_list[hr_index] = ods.addPicture(filename=img_name, content=img_dict[img_name])
        hr_index = hr_index - 1
    return hr_list


