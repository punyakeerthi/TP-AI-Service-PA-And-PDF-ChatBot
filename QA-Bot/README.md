# PDF QA Bot

A powerful Question & Answer bot that uses **Streamlit**, **Google Gemini AI**, and **LangChain** to answer questions based on uploaded PDF documents.

## Features

- 📄 **PDF Upload**: Upload any PDF document
- 🤖 **AI-Powered Q&A**: Ask questions and get accurate answers using Google Gemini
- 🔍 **Smart Search**: Uses vector embeddings for relevant content retrieval
- 💬 **Chat Interface**: Interactive conversation history
- 🚀 **Easy to Use**: Clean Streamlit web interface

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## How to Use

1. **Upload PDF**: Use the sidebar to upload your PDF document
2. **Process Document**: Click "Process PDF" to analyze the document 
3. **Ask Questions**: Type your questions in the main interface
4. **Get Answers**: The bot will provide answers based on the PDF content
5. **View History**: Previous questions and answers are saved in the conversation history

## Example Questions

- "What is the main topic of this document?"
- "Can you summarize the key points?"
- "What does the document say about [specific topic]?"
- "Who are the authors mentioned?"
- "What conclusions are drawn?"

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini Pro
- **Document Processing**: LangChain
- **PDF Parsing**: PyPDF2
- **Vector Database**: FAISS
- **Embeddings**: Google Generative AI Embeddings

## File Structure

```
QA-Bot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Limitations

- Only supports PDF files
- Answers are limited to content within the uploaded PDF
- Large PDFs may take longer to process
- Requires internet connection for Google Gemini API

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Make sure your Google API key is correctly set in the `.env` file
   - Ensure the API key has proper permissions

2. **PDF Processing Error**
   - Check if the PDF is not password protected
   - Ensure the PDF contains extractable text (not just images)

3. **Dependencies Error**
   - Run `pip install -r requirements.txt` again
   - Try creating a virtual environment

### Need Help?

If you encounter any issues:
1. Check the error messages in the Streamlit interface
2. Verify your API key is working
3. Ensure all dependencies are installed correctly

## Future Enhancements

- Support for multiple file formats (DOCX, TXT)
- Conversation memory across sessions
- Document comparison features
- Export conversation history
- Multiple language support