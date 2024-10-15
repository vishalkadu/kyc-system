import logging
import os
import re

import cv2
import face_recognition
import numpy as np
import pytesseract


class KYCVerificationSystem:
    def __init__(self, output_dir='kyc_results'):
        self.min_card_quality_score = 0.3
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=f'{output_dir}/kyc_verification.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def check_image_validity(image_path):
        """Check if image file exists and is valid"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Invalid image file")
            return img
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {str(e)}")
            raise

    def check_card_quality(self, card_image):
        """Check if the ID card image is of sufficient quality"""
        quality_score = 0.0

        # Convert to grayscale for analysis
        if len(card_image.shape) == 3:
            gray = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = card_image

        # Check for blur
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        logging.info(f"Blur score (Laplacian variance): {laplacian_var}")
        if laplacian_var > 100:
            quality_score += 0.3

        # Check for proper lighting
        brightness = np.mean(gray)
        logging.info(f"Brightness score: {brightness}")
        if 100 < brightness < 200:
            quality_score += 0.2

        # Check for tampering signs using edge detection
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.count_nonzero(edges) / edges.size
        logging.info(f"Edge density score: {edge_density}")
        if 0.05 < edge_density < 0.15:
            quality_score += 0.5

        logging.info(f"Overall quality score: {quality_score}")
        return quality_score > self.min_card_quality_score

    @staticmethod
    def pan_card_extract_text_and_identify(card_image):
        """Extract text from card and identify card type"""
        try:
            # Convert BGR to RGB for text extraction
            rgb_image = cv2.cvtColor(card_image, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(rgb_image)
            logging.info("Text extraction successful")
            logging.debug(f"Extracted text: {text}")

            # Clean the extracted text
            text = text.upper().replace(' ', '')

            # Identify card type based on patterns
            card_type = None
            # PAN card pattern: 5 letters + 4 numbers + 1 letter
            if re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text):
                card_type = 'PAN'
                logging.info("Card identified as PAN card")
            # Aadhaar card pattern: 12 digits (may be space-separated)
            elif re.search(r'[0-9]{12}|[0-9]{4}\s[0-9]{4}\s[0-9]{4}', text):
                card_type = 'AADHAAR'
                logging.info("Card identified as Aadhaar card")

            return {
                'card_type': card_type,
                'extracted_text': text
            }
        except Exception as e:
            logging.error(f"Text extraction failed: {str(e)}")
            return None

    @staticmethod
    def verify_face_match(person_image_path, card_image_path):
        """Verify if the face in person's photo matches the ID card photo"""
        try:
            # Load images
            person_image = face_recognition.load_image_file(person_image_path)
            card_image = face_recognition.load_image_file(card_image_path)

            # Get face encodings
            person_encodings = face_recognition.face_encodings(person_image)
            card_encodings = face_recognition.face_encodings(card_image)

            if not person_encodings or not card_encodings:
                logging.error("No face detected in one or both images")
                return False

            # Compare faces
            matches = face_recognition.compare_faces(
                [person_encodings[0]],
                card_encodings[0],
                tolerance=0.8
            )

            # Calculate face distance (lower means more similar)
            face_distance = face_recognition.face_distance(
                [person_encodings[0]],
                card_encodings[0]
            )[0]

            logging.info(f"Face match result: {matches[0]}, Distance: {face_distance}")
            return matches[0]

        except Exception as e:
            logging.error(f"Face verification failed: {str(e)}")
            return False

    def process_kyc(self, person_image_path, card_image_path):
        """Main KYC processing pipeline"""
        try:
            # Load and validate images
            logging.info(f"Processing KYC for person image: {person_image_path}")
            person_image = self.check_image_validity(person_image_path)
            card_image = self.check_image_validity(card_image_path)

            # Check card quality
            if not self.check_card_quality(card_image):
                result = {
                    'status': 'failed',
                    'reason': 'Poor card quality or potential tampering detected'
                }
                return result

            # Extract text and identify card
            card_info = self.pan_card_extract_text_and_identify(card_image)

            if not card_info or not card_info['card_type']:
                result = {
                    'status': 'failed',
                    'reason': 'Unable to identify card type'
                }
                logging.info(f"failed unable to find card type KYC for person image: {person_image_path}")
                return result

            # Verify face match
            if not self.verify_face_match(person_image_path, card_image_path):
                result = {
                    'status': 'failed',
                    'reason': 'Face verification failed'
                }
                logging.info(f"Failed KYC for person image: {person_image_path}")
                return result

            # All verifications passed
            result = {
                'status': 'success',
                'card_type': card_info['card_type'],
                'verification_complete': True
            }
            logging.info(f"Passed KYC for person image: {person_image_path}")
            return result

        except Exception as e:
            logging.error(f"KYC processing failed: {str(e)}")
            return {
                'status': 'error',
                'reason': str(e)
            }