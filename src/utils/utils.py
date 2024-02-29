import fitz


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store the extracted text
    text_content = ""

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the current page
        page = pdf_document[page_number]

        # Extract text from the page
        text_content += page.get_text()

    # Close the PDF file
    pdf_document.close()

    return text_content
