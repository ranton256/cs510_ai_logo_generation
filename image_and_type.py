from PIL import Image, ImageFont, ImageDraw
import os
import argparse

from numpy.core.fromnumeric import resize

'''
Create a logo by combining an imagr with text

Usage: python image_and_type.py --image imagelocation --text 'Text To Render'

Optional parameters:
--stacked: flag to indicate that text is rendered stacked, one word per line
--textcolor R,G,B (str): RGB values for the text color, expressed as R,G,B 
    (no spaces), where 0 <= R, G, B <= 255; default is black
--fontsize N (int): Determines the size of the text to render, where N > 0; 
    default is 50
--padding N (int): Additional blank space around the logo; default is 50
--spacer N (int): Space between the image and the text; default is 50
--textspacing N (int): Space between lines for stacked text; default is 50
--saveto filename (str): File name to save the logo; default is 'new_logo.jpg'
--sans: flag to select a sans serif font; if no font flag is selected, this
    is the default
--serif: flag to select a serif font
--script: flag to select a script font
--bold: flag to make the font bold
--ital: flag to make the font italic
--alignleft: flag to alignt the text and image to the left
--alignright: flag to align the tedt and image to the right
--aligncenter: flag to denter text and image; if no alignment flag is selected,
    this is the default
--resize widthxheight (str): if we want to resize the image, enter the dimentions with an x
'''


def render_text_oneline(img, font, text, color=(255, 255, 255), top=None):
    '''
    Render text in one line, centered in the image.

    Args: 
        img: Image object where we'll write the text
        font: Font object we'll use to determine the style for the text
        text (string): Text we will render
        color (tupple of ints): RGB values for the color for the text; each value 
            ranges 0 - 255; the default is black
        top (int): Top position for the text, relative to the top of the image

    Returns:
        Renders text directly on the img image object
    '''
    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)
    text_width, text_height = calculate_text_size_oneline(font, text)
    if top is None:
        position = ((image_width-text_width)/2,(image_height-text_height)/2)
    else:
        position = ((image_width-text_width)/2,top)
    draw.text(position, text, color, font=font)
    return img

def render_text_stacked(img, font, text,  color=(255, 255, 255), top=None, vertical_spacing=10, padding=10, align='center'):
    '''
    Render text in multiple lines (one line per word), left aligned to the image.

    Args: 
        img: Image object where we'll write the text
        font: Font object we'll use to determine the style for the text
        text (string): Text we will render
        color (tupple of ints): RGB values for the color for the text; each value 
            ranges 0 - 255; the default is black
        top (int): Top position for the text, relative to the top of the image
        vertical_spacing (int): Spacing between the lines of text, in pixels
        padding (int): Padding around the image, used to calculate text position
        align (str): Indicates the alignment of the stacked text (left, right, 
            center); default is center
    Returns:
        Renders text directly on the img image object
    '''
    draw = ImageDraw.Draw(img)
    widths = []
    words = text.split(' ')
    image_width, image_height = img.size
    for word in words:
        text_width, text_height = draw.textsize(word, font)
        widths.append(text_width)
    text_width = max(widths)
    if top is None:
        top = (image_height-text_height)/2
    for index in range(len(words)):
        if align == 'left':
            position_left = padding
        elif align == 'right':
            position_left = image_width - padding - widths[index]
        else:
            position_left = (image_width-widths[index])/2
        position_top = top + (text_height + vertical_spacing) * index
        position = (position_left, position_top)
        draw.text(position, words[index], color, font=font) 

def render_text(img, font, text, color=(255, 255, 255), top=None, vertical_spacing=10, padding=10, align_left=False, align_right=False, stacked=False):
    '''
    Wrapper function to determine with text rendeding function we'll use
    '''
    if align_left:
        alignment = 'left'
    elif align_right:
        alignment = 'right'
    else:
        alignment = 'center'
    
    if stacked:
        render_text_stacked(img, font, text, color, top, vertical_spacing, padding, alignment)
    else:
        render_text_oneline(img, font, text, color, top)
        
def calculate_text_size_oneline(font, text):
    '''
    Determine the width and the height of the rendered text, when the text is
    rendered in one line.

    Args: 
        font: Font object we'll use to determine the style for the text
        text (string): Text we will render
            ranges 0 - 255; the default is black

    Returns:
        The width and the height of the rendered text
    '''    
    txt = Image.new("RGB", (10, 10), (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    text_width, text_height = draw.textsize(text, font)
    return text_width, text_height

def calculate_text_size_stacked(font, text, vertical_spacing = 10):
    '''
    Determine the width and the height of the rendered text, when the text is
    rendered in multiple lines.
    Args: 
        font: Font object we'll use to determine the style for the text
        text (string): Text we will render
        vertical_spacing (int): Spacing between the lines of text, in pixels

    Returns:
        Renders text directly on the img image object
    '''
    txt = Image.new("RGB", (10, 10), (255,255,255,0))
    draw = ImageDraw.Draw(txt)
    widths = []
    words = text.split(' ')
    for word in words:
        text_width, text_height = draw.textsize(word, font)
        widths.append(text_width)
    text_width = max(widths)
    text_height = ((text_height + vertical_spacing) * len(words)) - vertical_spacing
    return text_width, text_height
    
def calculate_text_size(font, text, vertical_spacing=10, stacked=False):
    '''
    Wrapper function to determine which function we'll ue to calculate the
    size of the rendered text
    '''
    if stacked:
        return calculate_text_size_stacked(font, text, vertical_spacing)
    else:
        return calculate_text_size_oneline(font, text)


def select_font(sans, serif, script, bold, ital):
    '''
    Determine which font we'll be using, depending on the parameters entered
    by the user

    Args:
        sans, serif, script, bold, ital (bool): Each parameter holds the 
            corresponding attribute for the chosen font
    Returns:
        The path for the selected font based on the parameters
    '''
    if sans or (not serif and not script):
        if bold and ital:
            font = os.path.join('fonts', 'Roboto', 'Roboto-BoldItalic.ttf')
        elif bold:
            font = os.path.join('fonts', 'Roboto', 'Roboto-Bold.ttf')
        elif ital:
            font = os.path.join('fonts', 'Roboto', 'Roboto-Italic.ttf')
        else:
            font = os.path.join('fonts', 'Roboto', 'Roboto-Regular.ttf')
    elif serif:
        if bold and ital:
            font = os.path.join('fonts', 'Merriweather', 'Merriweather-BoldItalic.ttf')
        elif bold:
            font = os.path.join('fonts', 'Merriweather', 'Merriweather-Bold.ttf')
        elif ital:
            font = os.path.join('fonts', 'Merriweather', 'Merriweather-Italic.ttf')
        else:
            font = os.path.join('fonts', 'Merriweather', 'Merriweather-Regular.ttf')
    elif script:
        if bold:
            font = os.path.join('fonts', 'Charmonman', 'Charmonman-Bold.ttf')
        else:
            font = os.path.join('fonts', 'Charmonman', 'Charmonman-Regular.ttf')
    return font


if __name__ == '__main__':
    # Ask user for arguments. The only required arguments are are --image and --text
    parser = argparse.ArgumentParser(description='Combine an image and text')
    parser.add_argument('--image', type=str, help='Location of image for the logo')
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
    parser.add_argument('--resize', type=str, help='widthxheight', default=None)
    args = parser.parse_args()

    # Cast inputs as needed
    spacer = int(args.spacer)
    padding = int(args.padding)
    font_size = int(args.fontsize)
    text_spacing = int(args.textspacing)
    text_color = args.textcolor.split(',')
    text_color = (int(text_color[0]), int(text_color[1]), int(text_color[2]))
    image_size = 300
    
    # --text and --image are the two required arguments; if we don't have one or 
    #   the other, we print an error message and exit the program
    error_message = ''
    error = False
    if args.text is None:
        error = True
        error_message += 'Missing text for logo (--text \'Text for Logo\'). '
    if args.image is None:
        if error_message != '':
            error_message += '\n'
        error_message += 'Missing image for logo (--image image_location). '
    if error:
        print(error_message)
        exit()

    # Load the image and resize it; exit if there's an error
    print(args.image)
    try:
        source_image = Image.open(args.image)
        if args.resize is not None:
            resize_width, resize_height = args.resize.split('x')
            resize_width, resize_height = int(resize_width), int(resize_height)
            print(resize_width, resize_height)
            source_image = source_image.resize((resize_width, resize_height))
            #source_image.resize((resize_width, resize_height))
        else:
            source_image.thumbnail((image_size, image_size))
    except:
        print('Error loading image.')
        exit()

    # Pick the right font and create a font object to render the text
    font = ImageFont.truetype(select_font(args.sans, args.serif, args.script, args.bold, args.ital), font_size)

    # Determine all the dimensions needed, including the image size for the output logo
    source_image_width, source_image_height = source_image.size
    text_width, text_height = calculate_text_size(font, args.text, text_spacing, args.stacked)
    logo_width = max(source_image_width, text_width) + padding * 2
    logo_height = source_image_height + text_height + spacer + padding * 2
    
    # Create an image object for the logo that will combine the image and text
    logo = Image.new("RGB", (logo_width, logo_height), (255,255,255,0))

    # Determine the position of the source image relative to the logo based on 
    #   the user arguments, and place the image within the logo
    if args.alignleft:
        image_left = padding
    elif args.alignright:
        image_left = logo_width - source_image_width - padding
    else:
        image_left = (logo_width - source_image_width) // 2

    logo.paste(source_image, (image_left, padding))

    # Render the type; depending on the 
    text_top = padding + source_image_height + spacer
    render_text(logo, font, args.text, text_color, text_top, text_spacing, padding, args.alignleft, args.alignright, args.stacked)

    logo.save(args.saveto)