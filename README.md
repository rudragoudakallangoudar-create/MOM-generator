# MOM Generator 🤖

AI-powered Minutes of Meeting (MOM) generator that extracts text from images, PDFs, and DOCX files to create standardized meeting minutes.

## 🌟 Features

- **Multi-format Text Extraction**: Extract text from Images, PDFs, and DOCX files
- **Advanced OCR**: Compare Tesseract and Google AI OCR methods
- **AI-Powered MOM Generation**: Create standardized meeting minutes using Google Gemini AI
- **Text Summarization**: Generate concise summaries of meeting notes
- **Multi-file Processing**: Combine and process multiple documents
- **Web Interface**: User-friendly Streamlit web application
- **File Download**: Download generated MOMs and summaries

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google AI API key (for OCR and MOM generation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/MOM-generator.git
cd MOM-generator
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google AI API key:
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_api_key_here
```

### Usage

#### Web Application
```bash
streamlit run webapp.py
```

#### Jupyter Notebook
Open `Loadig text.ipynb` for development and testing.

## 📁 Project Structure

```
MOM-generator/
├── webapp.py                 # Streamlit web application
├── Loadig text.ipynb         # Jupyter notebook for development
├── imageextractor.py         # Image text extraction module
├── pdfextractor.py           # PDF text extraction module
├── docxextractor.py          # DOCX text extraction module
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore file
└── outputs/                  # Generated files directory
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google AI API key for text processing and MOM generation

### Supported File Formats
- **Images**: PNG, JPG, JPEG
- **Documents**: PDF, DOCX
- **OCR Methods**: Tesseract OCR, Google AI Vision

## 🎯 Features in Detail

### Text Extraction
- **Images**: Uses OpenCV preprocessing + Google AI for accurate OCR
- **PDFs**: Extracts text using pypdf library
- **DOCX**: Parses Word documents using python-docx

### MOM Generation
Creates standardized minutes of meeting with:
- Meeting title and agenda
- Attendees and location
- Key points discussed
- Decisions made
- Actionable items
- Deadlines and next meetings
- Summary

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google AI for providing the Gemini API
- Tesseract OCR for open-source OCR capabilities
- Streamlit for the web application framework

---

## 🚀 Deployment

### Streamlit Cloud Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `webapp.py`
5. Add secret: `GOOGLE_API_KEY = "your_api_key_here"`
6. Deploy!

**Live App**: [Deploy your own instance](#deployment)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google AI for providing the Gemini API
- Tesseract OCR for open-source OCR capabilities
- Streamlit for the web application framework

---

## 🚀 Deployment

### Streamlit Cloud Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select this repository: `rudragoudakallangoudar-create/MOM-generator`
4. Set main file path: `webapp.py`
5. Add secret: `GOOGLE_API_KEY = "your_api_key_here"`
6. Deploy!

**Live App**: [Deploy your own instance](#deployment)



