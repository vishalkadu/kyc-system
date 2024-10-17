import os
import streamlit as st
from PIL import Image
from kyc1 import KYCVerificationSystem  # Import your KYC system

def load_image(image_file):
    """Load and return an image from an uploaded file."""
    return Image.open(image_file)

def save_image(image_file, save_path):
    """Save the uploaded image file to the specified path with error handling."""
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(image_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Failed to save image: {e}")
        return False

def display_images(id_card, person_photo):
    """Display ID card and person's photo side by side."""
    st.markdown("<h3 style='text-align: center;'>Provided Documents</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image(load_image(id_card), caption="ID Card", use_column_width=True)
    with col2:
        st.image(load_image(person_photo), caption="Your Photo", use_column_width=True)
    st.markdown("---")

def verify_kyc(kyc_system, id_card_path, person_photo_path):
    """Perform KYC verification and display results."""
    with st.spinner("Processing ID verification..."):
        result = kyc_system.process_kyc(person_photo_path, id_card_path)
    st.markdown("<h3 style='text-align: center;'>ID Verification Results</h3>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"**Status**: {result.get('status', 'Unknown')}")
    if 'reason' in result:
        st.markdown(f"**Reason**: {result['reason']}")
    if 'card_type' in result:
        st.markdown(f"**Card Type**: {result['card_type']}")
    st.markdown("<hr>", unsafe_allow_html=True)

def main():
    # App title and introduction
    st.markdown("<h1 style='text-align: center; color: #4F8A8B;'>ID Verification System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #556B2F;'>Secure and Fast KYC Verification</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # Initialize the KYC system
    kyc_system = KYCVerificationSystem(output_dir='kyc_results')

    # Step 1: Capture or Upload ID Card Image
    st.markdown("### Step 1: Capture or Upload ID Card Image")
    id_card_option = st.radio("Select how to provide your ID card:", ('Capture ID via Webcam', 'Upload ID Card Image'))
    id_card = st.camera_input("Capture your ID card via webcam") if id_card_option == 'Capture ID via Webcam' else st.file_uploader("Upload ID card image", type=['jpg', 'png', 'jpeg'])
    st.markdown("---")

    # Step 2: Capture or Upload Person's Photo
    st.markdown("### Step 2: Capture or Upload Your Photo")
    person_photo_option = st.radio("Select how to provide your photo:", ('Capture Photo via Webcam', 'Upload Photo from Device'))
    person_photo = st.camera_input("Capture your photo via webcam") if person_photo_option == 'Capture Photo via Webcam' else st.file_uploader("Upload your photo", type=['jpg', 'png', 'jpeg'])
    st.markdown("---")

    # Display images and proceed with verification
    if id_card and person_photo:
        display_images(id_card, person_photo)

        # Button to start KYC verification
        if st.button("Verify My ID"):
            id_card_path = "data/id_card_temp.png"
            person_photo_path = "data/person_photo_temp.png"

            # Save images to specified paths
            if save_image(id_card, id_card_path) and save_image(person_photo, person_photo_path):
                verify_kyc(kyc_system, id_card_path, person_photo_path)
            else:
                st.error("Failed to process images. Please try again.")

if __name__ == "__main__":
    main()
