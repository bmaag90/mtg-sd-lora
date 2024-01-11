from PIL import Image
import argparse
import os

def run(args):

    for l in os.listdir(args.path_img):
        print('Artwork image file: {}'.format(l))
        if not (l.endswith('.jpg') or l.endswith('.png')):
            continue
        img = Image.open(os.path.join(args.path_img, l))
        print(img.size)
        img_resized = img.resize(
            (args.size_x,args.size_y)
        )

        img_resized.save(os.path.join(args.path_output, l))

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(
        'Artwork image preprocessing, i.e. resizing for model'
    )
    argument_parser.add_argument('-pi', '--path_img', type=str, default='data/raw_images', help='Path to folder containing raw image')
    argument_parser.add_argument('-po', '--path_output', type=str, default='./data/proc', help='Path where resized artwork images are saved to')
    argument_parser.add_argument('-sx', '--size_x', type=int, default=512, help='New x size (width) of img')
    argument_parser.add_argument('-sy', '--size_y', type=int, default=512, help='New y size (height) of img')
    args = argument_parser.parse_args()

    run(args)