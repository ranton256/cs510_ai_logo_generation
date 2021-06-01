import os
from PIL import Image
import argparse

'''
Run this program.

Source images should be in 'input/'
Output logos will go to 'logos/'

When entering the file names, don't include 'input/' or 'output/'

Minumum usage: python style_and_compose.py --CONTENT_IMAGE content_image_filename --STYLE_IMAGE style_image_filename --text "Text for Logo"
With the above usage, the source image will be re-written with a cropped version of itself and the logo will be saved as new_logo.jpg

Recommended minumum usage: python style_and_compose.py --CONTENT_IMAGE content_image_filename --STYLE_IMAGE style_image_filename --text "Text for Logo" --CROPPED_IMAGE filename_to_save_cropped_image --saveto save_to_file_name
The above will keep the original source image and will saved a new, cropped version, and will customize the name of the resulting logo
'''

parser = argparse.ArgumentParser(description='A Neural Algorithm of Artistic Style')
# Args for style transfer
parser.add_argument('--w1', '-w1',type=float, default='1',help='w1')
parser.add_argument('--w2', '-w2',type=float, default='1',help='w2')
parser.add_argument('--w3', '-w3',type=float, default='1',help='w3')
parser.add_argument('--w4', '-w4',type=float, default='1',help='w4')
parser.add_argument('--w5', '-w5',type=float, default='1',help='w5')
parser.add_argument("--IMAGE_WIDTH", "-width",type=int, default = 400, help = "width & height of image")
parser.add_argument("--CONTENT_IMAGE", "-CONTENT_IMAGE", type=str, help = "Path to content image")
parser.add_argument("--STYLE_IMAGE", "-STYLE_IMAGE", type=str, help = "Path to style image")
parser.add_argument("--CROPPED_IMAGE", "-CROPPED_IMAGE", type=str, help = "Path to content image", default="empty")
parser.add_argument("--GPU", "-GPU", help="Use GPU", action="store_true")
parser.add_argument("--alpha",  "-alpha",type=float,  default="0.001",   help="alpha")
parser.add_argument("--beta",   "-beta", type=float,  default="0.8",     help="beta")
parser.add_argument("--gamma",  "-gamma",type=float,  default="0.001",    help="gamma")
parser.add_argument("--epoch",  "-epoch",type=int, default=5000, help="number of epochs to run" )

#Args for image + type
parser.add_argument('--text', type=str, help='Text for the logo')
parser.add_argument('--stacked', help='Stack type, one word per line', action='store_true')
parser.add_argument('--textcolor', type=str, default='0, 0, 0', help='RGB colors for text; separate by commas; 0, 0, 0 - 255, 255, 255')
parser.add_argument('--fontsize', type=str, default='50', help='Font size')
parser.add_argument('--padding', type=str, default='50', help='Padding around image')
parser.add_argument('--spacer', type=str, default='50', help='Space between text and image')
parser.add_argument('--textspacing', type=str, default='15', help='Space between lines of text when stacked')
parser.add_argument('--saveto', type=str, default='new_logo.jpg', help='Space between lines of text when stacked')
parser.add_argument('--sans', help='Select sans serif typeface', action='store_true')
parser.add_argument('--serif', help='Select serif typeface', action='store_true')
parser.add_argument('--script', help='Select script typeface', action='store_true')
parser.add_argument('--bold', help='Select bold typeface', action='store_true')
parser.add_argument('--ital', help='Select italic serif typeface', action='store_true')
parser.add_argument('--alignleft', help='Align image to the left of the text', action='store_true')
parser.add_argument('--alignright', help='Align image to the right of the text', action='store_true')
parser.add_argument('--aligncenter', help='Center image and text', action='store_true')
args = parser.parse_args()

# try:
#     source_image = Image.open(args.CONTENT_IMAGE)
# except:
#     print('Error loading image.')
#     exit()

# source_size = source_image.size
# source_image_width, source_image_height = source_image.size
# EDIT: Made it 500 x 500 to make it a bit bigger
crop_image = f'python crop_image.py --CONTENT_IMAGE {args.CONTENT_IMAGE} --CROPPED_IMAGE {args.CROPPED_IMAGE}'

os.system(crop_image)


if args.CROPPED_IMAGE != 'empty':
    args.CONTENT_IMAGE = args.CROPPED_IMAGE


args.IMAGE_WIDTH = 300



style_transfer_commands = f'python StyleTransfer.py -w1 {args.w1} -w2 {args.w2} -w3 {args.w3} -w4 {args.w4} -w5 {args.w5} --IMAGE_WIDTH {args.IMAGE_WIDTH} -CONTENT_IMAGE {args.CONTENT_IMAGE} -STYLE_IMAGE {args.STYLE_IMAGE} -alpha {args.alpha} -beta {args.beta} -gamma {args.gamma} -epoch {args.epoch}'

if args.GPU:
    style_transfer_commands += ' -GPU'

os.system(style_transfer_commands)


CONTENT_IMAGE = args.CONTENT_IMAGE
STYLE_IMAGE = args.STYLE_IMAGE

# Splitting content path & name
dot = 0
slash = 0
for c in reversed(CONTENT_IMAGE):
    dot += 1
    if c == ".":
        break
for c in reversed(CONTENT_IMAGE):
    slash += 1 
    if c =="/" or c =="\\":
        break
content_path = CONTENT_IMAGE[:1-slash]
content_name = CONTENT_IMAGE[-slash:-dot]

# Splitting style path & name
dot = 0 
slash = 0 
for c in reversed(STYLE_IMAGE):
    dot += 1
    if c == ".":
        break
for c in reversed(STYLE_IMAGE):
    slash += 1
    if c == "/" or c =="\\":
        break
style_path = STYLE_IMAGE[:1-slash]
style_name = STYLE_IMAGE[-slash:-dot]

OUTPUT_DIR = ("output/" + content_name + "_vs_" + style_name)
f = []
for (dirpath, dirnames, filenames) in os.walk(OUTPUT_DIR):
    f.extend(filenames)
print(f)
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for item in f:
    if item[0] not in numbers:
        f.remove(item)
f.sort(key = lambda w: int(w[0:-4]))
image_path = os.path.join(OUTPUT_DIR, f[-1])
try:
    source_image = Image.open('input/' + CONTENT_IMAGE)
    source_image.thumbnail((args.IMAGE_WIDTH, args.IMAGE_WIDTH))
    resize_width, resize_height = source_image.size
except:
    print('Error loading image.')
    exit()

compose_commands = f'python image_and_type.py --image {image_path} --text \'{args.text}\' --textcolor \'{args.textcolor}\' --fontsize {args.fontsize} --padding {args.padding} --spacer {args.spacer} --textspacing {args.textspacing} --saveto {args.saveto} --resize {resize_width}x{resize_height}'

if args.stacked:
    compose_commands += ' --stacked'
if args.sans:
    compose_commands += ' --sans'
if args.serif:
    compose_commands += ' --serif'
if args.script:
    compose_commands += ' --script'
if args.bold:
    compose_commands += ' --bold'
if args.ital:
    compose_commands += ' --ital'
if args.alignleft:
    compose_commands += ' --alignleft'
if args.alignright:
    compose_commands += ' --alignright'
if args.aligncenter:
    compose_commands += ' --aligncenter'


os.system(compose_commands)




