# Setup Guide: Local Version (No API Key Required)

This version uses **Ollama** (free, local LLM) and **sentence-transformers** (local embeddings) - **no API key needed!**

## Step 1: Install Ollama

1. Download Ollama from: https://ollama.ai
2. Install and start Ollama
3. Download a model (choose one):
   ```bash
   ollama pull llama3.2
   ```
   Or try other models:
   ```bash
   ollama pull mistral
   ollama pull qwen2.5
   ollama pull phi3
   ```

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit
- LangChain
- Ollama integration
- Sentence transformers (for local embeddings)
- FAISS (for vector search)
- PyPDF (for PDF processing)

## Step 3: Run the Application

```bash
python -m streamlit run app.py
```

Or use the batch file:
```bash
run.bat
```

## How It Works

1. **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` (runs locally, free, no API)
2. **LLM**: Uses Ollama with your chosen model (runs locally, free, no API)
3. **Vector Store**: Uses FAISS (local file storage)

## Benefits

✅ **No API key required**
✅ **100% free** - runs entirely on your computer
✅ **Privacy** - your data never leaves your machine
✅ **Fast** after first setup (embeddings cached)

## Troubleshooting

**"Ollama not available" error:**
- Make sure Ollama is installed and running
- Check if you downloaded a model: `ollama list`
- Try: `ollama pull llama3.2` again

**Slow first run:**
- First time will download embedding model (~80MB)
- PDF indexing happens once, then cached
- Subsequent runs are much faster!

**Out of memory:**
- Try a smaller model: `ollama pull phi3` (3.8B parameters)
- Or use `mistral` which is efficient

## Model Recommendations

- **llama3.2** - Good balance (3B params, fast, quality)
- **mistral** - Very fast, good quality (7B params)
- **qwen2.5** - Great for technical content (7B params)
- **phi3** - Smallest, fastest (3.8B params)

