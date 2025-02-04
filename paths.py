from libraries import *
def resource_path(relative_path):

    try:
       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

base_dir = resource_path(r'your application path')
# Update paths to use resource_path
template_dir = os.path.join(base_dir, 'templates') # path to the invoice templates file


templates = {
    "جواهرات": os.path.join(template_dir, "your invoice template for jwelery name (.jpeg fromat)"),
    "طلا": os.path.join(template_dir, "your invoice template for gold name (.jpeg fromat)"),
}

output_dir = resource_path(r'your path that you want to save your generated invoices')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
font_path = os.path.join(base_dir, 'assets', 'Arial.ttf')
font = ImageFont.truetype(font_path, 24)
pdfmetrics.registerFont(TTFont('Arial', font_path))
