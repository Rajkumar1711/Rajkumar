import qrcode
from PIL import Image
import requests
from io import BytesIO

site = 'https://dev-in.skillup.online/'

def generate_qr_code(slug):
    url = f'{site}{slug}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    return img

def overlay_qr_on_certificate(certificate_url, slug):
    # Download the image from the URL
    response = requests.get(certificate_url)
    certificate = Image.open(BytesIO(response.content))
    
    qr_img = generate_qr_code(slug)
    qr_img = qr_img.resize((350, 350)) 
    position = (certificate.width - qr_img.width - 150, 150)
    certificate.paste(qr_img, position)
    certificate.save(f'{slug}_certificate_with_qr.png')

# Example usage
certificate_url = 'https://devcourses-in.skillup.online/media/Program_03_Microsoft_Azure_Solutions_Architect_Program_v2.jpg'
slug = 'microsoft-azure-solutions-architect-certification-program'
overlay_qr_on_certificate(certificate_url, slug)
