import requests
import argparse
import wget
import os
import re
import pandas as pd
from time import sleep


base_url = 'https://api.scryfall.com'

def run(args):

    with open(os.path.join('data', 'card_info', 'name_manacost_type_text_pt.txt'), 'r') as fh:
        arr_cards = fh.readlines()

    arr_dict_card_info = []
    for idx, card_txt_line in enumerate(arr_cards):
        if idx <= args.start_idx:
            continue
        # Process card text to retrieve card name
        card_txt_line = card_txt_line.replace('\n', '')
        try:
            s = card_txt_line.split(', {')
            name = s[0]
            name = re.sub('[^\w\s]', '', name)
            name = re.sub('\s', '+', name)
        except Exception as e:
            print('No name found for card text line: {} // error: {}'.format(
                card_txt_line,
                e
            ))
            continue
        
        # Prepare API url
        print('Card name: {}'.format(name))
        url_card_named_fuzzy = base_url + '/cards/named?fuzzy={}'.format(
            name
        )
        try: 
            r = requests.get(
                url_card_named_fuzzy
            )
        except Exception as e:
            print('Failed getting scryfall card info: {} // error: {}'.format(
                name,
                e
            ))
            continue

        # Download cropped art
        try: 
            url_art_crop = r.json()['image_uris']['art_crop']
            path_img = wget.download(url_art_crop, out=args.path_output)
            arr_dict_card_info.append({
                'card_txt_line': card_txt_line,
                'path_img': path_img
            })
        except Exception as e:
            print('Failed getting art image: {} // error: {}'.format(
                url_art_crop, 
                e
            ))
        # Sleep for 500ms to avoid sending to many requests
        sleep(0.5)
        # stop if we reached the number of max. cards
        if idx == args.max_cards:
            break
    
    # save card metadata
    df_images = pd.DataFrame(arr_dict_card_info)
    df_images.to_csv(
        os.path.join(
            args.path_output,
            'card_images_{}_{}.csv'.format(args.start_idx, args.start_idx+args.max_cards)
            ), 
        sep=';', 
        index_label='index'
    )

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(
        'Artwork retrival using scryfall API'
    )
    argument_parser.add_argument('-si', '--start_idx', type=int, default=0, help='Index of first card to process in list of cards')
    argument_parser.add_argument('-mc', '--max_cards', type=int, default=1000, help='Max. number of artworks of cards to retrieve')
    argument_parser.add_argument('-po', '--path_output', type=str, default='./data/raw_images', help='Path where artwork images are saved to')

    args = argument_parser.parse_args()

    run(args)