# KYC Verification System

## Overview

The **KYC Verification System** is a streamlined tool for verifying identity documents in a KYC (Know Your Customer) workflow. This system doesn't require complex model training; instead, it leverages robust libraries to conduct image quality checks, card type identification, and face matching. The setup includes a simple UI, custom logic, and application-specific wrapper code for fast, reliable verification with impressive accuracy.

## Features

- **Image Quality Verification**: Analyzes image clarity, lighting, and potential tampering.
- **Card Type Identification**: Recognizes PAN and Aadhaar cards based on extracted text patterns.
- **Face Matching**: Compares a user's ID photo to their provided photo, ensuring a match.
- **Easy Integration**: The system is designed to fit into any KYC workflow with minimal setup.
- **User-Friendly UI**: The optional UI provides a smooth experience for uploading and verifying ID documents.

## Getting Started

### Prerequisites

Before using the KYC Verification System, make sure the following libraries are installed:

- Python 3.9+
- OpenCV (cv2)
- face_recognition
- numpy
- pytesseract
- re (for regular expressions)
- os (standard library)
- logging (standard library)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/vishalkadu/kyc-system.git
   cd kyc-verification-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Tesseract OCR: Install Tesseract OCR on your machine if it's not already installed. Ensure that pytesseract points to the correct installation path.

4. Set up the output directory: The system logs and stores results in an `output_dir`. The default is `kyc_results`, but this can be customized during initialization.

## Usage

The system can be run as a script or integrated into other applications. To process a KYC case, follow these steps:

1. Initialize the System:
   ```python
   from kyc_verification import KYCVerificationSystem
   kyc_system = KYCVerificationSystem(output_dir='kyc_results')
   ```

2. Process KYC:
   ```python
   result = kyc_system.process_kyc(person_image_path='path/to/person_image.jpg', card_image_path='path/to/card_image.jpg')
   print(result)
   ```

## Detailed Workflow

The KYC system works in stages, each implemented as a separate function within `KYCVerificationSystem`:

1. **Image Validity Check**:
   - Verifies if the provided image files exist and are in a readable format.
   - Method: `check_image_validity`

2. **Image Quality Check**:
   - Analyzes the image for clarity, proper lighting, and signs of tampering.
   - Quality metrics are calculated based on:
     - Blur detection: Using Laplacian variance.
     - Brightness: Checking if the brightness level falls within an optimal range.
     - Edge density: Verifying edge density for signs of tampering.
   - Method: `check_card_quality`

3. **Text Extraction and Card Type Identification**:
   - Extracts text from the image using pytesseract.
   - Identifies PAN and Aadhaar cards based on text patterns.
   - Method: `pan_card_extract_text_and_identify`

4. **Face Matching**:
   - Compares the face in the user's photo to the ID card photo.
   - Uses face_recognition to encode faces and compare encodings for similarity.
   - Method: `verify_face_match`

## Logging

All steps in the KYC process, including successes and errors, are logged for easy debugging and record-keeping. The logs are stored in `output_dir` under the filename `kyc_verification.log`.

## Example Results

The result of a KYC process will return a JSON-like structure with a status and details:

```json
{
    "status": "success",
    "card_type": "PAN",
    "verification_complete": true
}
```

Or if verification fails at any stage:

```json
{
    "status": "failed",
    "reason": "Face verification failed"
}
```

## Customization

- **Threshold Tuning**: The KYC system can be fine-tuned by adjusting quality scores and tolerance levels. For example:
  - Change `self.min_card_quality_score` to adjust card quality thresholds.
  - Adjust tolerance in `verify_face_match` for face matching sensitivity.
- **Additional Card Types**: Add new regex patterns in `pan_card_extract_text_and_identify` to support other types of ID cards.

## Limitations & Future Enhancements

- **Environmental Dependencies**: The system relies on image quality and lighting conditions. Ensure images are well-lit and free of noise for optimal results.
- **Face Recognition Accuracy**: Face matching may vary based on angle, lighting, and facial occlusions (e.g., masks, glasses).
- **Future Additions**:
  - Enhanced support for different ID formats.
  - Advanced tampering detection using machine learning models.
  - Additional UI features for a smoother user experience.

## Contributing

If you'd like to contribute to the development of this project, please fork the repository and submit a pull request. Bug reports and feature requests are also welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Special thanks to the open-source projects and libraries used, including OpenCV, face_recognition, and pytesseract, for making this KYC Verification System possible.

Happy Coding! 🚀
