import qrcode
from PIL import Image

# Fixed part of the URL
site = 'https://dev-in.skillup.online/'

# Function to generate QR code
def generate_qr_code(slug):
    # Construct the full URL
    url = f'{site}{slug}'
    
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add the URL data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')
    
    return img

# Function to overlay QR code on certificate
def overlay_qr_on_certificate(certificate_url, slug):
    # Generate QR code
    qr_img = generate_qr_code(slug)
    
    # Open the certificate image
    certificate = Image.open(certificate_url)
    
    # Resize QR code if necessary
    qr_img = qr_img.resize((100, 100))  # Adjust size as needed
    
    # Position to place the QR code (top right corner)
    position = (certificate.width - qr_img.width - 10, 10)  # Adjust position as needed
    
    # Paste the QR code onto the certificate
    certificate.paste(qr_img, position)
    
    # Save the final image
    certificate.save(f'{slug}_certificate_with_qr.png')

# Example usage
certificate_url = 'https://devcourses-in.skillup.online/media/Program_03_Microsoft_Azure_Solutions_Architect_Program_v2.jpg'
slug = 'microsoft-azure-solutions-architect-certification-program'
overlay_qr_on_certificate(certificate_url, slug)
