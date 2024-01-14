import pandas as pd
import argparse
import shutil
import json
import os

def prepare_dataset(path_image_info):

    df = pd.read_csv(path_image_info, sep=';', index_col='index')

    num_cards = [100, 1000, 5000, -1]
    for nc in num_cards:
        if nc == -1:
            nc = len(df)
        tmp = df.sample(nc)
        dir_cn = os.path.join(
                'datasets',
                'card_name_{}'.format(nc)
            )
        if not os.path.exists(dir_cn):
            os.makedirs(dir_cn)
        dir_fc = os.path.join(
                'datasets',
                'full_card_{}'.format(nc)
            )
        if not os.path.exists(dir_fc):
            os.makedirs(dir_fc)


        arr_cn = ''
        arr_fc = ''

        for idx, series in tmp.iterrows():

            p = series['path_img']
            fn = p[4:]
            np = 'proc' + p[3:]

            t = series['card_txt_line'].replace('"', '')
            s = t.split(', {')[0].replace('"', '')
            txt_cn = 'magic the gathering card artwork, {}'.format(s)
            txt_fc = 'magic the gathering card artwork, {}'.format(t)
            print(fn)
            arr_cn += '{"file_name": "' + str(fn) +'", "text": "' + str(txt_cn) + '"}\n'
            arr_fc += '{"file_name": "' + str(fn) +'", "text": "' + str(txt_fc) + '"}\n'

            shutil.copy(
                np,
                os.path.join(dir_cn, fn)
            )
            shutil.copy(
                np,
                os.path.join(dir_fc, fn)
            )
    
        with open(os.path.join(dir_cn, 'metadata.jsonl'), 'w+') as fh:
            fh.write(arr_cn)
        with open(os.path.join(dir_fc, 'metadata.jsonl'), 'w+') as fh:
            fh.write(arr_fc)


if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(
        'Artwork retrival using scryfall API'
    )
    argument_parser.add_argument('-pi', '--path_image_info', type=str, default='raw_images/card_images_0_1000.csv', help='Path to csv file containing file paths and card info')
  
    args = argument_parser.parse_args()

    prepare_dataset(args.path_image_info)