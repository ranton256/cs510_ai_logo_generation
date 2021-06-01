from PIL import Image, ImageOps
import argparse

parser = argparse.ArgumentParser(description='A Neural Algorithm of Artistic Style')
# Args for style transfer
parser.add_argument("--CONTENT_IMAGE", "-CONTENT_IMAGE", type=str, help = "Path to content image")
parser.add_argument("--CROPPED_IMAGE", "-CROPPED_IMAGE", type=str, help = "Path to content image", default="empty")


args = parser.parse_args()

image_name = args.CONTENT_IMAGE

if args.CROPPED_IMAGE == 'empty':
    saved_image = args.CONTENT_IMAGE
else:
    saved_image = 'output/' + args.CROPPED_IMAGE

try:
    source_image = Image.open(image_name)
    white_background = Image.new('RGBA', source_image.size, (255, 255, 255))
    source_image = Image.alpha_composite(white_background, source_image)
    source_image = source_image.convert('RGB')
    invert_image = source_image.convert('RGB')
    invert_image = ImageOps.invert(invert_image)
    trim_box = invert_image.getbbox()
    source_image = source_image.crop(trim_box)
    source_image.save(saved_image)
except Exception as e:
    print('Error loading image.')
    print(e)
    exit()