from os import path, listdir, renames, chdir, remove, mkdir, chmod, rmdir
import shutil
from os.path import exists, dirname
from PIL import Image
import getpass

presentDir = dirname(__file__)
source_dir = r'C:\Users\{username}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'.format(
    username=getpass.getuser())
temp = path.join(presentDir, 'temp')
# destination_dir = path.join(presentDir, 'win10好图')
destination_dir = r'E:\win10好图'


def copyFile(source_dir, temp):
    for file in [fi for fi in listdir(source_dir)]:
        if path.getsize(path.join(source_dir, file)) > 190000:
            shutil.copy2(path.join(source_dir, file), path.join(temp, file))
    print('copy file form ms.assets successfully!')


def renameFile(suffix):
    chdir(temp)
    for file in [fi for fi in listdir(temp)]:
        renames(file, file + suffix)
    print('rename file to XXX%s successfully!' % suffix)


def judgeFile():
    # chdir(temp)
    for file in [fi for fi in listdir(temp)]:
        img = Image.open(file)
        # print(img.size, img.format, img.mode) #(1920, 1080) JPEG RGB
        img.close()
        if img.size != (1920, 1080):
            remove(file)

        # print(dir(img))
        # print(hasattr(img, '_getexif'))
        # '_Image__transformer', '__array_interface__', '__class__', '__copy__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_close_exclusive_fp_after_loading', '_copy', '_crop', '_dump', '_exclusive_fp', '_expand', '_getexif', '_getmp', '_new', '_open', '_repr_png_', 'alpha_composite', 'app', 'applist', 'bits', 'category', 'close', 'convert', 'copy', 'crop', 'decoderconfig', 'decodermaxblock', 'draft', 'effect_spread', 'filename', 'filter', 'format', 'format_description', 'fp', 'frombytes', 'fromstring', 'getbands', 'getbbox', 'getcolors', 'getdata', 'getextrema', 'getim', 'getpalette', 'getpixel', 'getprojection', 'height', 'histogram', 'huffman_ac', 'huffman_dc', 'icclist', 'im', 'info', 'layer', 'layers', 'load', 'load_djpeg', 'load_end', 'load_prepare', 'mode', 'offset', 'palette', 'paste', 'point', 'putalpha', 'putdata', 'putpalette', 'putpixel', 'pyaccess', 'quantization', 'quantize', 'readonly', 'remap_palette', 'resize', 'rotate', 'save', 'seek', 'show', 'size', 'split', 'tell', 'thumbnail', 'tile', 'tobitmap', 'tobytes', 'toqimage', 'toqpixmap', 'tostring', 'transform', 'transpose', 'verify', 'width'
    print('get pictures\' size and remove unfit pictures successfully!')


def moveFile(sour, dest):
    # chdir(temp)
    for file in [fi for fi in listdir(temp)]:
        shutil.copy2(path.join(sour, file), path.join(dest, file))
        remove(file)
    print('move pictures from temp dir to destination dir successfully!')


def main():
    if not exists(destination_dir):
        mkdir(destination_dir)
    if not exists(temp):
        mkdir(temp)
    copyFile(source_dir, temp)
    renameFile('.jpg')
    judgeFile()
    moveFile(temp, destination_dir)
    chdir(presentDir)
    rmdir(temp)


main()
