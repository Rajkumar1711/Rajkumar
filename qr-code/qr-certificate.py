import qrcode

# URL to be encoded in the QR code
url = 'https://dev-in.skillup.online/data-science-and-artificial-intelligence-techmasters-program/'

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
img.save('program_about_page_qr.png')
