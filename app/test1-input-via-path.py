import os

from kyc1 import KYCVerificationSystem


def test_kyc():
    # Initialize the KYC system
    kyc_system = KYCVerificationSystem(output_dir='kyc_results')

    # Replace these paths with your actual image paths

    # # tamperd image
    person_photo_path = "../data/Subject.png"
    id_card_path = "../data/id_card.png"

    # incorrect peroson
    # person_photo_path = "../data/subject-k.jpg"
    # id_card_path = "../data/sample-pan-card-clear-img.jpg"

    # correct person and correct id card
    #
    #person_photo_path = "../data/Subject.png"
    # id_card_path = "../data/id_card.png"

    # Verify paths exist
    if not os.path.exists(person_photo_path):
        print(f"Error: Person photo not found at {person_photo_path}")
        return
    if not os.path.exists(id_card_path):
        print(f"Error: ID card photo not found at {id_card_path}")
        return

    # Process the KYC verification
    print("\nProcessing KYC verification...")
    result = kyc_system.process_kyc(person_photo_path, id_card_path)

    # Print the results
    print("\nKYC Verification Results:")
    print("-" * 30)
    print(f"Status: {result['status']}")
    if 'reason' in result:
        print(f"Reason: {result['reason']}")
    if 'card_type' in result:
        print(f"Card Type: {result['card_type']}")
    print("-" * 30)


if __name__ == "__main__":
    test_kyc()
