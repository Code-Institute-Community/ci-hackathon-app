import base64


def image_to_base64str(image):
    """ Converts an image file to base64 string """
    file_bytes = image.file.read()
    base64_img_str = 'data:image;base64, '
    base64_img_str += str(base64.b64encode(file_bytes), 'utf-8')
    return base64_img_str
