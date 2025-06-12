import qrcode

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
    
    # Save the QR code image
    img.save(f'{slug}_qr.png')

# Example usage
slug = 'microsoft-azure-solutions-architect-certification-program'
generate_qr_code(slug)
