"""
Main Streamlit application for Netflix AI Recommendation Chatbot
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from data_processor import DataProcessor
from recommendation_engine import RecommendationEngine
from config import *


# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix-like styling with improved visibility
def load_css():
    st.markdown(f"""
    <style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {{
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background-color: transparent;
        color: #ffffff;
    }}
    
    /* Text color improvements */
    .stMarkdown, .stMarkdown > div, p {{
        color: #ffffff !important;
    }}
    
    .stSelectbox label, .stSelectbox > label {{
        color: #ffffff !important;
        font-weight: 500 !important;
    }}
    
    .stSelectbox > div > div {{
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(229, 9, 20, 0.3) !important;
        border-radius: 8px !important;
    }}
    
    .stSelectbox > div > div > div {{
        color: #ffffff !important;
    }}
    
    /* Netflix header */
    .netflix-header {{
        background: linear-gradient(135deg, {NETFLIX_RED} 0%, #cc0000 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(229, 9, 20, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .netflix-header h1 {{
        color: #ffffff !important;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
        font-family: 'Inter', sans-serif;
    }}
    
    .netflix-header p {{
        color: #f0f0f0 !important;
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        font-weight: 400;
    }}
    
    /* Emotion card styling */
    .emotion-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.08) 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(229, 9, 20, 0.2);
        backdrop-filter: blur(20px);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}
    
    .emotion-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(229, 9, 20, 0.25);
        border-color: rgba(229, 9, 20, 0.4);
    }}
    
    .emotion-card h2 {{
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }}
    
    .emotion-card p {{
        color: #e0e0e0 !important;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
    }}
    
    /* Recommendation box */
    .recommendation-box {{
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.15) 0%, rgba(0, 0, 0, 0.4) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(229, 9, 20, 0.4);
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
    }}
    
    .recommendation-box h2 {{
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}
    
    .recommendation-box div {{
        color: #f5f5f5 !important;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 400;
    }}
    
    /* Stats cards */
    .stats-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    .stats-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.2);
    }}
    
    .stats-card h3, .stats-card h4 {{
        color: #ffffff !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    .stats-card p {{
        color: #cccccc !important;
        font-size: 0.95rem;
        font-weight: 400;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {NETFLIX_RED} 0%, #cc0000 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 3rem !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 25px rgba(229, 9, 20, 0.4) !important;
        text-transform: none !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 35px rgba(229, 9, 20, 0.6) !important;
        background: linear-gradient(135deg, #ff0a1a 0%, #e60000 100%) !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: rgba(15, 15, 15, 0.95) !important;
    }}
    
    .sidebar .sidebar-content {{
        background-color: rgba(20, 20, 20, 0.95) !important;
    }}
    
    /* Sidebar text colors */
    .css-1d391kg .stMarkdown {{
        color: #ffffff !important;
    }}
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {{
        color: #ffffff !important;
    }}
    
    /* Info box styling */
    .stInfo {{
        background-color: rgba(229, 9, 20, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(229, 9, 20, 0.3) !important;
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    /* Spinner styling */
    .stSpinner > div {{
        border-top-color: {NETFLIX_RED} !important;
    }}
    
    /* Error and success message styling */
    .stError {{
        background-color: rgba(255, 67, 67, 0.1) !important;
        color: #ff6b6b !important;
        border: 1px solid rgba(255, 67, 67, 0.3) !important;
    }}
    
    .stSuccess {{
        background-color: rgba(76, 175, 80, 0.1) !important;
        color: #81c784 !important;
        border: 1px solid rgba(76, 175, 80, 0.3) !important;
    }}
    
    /* Pro tips box */
    .pro-tips-box {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }}
    
    .pro-tips-box h4 {{
        color: #ffffff !important;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}
    
    .pro-tips-box ul {{
        color: #e0e0e0 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    
    .pro-tips-box li {{
        color: #e0e0e0 !important;
        margin-bottom: 0.5rem;
    }}
    
    /* Footer styling */
    .footer-content {{
        text-align: center;
        padding: 2rem;
        color: #888888 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 3rem;
    }}
    
    .footer-content p {{
        color: #888888 !important;
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    .footer-content small {{
        color: #666666 !important;
        font-size: 0.85rem;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {NETFLIX_RED};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #cc0000;
    }}
    </style>
    """, unsafe_allow_html=True)


def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="netflix-header">
        <h1>🎬 Netflix AI Recommender</h1>
        <p>Discover your perfect watch based on your current mood</p>
    </div>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = None
    if 'recommendation_engine' not in st.session_state:
        st.session_state.recommendation_engine = None
    if 'database_ready' not in st.session_state:
        st.session_state.database_ready = False


def setup_database():
    """Setup database and recommendation engine"""
    if not st.session_state.database_ready:
        with st.spinner("🔄 Initializing Netflix recommendation system..."):
            # Initialize data processor
            data_processor = DataProcessor()
            
            # Setup database
            if data_processor.setup_database():
                st.session_state.data_processor = data_processor
                st.session_state.recommendation_engine = RecommendationEngine(
                    data_processor.get_collection()
                )
                st.session_state.database_ready = True
                return True
            else:
                st.error("❌ Failed to initialize the recommendation system")
                return False
    return True


def display_stats():
    """Display dataset statistics in sidebar"""
    if st.session_state.data_processor:
        stats = st.session_state.data_processor.get_stats()
        if stats:
            st.sidebar.markdown("### 📊 Database Stats")
            
            col1, col2 = st.sidebar.columns(2)
            with col1:
                st.sidebar.markdown(f"""
                <div class="stats-card">
                    <h3>{stats['total_items']}</h3>
                    <p>Total Items</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.sidebar.markdown(f"""
                <div class="stats-card">
                    <h3>{stats['genres']}</h3>
                    <p>Genres</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Movie vs Series chart
            if stats['movies'] > 0 or stats['series'] > 0:
                chart_data = pd.DataFrame({
                    'Type': ['Movies', 'Series'],
                    'Count': [stats['movies'], stats['series']]
                })
                
                fig = px.pie(
                    chart_data, 
                    values='Count', 
                    names='Type',
                    color_discrete_sequence=[NETFLIX_RED, '#B20710'],
                    title="Content Distribution"
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_size=16,
                    font_family="Inter"
                )
                st.sidebar.plotly_chart(fig, use_container_width=True)


def display_emotion_selector():
    """Display emotion selection interface"""
    st.markdown("""
    <div class="emotion-card">
        <h2>🎭 How are you feeling today?</h2>
        <p>Select your current mood and let me find the perfect content for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emotion dropdown
    selected_emotion = st.selectbox(
        "Choose your current emotion:",
        options=list(EMOTION_QUERIES.keys()),
        index=0,
        help="Select the emotion that best describes how you're feeling right now"
    )
    
    return selected_emotion


def display_recommendations(emotion, recommendations):
    """Display the AI-generated recommendations"""
    st.markdown(f"""
    <div class="recommendation-box">
        <h2>🎯 Perfect matches for your {emotion} mood!</h2>
        <div style="white-space: pre-wrap; line-height: 1.8; font-size: 1.1rem; color: #f5f5f5;">
        {recommendations}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_footer():
    """Display footer information"""
    st.markdown("---")
    st.markdown("""
    <div class="footer-content">
        <p>🤖 Powered by Google Gemini AI • 🎬 Netflix Dataset • ⚡ ChromaDB Vector Search</p>
        <p><small>Built with Streamlit • Made with ❤️ for movie lovers</small></p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Load custom CSS
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Setup database
    if not setup_database():
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎬 Navigation")
    st.sidebar.markdown("---")
    
    # Display stats
    display_stats()
    
    # About section in sidebar
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "This AI-powered recommendation system uses advanced semantic search "
        "to find Netflix content that matches your current emotional state. "
        "Just select your mood and get personalized recommendations!"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Emotion selector
        selected_emotion = display_emotion_selector()
        
        # Get recommendations button
        if st.button("🎯 Get My Perfect Recommendations", use_container_width=True):
            if st.session_state.recommendation_engine:
                with st.spinner(f"🔍 Finding perfect content for your {selected_emotion} mood..."):
                    recommendations = st.session_state.recommendation_engine.generate_emotion_based_recommendations(
                        selected_emotion
                    )
                    
                    if recommendations:
                        display_recommendations(selected_emotion, recommendations)
                    else:
                        st.error("Sorry, I couldn't generate recommendations at the moment. Please try again!")
            else:
                st.error("Recommendation system not ready. Please refresh the page.")
    
    with col2:
        # Current time and date
        current_time = datetime.now().strftime("%B %d, %Y\n%I:%M %p")
        st.markdown(f"""
        <div class="stats-card">
            <h4>🕐 Current Time</h4>
            <p>{current_time}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("""
        <div class="pro-tips-box">
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>🎭 Choose your emotion honestly for better recommendations</li>
                <li>🔄 Try different emotions to discover new content</li>
                <li>⭐ Each recommendation is personalized just for you</li>
                <li>🎬 Mix of movies and series based on your mood</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Emotion guide
        with st.expander("🎭 Emotion Guide"):
            st.markdown("""
            **😊 Happy**: Feel-good comedies and uplifting stories
            
            **😢 Sad**: Comforting and heartwarming content
            
            **😡 Angry**: Action-packed thrillers to release tension
            
            **😴 Relaxed**: Calm documentaries and light romance
            
            **💪 Motivated**: Inspirational and biographical content
            
            **😱 Excited**: Adventure and suspenseful thrillers
            
            **💔 Heartbroken**: Romantic healing stories
            
            **🤔 Thoughtful**: Deep documentaries and philosophy
            
            **😂 Playful**: Fun animations and comedy series
            
            **😌 Peaceful**: Nature docs and slow-paced films
            
            **🔥 Energetic**: High-energy action and adventure
            
            **🧠 Curious**: Educational mysteries and documentaries
            """)
    
    # Footer
    display_footer()


if __name__ == "__main__":
    main()