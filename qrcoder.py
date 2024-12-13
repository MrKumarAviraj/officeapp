import streamlit as st
import qrcode
from PIL import Image
import io

st.title("Enhanced QR Code Generator")

# Input data for the QR code
data = st.text_input("Enter the data or URL for the QR Code:", "")

# File upload for logo (optional)
logo_file = st.file_uploader("Upload a logo to embed in the QR Code (optional):", type=["png", "jpg", "jpeg"])

# Generate QR Code
if st.button("Generate QR Code"):
    if data:
        # Create QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction to accommodate a logo
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Add logo to the QR code if provided
        if logo_file is not None:
            logo = Image.open(logo_file)
            # Resize logo
            logo_size = min(img.size[0] // 4, img.size[1] // 4)  # Logo size as a fraction of QR size
            logo = logo.resize((logo_size, logo_size))

            # Calculate position for the logo
            x = (img.size[0] - logo.size[0]) // 2
            y = (img.size[1] - logo.size[1]) // 2
            img.paste(logo, (x, y), logo)

        # Display the QR Code
        st.image(img, caption="Generated QR Code", use_column_width=True)

        # Prepare image for download
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Provide a download button
        st.download_button(
            label="Download QR Code",
            data=buffer,
            file_name="qr_code.png",
            mime="image/png",
        )
    else:
        st.warning("Please enter some data to generate a QR Code.")
