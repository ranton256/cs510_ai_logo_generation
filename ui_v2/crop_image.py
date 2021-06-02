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
    source_image = source_image.convert('RGBA')
    white_background = Image.new('RGBA', source_image.size, (255,255,255))
    source_image = Image.alpha_composite(white_background, source_image)
    source_image = source_image.convert('RGB')
    invert_image = source_image.convert('RGB')
    invert_image = ImageOps.invert(invert_image)
    print('post')
    trim_box = invert_image.getbbox()
    source_image = source_image.crop(trim_box)
    size = source_image.size
    max_size = max(size[0], size[1])
    square = Image.new('RGB', (max_size, max_size), (255,255,255))
    position = ((max_size - size[0]) // 2, (max_size - size[1]) // 2)
    square.paste(source_image, position)
    square.save(saved_image)
except:
    print('Error loading image.')
    exit()