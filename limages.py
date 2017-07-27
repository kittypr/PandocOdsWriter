import sys
from subprocess import Popen, PIPE
from odf.opendocument import load

img_dict = {}


def load_images(input_file, ods):
    cur_dir = str(sys.argv[0])
    cur_dir = cur_dir.replace('odswritter.py', '')
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

    hr_list = [i for i in range(0, len(img_dict))]
    hr_index = len(img_dict) - 1
    for img_name in img_dict:
        hr_list[hr_index] = ods.addPicture(filename=img_name, content=img_dict[img_name])
        hr_index = hr_index - 1
    return hr_list


