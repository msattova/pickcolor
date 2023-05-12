import argparse
import re
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

'''
x軸: S[0-100]
y軸: V[0-100]
'''

def load_image(filepath: str, sample: int|None):
    img_array = np.array(Image.open(filepath))
    row, column, _ = img_array.shape
    # randがNoneでなければランダムな座標rand箇所から色を取得する
    if sample is None:
        colorset = set([tuple(img_array[i, j][:3])
                        for i in range(row) for j in range(column)])
    else:
        rng = np.random.default_rng()
        colorset = set([tuple(img_array[i, j][:3])
                        for i in rng.choice(row, size=sample, replace=False)
                        for j in rng.choice(column, size=sample, replace=False)])
    HSV_colorset = set([tuple([ np.round(i, decimals=2) for i in calc_HSV(c)])
                    for c in colorset])
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

def progress_bar(i, epoch):
    bar = '='*i + ('>' if i < epoch-1 else '=') + ' '*(epoch-i-1)
    print(f'\r[{bar}] {i+1}/{epoch}', end='')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='pickcolor',
                                     description='その画像で使われている色をSaturation-Value平面にプロットする。複数指定した場合はその全てを合わせて出力する')
    parser.add_argument('imgpaths',
                        nargs='+',
                        action='store',
                        type=Path)
    parser.add_argument('--sample', '-s', type=int,
                        nargs='?', default=0, const=100,
                        help='サンプルサイズを指定し、ランダムな座標n箇所から色を取得するようにします')
    parser.add_argument('--view', '-v', action='store_true',
                        help='処理終了時にグラフを表示する')
    parser.add_argument('--output', '-o', type=str, default='output.png',
                        help='出力画像のファイル名を指定')

    args = parser.parse_args()
    paths = args.imgpaths
    sample = args.sample if args.sample > 0 else None
    is_view = args.view
    output = args.output

    HSV_colorset = set()
    imagepaths = set()
    imagepaths |= set([filepath
                      for p in paths if Path.is_dir(p)
                      for filepath in p.glob('**/*')
                      if re.search(r'.*\.(png|jpe?g)', str(filepath))])
    imagepaths |= set([filepath for filepath in paths
                       if Path.is_file(filepath)
                       and re.search(r'.*\.(png|jpe?g)', str(filepath))])
    for i, p in enumerate(imagepaths) :
        progress_bar(i, len(imagepaths))
        HSV_colorset |= load_image(p, sample)

    # set型では順序は保証されないため、一旦tupleに変換して順序を確定させる
    HSV_colortuple = tuple(HSV_colorset)
    saturation_list = [ c[1] for c in HSV_colortuple ]
    value_list = [ c[2] for c in HSV_colortuple ]

    save(saturation_list, value_list, output)

    print('\nComplete!')
    if is_view:
        print('グラフを別ウインドウで表示します。')
        plt.show()


