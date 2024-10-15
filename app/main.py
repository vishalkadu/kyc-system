import streamlit as st
from PIL import Image
from kyc1 import KYCVerificationSystem  # Import your KYC system


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main():
    # App title and introduction
    st.markdown("<h1 style='text-align: center; color: #4F8A8B;'>ID Verification System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #556B2F;'>Secure and Fast KYC Verification</h4>",
                unsafe_allow_html=True)
    st.markdown("---")

    # Initialize the KYC system
    kyc_system = KYCVerificationSystem(output_dir='kyc_results')

    # Step 1: Capture or Upload ID Card Image
    st.markdown("### Step 1: Capture or Upload ID Card Image")
    st.markdown("<p style='color: #556B2F;'>Select how to provide your ID card:</p>", unsafe_allow_html=True)
    id_card_option = st.radio("", ('Capture ID via Webcam', 'Upload ID Card Image'))

    if id_card_option == 'Capture ID via Webcam':
        id_card = st.camera_input("Capture your ID card via webcam")
    else:
        id_card = st.file_uploader("Upload ID card image", type=['jpg', 'png', 'jpeg'])

    st.markdown("---")

    # Step 2: Capture or Upload Person's Photo
    st.markdown("### Step 2: Capture or Upload Your Photo")
    st.markdown("<p style='color: #556B2F;'>Select how to provide your photo:</p>", unsafe_allow_html=True)
    person_photo_option = st.radio("", ('Capture Photo via Webcam', 'Upload Photo from Device'))

    if person_photo_option == 'Capture Photo via Webcam':
        person_photo = st.camera_input("Capture your photo via webcam")
    else:
        person_photo = st.file_uploader("Upload your photo", type=['jpg', 'png', 'jpeg'])

    st.markdown("---")

    # Display images and proceed with verification
    if id_card is not None and person_photo is not None:
        # Display uploaded ID card and photo
        st.markdown("<h3 style='text-align: center;'>Provided Documents</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image(load_image(id_card), caption="ID Card", use_column_width=True)
        with col2:
            st.image(load_image(person_photo), caption="Your Photo", use_column_width=True)

        st.markdown("---")

        # Button to start KYC verification
        if st.button("Verify My ID", key="verify_button"):
            # Save images for processing
            id_card_path = "../data/id_card_temp.png"
            person_photo_path = "../data/person_photo_temp.png"

            # Write ID card data to file
            with open(id_card_path, "wb") as f:
                f.write(id_card.getbuffer())

            # Write person photo data to file
            with open(person_photo_path, "wb") as f:
                f.write(person_photo.getbuffer())

            # Perform KYC verification
            with st.spinner("Processing ID verification..."):
                result = kyc_system.process_kyc(person_photo_path, id_card_path)

            # Display KYC results
            st.markdown("<h3 style='text-align: center;'>ID Verification Results</h3>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"**Status**: {result.get('status', 'Unknown')}")
            if 'reason' in result:
                st.markdown(f"**Reason**: {result['reason']}")
            if 'card_type' in result:
                st.markdown(f"**Card Type**: {result['card_type']}")
            st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()