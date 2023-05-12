import argparse
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

'''
x軸: S[0-100]
y軸: V[0-100]
'''

def load_image(filepath: str):
    img_array = np.array(Image.open(filepath))
    row, column, _ = img_array.shape
    #print(f'shape: {img_array.shape}')
    colorset = set([tuple(img_array[i, j][:3])
                  for i in range(row) for j in range(column)])
    #print(colorset)
    HSV_colorset = [ tuple([ np.round(i, decimals=2) for i in calc_HSV(c)])
                    for c in colorset]
    return HSV_colorset

def calc_HSV(rgb):
    tmp = tuple( float(i/255) for i in rgb)
    x_max = max(tmp)
    x_min = min(tmp)
    v = x_max
    c = x_max - x_min
    s = 0 if v == 0 else c/v
    h = 0  # hは計算せずに0で決めうち
    return (h, s*100, v*100)

def save(saturation, value, output):
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    ax.set_xlabel('Saturation')
    ax.set_ylabel('Value')
    ax.scatter(saturation, value,
               alpha=0.4, s=[3])
    plt.savefig(output)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='pickcolor',
                                     description='その画像で使われている色をSaturation-Value平面にプロットする。複数指定した場合はその全てを合わせて出力する')
    parser.add_argument('imgpaths',
                        nargs='+',
                        action='store',
                        type=Path)
    args = parser.parse_args()
    paths = args.imgpaths

    output = 'output_.png'

    saturation_list = []
    value_list = []
    for p in paths:
        # ディレクトリの場合
        if Path.is_dir(p):
            tmp = tuple([filepath
                   for filepath in p.glob('**/*.png')])
            print(tmp)
            for p in tmp:
                HSV_colorset = load_image(p)
                s = [c[1] for c in HSV_colorset]
                v = [c[2] for c in HSV_colorset]
                saturation_list.extend(s)
                value_list.extend(v)
        #ファイルの場合
        else:
            HSV_colorset = load_image(p)
            s = [c[1] for c in HSV_colorset]
            v = [c[2] for c in HSV_colorset]
            saturation_list.extend(s)
            value_list.extend(v)

    save(saturation_list, value_list, output)
    plt.show()


