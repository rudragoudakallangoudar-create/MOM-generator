import google.genai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

from dotenv import load_dotenv
load_dotenv() #activate api key

# Configure The Model
key = os.getenv('GOOGLE_API_KEY')
client = genai.Client(api_key=key)

# Create outputs directory if it doesn't exist
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# Function to extract text using Tesseract
def extract_text_tesseract(image):
    try:
        # Convert PIL to numpy array
        image_np = np.array(image)
        # Convert to grayscale
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Extract text
        text = pytesseract.image_to_string(thresh)
        return text
    except Exception as e:
        return f"Error in Tesseract extraction: {str(e)}"

# Function to combine texts
def combine_texts(texts_dict):
    combined = ""
    for source, text in texts_dict.items():
        if text and not text.startswith("Error") and not text.startswith("PDF file not found"):
            combined += f"{source}:\n{text}\n\n"
    return combined

# Upload files in Sidebar
st.sidebar.title(':orange[Upload your MoM notes here:]')
st.sidebar.subheader("Upload Images, PDFs, and DOCX files")

# Allow multiple file uploads
user_files = st.sidebar.file_uploader("Upload your files", type=['pdf', 'docx', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)

extracted_texts = {}
ocr_comparison = {}

if user_files:
    for user_file in user_files:
        if user_file.type == 'application/pdf':
            text = text_extractor_pdf(user_file)
            extracted_texts[f"PDF ({user_file.name})"] = text
        elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            text = text_extractor_docx(user_file)
            extracted_texts[f"DOCX ({user_file.name})"] = text
        elif user_file.type in ['image/jpg','image/jpeg','image/png']:
            # Extract with Google AI
            google_text = extract_text_image(user_file)
            extracted_texts[f"Image Google AI ({user_file.name})"] = google_text

            # Extract with Tesseract for comparison
            image = Image.open(user_file)
            tesseract_text = extract_text_tesseract(image)
            ocr_comparison[user_file.name] = {
                'Google AI': google_text,
                'Tesseract': tesseract_text
            }

# Main page
st.title(':blue[Minutes Of Meeting] : :green[AI assisted MoM generator in a standardized form from meeting notes.]')

tips = '''Tips to use this app:
* Upload your meeting notes in the sidebar (Images, PDFs, or DOCX files)
* Choose from available options: Generate MOM, Summarize, Combine Texts, or Compare OCR
* Get standardized MOMs, summaries, or comparisons'''
st.write(tips)

# Options
col1, col2, col3, col4 = st.columns(4)

with col1:
    generate_mom = st.button('Generate MOM')

with col2:
    summarize = st.button('Summarize')

with col3:
    combine = st.button('Combine Texts')

with col4:
    compare_ocr = st.button('Compare OCR')

mom_prompt = '''Assume you are expert in creating minutes of meeting. User has provided
notes of meeting in text format. Using this data you need to create a standardized
minutes of meeting for the user.

Output must follow word/docx format, strictly in the following manner:
title : Title of meeting
Heading : Meeting Agenda
subheading : Name of attendees (If attendees name is not there keep it NA)
subheading : date of meeting and place of meeting (place means name of conference /meeting room if not provided keep it online)
Body: The body must follow the following sequence of points
* Key points discussed
* Highlight any decision that has been finalised.
* mention actionable items.
* Any additional notes.
* Any deadline that has been discussed.
* Any next meeting date that has been discussed.
* 2 to 3 line of summary.
* Use bullet points and highlight or bold important keywords such the context is clear.
* Generate the output in such a format that it can can be copied and paste in word and create pdf.'''

summary_prompt = "Summarize the following meeting notes in 2-3 sentences:"

if generate_mom:
    if not extracted_texts:
        st.error('No text extracted from uploaded files')
    else:
        with st.spinner('Generating MOM...'):
            # Use the first extracted text or combined if multiple
            if len(extracted_texts) == 1:
                meeting_notes = list(extracted_texts.values())[0]
            else:
                meeting_notes = combine_texts(extracted_texts)

            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[mom_prompt, meeting_notes]
            )
            mom_output = response.text

            st.subheader("Generated Minutes of Meeting:")
            st.write(mom_output)

            # Save to file
            filename = 'generated_mom.txt'
            with open(f'outputs/{filename}', 'w', encoding='utf-8') as f:
                f.write(mom_output)

            st.download_button(label='Download MOM',
                             data=mom_output,
                             file_name=filename,
                             mime='text/plain')

if summarize:
    if not extracted_texts:
        st.error('No text extracted from uploaded files')
    else:
        with st.spinner('Generating summary...'):
            # Use the first extracted text or combined if multiple
            if len(extracted_texts) == 1:
                meeting_notes = list(extracted_texts.values())[0]
            else:
                meeting_notes = combine_texts(extracted_texts)

            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[summary_prompt, meeting_notes]
            )
            summary_output = response.text

            st.subheader("Summary:")
            st.write(summary_output)

            # Save to file
            filename = 'summary.txt'
            with open(f'outputs/{filename}', 'w', encoding='utf-8') as f:
                f.write(summary_output)

            st.download_button(label='Download Summary',
                             data=summary_output,
                             file_name=filename,
                             mime='text/plain')

if combine:
    if not extracted_texts:
        st.error('No text extracted from uploaded files')
    else:
        combined_text = combine_texts(extracted_texts)

        st.subheader("Combined Text from all files:")
        st.text_area("Combined Text:", combined_text, height=300)

        # Save to file
        filename = 'combined_text.txt'
        with open(f'outputs/{filename}', 'w', encoding='utf-8') as f:
            f.write(combined_text)

        st.download_button(label='Download Combined Text',
                         data=combined_text,
                         file_name=filename,
                         mime='text/plain')

        # Option to generate MOM from combined text
        if st.button('Generate MOM from Combined Text'):
            with st.spinner('Generating MOM from combined text...'):
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=[mom_prompt, combined_text]
                )
                combined_mom = response.text

                st.subheader("MOM from Combined Text:")
                st.write(combined_mom)

                # Save to file
                mom_filename = 'combined_mom.txt'
                with open(f'outputs/{mom_filename}', 'w', encoding='utf-8') as f:
                    f.write(combined_mom)

                st.download_button(label='Download Combined MOM',
                                 data=combined_mom,
                                 file_name=mom_filename,
                                 mime='text/plain')

if compare_ocr:
    if not ocr_comparison:
        st.error('No image files uploaded for OCR comparison')
    else:
        st.subheader("OCR Comparison Results:")

        for filename, results in ocr_comparison.items():
            st.write(f"**File: {filename}**")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Tesseract Output:**")
                st.text_area(f"Tesseract - {filename}", results['Tesseract'], height=150, key=f"tess_{filename}")

            with col2:
                st.write("**Google AI Output:**")
                st.text_area(f"Google AI - {filename}", results['Google AI'], height=150, key=f"google_{filename}")

        # Save comparison to file
        comparison_text = ""
        for filename, results in ocr_comparison.items():
            comparison_text += f"File: {filename}\n\nTesseract Output:\n{results['Tesseract']}\n\nGoogle AI Output:\n{results['Google AI']}\n\n{'='*50}\n\n"

        filename = 'ocr_comparison.txt'
        with open(f'outputs/{filename}', 'w', encoding='utf-8') as f:
            f.write(comparison_text)

        st.download_button(label='Download OCR Comparison',
                         data=comparison_text,
                         file_name=filename,
                         mime='text/plain')

# Display extracted texts
if extracted_texts:
    st.subheader("Extracted Texts:")
    for source, text in extracted_texts.items():
        with st.expander(f"View {source}"):
            st.text_area(f"Text from {source}", text, height=200, key=f"extract_{source}")
