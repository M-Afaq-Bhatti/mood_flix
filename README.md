# mood_flix
# 🎬 Netflix AI Recommender

An intelligent Netflix recommendation system that suggests movies and TV shows based on your current emotional state. Built with Streamlit, Google Gemini AI, and ChromaDB vector search.

## ✨ Features

- 🎭 **Emotion-Based Recommendations**: 12 different emotional states to choose from
- 🧠 **AI-Powered**: Uses Google Gemini AI for personalized, contextual recommendations
- 🔍 **Semantic Search**: ChromaDB vector database for intelligent content matching
- 🎨 **Netflix-Style UI**: Professional, dark-themed interface with smooth animations
- 📊 **Database Statistics**: Real-time insights into your Netflix dataset
- 🚀 **Fast & Responsive**: Optimized caching and efficient processing

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS
- **AI Model**: Google Gemini 2.0 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Data Processing**: Pandas
- **Visualizations**: Plotly

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from Google AI Studio)
- Netflix dataset in CSV format

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Create project directory
mkdir netflix-chatbot
cd netflix-chatbot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key for the next step

### 3. Configure Environment

Create a `.env` file in the root directory:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Add Your Dataset

Place your `netflix_content.csv` file in the `data/` folder. The dataset should have these columns:
- `title`: Movie/show title
- `overview`: Plot description
- `category`: Movie or TV Show
- `genre`: Content genre
- `year`: Release year
- `rating`: Content rating

### 5. Run the Application

```bash
streamlit run app.py
```

The app will automatically:
- Load and clean your Netflix dataset
- Create embeddings for semantic search
- Initialize the ChromaDB vector database
- Launch the web interface

## 📁 Project Structure

```
netflix-chatbot/
├── app.py                    # Main Streamlit application
├── data_processor.py         # Data loading and ChromaDB setup
├── recommendation_engine.py  # RAG pipeline and Gemini integration
├── config.py                # Configuration and constants
├── requirements.txt          # Dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── data/
│   └── netflix_content.csv # Your Netflix dataset
└── database/
    └── (ChromaDB files)    # Auto-generated database files
```

## 🎭 Available Emotions

The system supports 12 different emotional states:

- 😊 **Happy**: Comedy and feel-good content
- 😢 **Sad**: Comforting and heartwarming stories
- 😡 **Angry**: Action-packed thrillers
- 😴 **Relaxed**: Calm documentaries and light romance
- 💪 **Motivated**: Inspirational biographical content
- 😱 **Excited**: Adventure and suspenseful thrillers
- 💔 **Heartbroken**: Romantic healing stories
- 🤔 **Thoughtful**: Deep documentaries and philosophy
- 😂 **Playful**: Fun animations and comedy
- 😌 **Peaceful**: Nature docs and slow-paced films
- 🔥 **Energetic**: High-energy action and adventure
- 🧠 **Curious**: Educational mysteries and documentaries

## ⚙️ Configuration

Edit `config.py` to customize:

- **Emotions and queries**: Modify `EMOTION_QUERIES` dictionary
- **Database settings**: Change `DB_PATH` and `COLLECTION_NAME`
- **Model settings**: Update `GEMINI_MODEL` and `EMBEDDING_MODEL`
- **UI styling**: Modify Netflix color scheme variables

## 🔧 Troubleshooting

### Common Issues

**Database initialization fails:**
- Ensure the `data/netflix_content.csv` file exists and has the required columns
- Check if the `database/` directory has write permissions

**Gemini API errors:**
- Verify your API key is correct in the `.env` file
- Check your API quota and usage limits
- Ensure you have an active internet connection

**Missing dependencies:**
- Run `pip install -r requirements.txt` to install all required packages
- For embedding model issues, try: `pip install sentence-transformers --upgrade`

### Performance Optimization

- **Large datasets**: Increase `BATCH_SIZE` in `config.py` for faster processing
- **Memory issues**: Reduce `n_results` parameter in recommendation queries
- **Slow startup**: The first run takes longer due to embedding model download

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Connect to Streamlit Cloud
3. Add your `GEMINI_API_KEY` in the secrets management
4. Deploy!

### Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language generation
- Streamlit for the amazing web app framework
- ChromaDB for efficient vector storage
- SentenceTransformers for semantic embeddings
- The open-source community for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information
4. Include error logs and system information

---

**Made with ❤️ for movie lovers everywhere!** 🍿