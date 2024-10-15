import streamlit as st
from PIL import Image

from kyc1 import KYCVerificationSystem  # Import your KYC system


def load_image(image_file):
    img = Image.open(image_file)
    return img


def main():
    st.title("ID Verification System")

    # Initialize the KYC system
    kyc_system = KYCVerificationSystem(output_dir='kyc_results')

    # Step 1: Capture or Upload ID Card Image
    st.write("### Step 1: Capture your ID card or upload an image")

    id_card_option = st.radio("Select how to provide your ID card", ('Capture ID via Webcam', 'Upload ID Card Image'))

    if id_card_option == 'Capture ID via Webcam':
        id_card = st.camera_input("Capture your ID card via webcam")
    else:
        id_card = st.file_uploader("Upload ID card image", type=['jpg', 'png', 'jpeg'])

    # Step 2: Capture or Upload Person's Photo
    st.write("### Step 2: Capture your face or upload a photo")

    person_photo_option = st.radio("Select how to provide your photo",
                                   ('Capture Photo via Webcam', 'Upload Photo from Device'))

    if person_photo_option == 'Capture Photo via Webcam':
        person_photo = st.camera_input("Capture your photo via webcam")
    else:
        person_photo = st.file_uploader("Upload your photo", type=['jpg', 'png', 'jpeg'])

    # Proceed if both ID card and photo (captured or uploaded) are available
    if id_card is not None and person_photo is not None:
        # Display uploaded ID card and photo
        st.image(load_image(id_card), caption="Provided ID Card", use_column_width=True)

        if person_photo_option == 'Capture Photo via Webcam':
            st.image(person_photo, caption="Captured Photo", use_column_width=True)
        else:
            st.image(load_image(person_photo), caption="Uploaded Photo", use_column_width=True)

        # Provide option to proceed with KYC verification
        if st.button("Proceed with ID Verification"):
            # Save images for processing
            id_card_path = "../data/id_card_temp.png"
            person_photo_path = "../data/person_photo_temp.png"

            with open(id_card_path, "wb") as f:
                f.write(id_card.getbuffer())

            # For captured photo, we need to convert it to bytes
            if person_photo_option == 'Capture Photo via Webcam':
                person_photo.save(person_photo_path)
            else:
                with open(person_photo_path, "wb") as f:
                    f.write(person_photo.getbuffer())

            # Perform KYC verification
            st.write("\nProcessing ID verification...")
            result = kyc_system.process_kyc(person_photo_path, id_card_path)

            # Display KYC results
            st.write("\nID Verification Results:")
            st.write("-" * 30)
            st.write(f"**Status**: {result['status']}")
            if 'reason' in result:
                st.write(f"**Reason**: {result['reason']}")
            if 'card_type' in result:
                st.write(f"**Card Type**: {result['card_type']}")
            st.write("-" * 30)


if __name__ == "__main__":
    main()
