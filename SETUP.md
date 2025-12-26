# Setup Instructions for Vellicate Agent

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or run the setup script:
   ```bash
   setup.bat
   ```

2. **Configure API Key**
   - Open the `.env` file in the project root
   - Replace `your_api_key_here` with your actual Gemini API key
   - Get your API key from: https://aistudio.google.com/app/apikey
   
   Example `.env` file:
   ```
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Use the Application**
   - The app will open in your browser (usually at http://localhost:8501)
   - If you've set up the `.env` file, your API key will be pre-loaded
   - Click "Initialize Agent" to load and index the PDF
   - Start asking questions about the PDF content!

## Project Structure

```
vellicate_agent/
├── app.py                 # Streamlit web interface
├── rag_logic.py           # RAG chain logic
├── requirements.txt       # Python dependencies
├── .env                   # API key configuration (create this)
├── .gitignore            # Git ignore rules
├── setup.bat             # Windows setup script
└── complete data.pdf  # PDF document
```

## Troubleshooting

- **Module not found errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
- **API key errors**: Verify your `.env` file has the correct format: `GEMINI_API_KEY=your_key_here`
- **PDF not found**: Ensure `complete data.pdf` is in the project root directory

