from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import argparse
import am

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')  # 输入文件
    parser.add_argument('-o', '--output')  # 输出文件
    parser.add_argument('--width', type=int, default=40)  # 输出字符画宽
    parser.add_argument('--height', type=int, default=40)  # 输出字符画高

    # 获取参数
    return parser.parse_args()


def command_line_runner():
    args = get_args()
    IMG = args.file
    WIDTH = args.width
    HEIGHT = args.height
    OUTPUT = args.output

    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    # 亮度增强
    brightness = ImageEnhance.Brightness(im)
    im = brightness.enhance(1.0)
    # 获取图片尖锐化对象
    sharpness = ImageEnhance.Sharpness(im)
    im = sharpness.enhance(4.0)
    # 增加对比度
    contrast = ImageEnhance.Contrast(im)
    im = contrast.enhance(1.0)
    # im = im.filter(ImageFilter.FIND_EDGES)
    # im = im.filter(ImageFilter.SHARPEN)
    # im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # im = im.filter(ImageFilter.CONTOUR)
    # im = im.filter(ImageFilter.DETAIL)

    im.save('E://temp/t.png')

    txt = ''

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    print(txt)
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open('E://temp/ascii.txt', 'w') as f:
            f.write(txt)


def other():
    args = get_args()
    IMG = args.file
    WIDTH = args.width
    HEIGHT = args.height
    OUTPUT = args.output

    im = Image.open(IMG).convert('L')
    print(vars(im))


if __name__ == '__main__':
    command_line_runner()
