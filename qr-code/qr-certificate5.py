import qrcode
from PIL import Image, ImageDraw, ImageFont
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

def overlay_qr_on_certificate(certificate_url, slug, username):
    # Download the image from the URL
    response = requests.get(certificate_url)
    certificate = Image.open(BytesIO(response.content))
    
    # Generate QR code
    qr_img = generate_qr_code(slug)
    qr_img = qr_img.resize((350, 350)) 
    position = (certificate.width - qr_img.width - 150, 150)
    certificate.paste(qr_img, position)
    
    # Add username to the certificate
    draw = ImageDraw.Draw(certificate)
    font = ImageFont.truetype("arial.ttf", 200)  # You can change the font and size as needed
    bbox = draw.textbbox((0, 0), username, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_position = ((certificate.width - text_width) / 2.2, (certificate.height - text_height) / 2.2)
    draw.text(text_position, username, font=font, fill="black")
    
    certificate.save(f'{slug}_certificate_with_qr.png')

# Example usage
certificate_url = 'https://devcourses-in.skillup.online/media/Program_03_Microsoft_Azure_Solutions_Architect_Program_v2.jpg'
slug = 'microsoft-azure-solutions-architect-certification-program'
username = 'Raj Kumar'
overlay_qr_on_certificate(certificate_url, slug, username)
