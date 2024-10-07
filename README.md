# 📄🚀 Resume & Job Offer Parser with ChatGPT

Welcome to Resume & Job Offer Parser, a Python tool that processes resumes and job offers in PDF format, extracts text, and uses ChatGPT to parse them into structured sections as per your custom prompt instructions! 🧠✨


# 📌 Features

- Extract Text from PDFs: use the PyMuPDF library to extract text from resumes and job offers

- AI-Powered Parsing: utilize ChatGPT API to parse extracted text into structured sections like Skills, Experience, Job requirements, Education, etc

- Token Usage Tracking: monitor your ChatGPT API usage by recording token consumption (completion, prompt, and total tokens)

- JSON Export: export the processed information into JSON files for further integration and analysis

- Highly Customizable: tailor the parsing through custom prompt instructions, making it flexible for various use cases


# 🛠️ How It Works

- PDF Processing: the tool reads PDF files (resumes and job offers) using the PyMuPDF library to extract their text content

- ChatGPT Parsing: the extracted text is then sent to ChatGPT, which parses it based on the prompt instructions provided

- Token Tracking: the script records the token usage for each ChatGPT API call, including completion tokens, prompt tokens, and total tokens.

- Structured Output: parsed information is exported into JSON files, organized into the specified sections


# 🚀 Quick Start

Follow these steps to get the project up and running:

1. Clone the Repository

git clone https://github.com/dsprovider/chatGPT-resume_joboffer_parser

cd chatGPT-resume_joboffer_parser

2. Install Dependencies

pip install -r requirements.txt

3. Run the Code

python jobResumeParser.py


# 📝 Example Usage

- Input: folder path containig your resumes or job offers in PDF format

- Processing: the text is extracted and sent to ChatGPT, which parses it into sections like Skills, Experience, Job requirements, Education, etc

- Token Tracking: the script logs token usage including completion tokens, prompt tokens, and total tokens

- Output: a JSON file is generated per resume / job offer with the parsed information


# 📚 Requirements

- Python 3.7+

- PyMuPDF for PDF text extraction

- OpenAI API for ChatGPT interactions

Enjoy parsing! 🎉✨
