import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="PriceHunter - Compare & Save",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern e-commerce vibe
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .price-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
        border: 2px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    
    .price-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    }
    
    .best-price {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border: 3px solid #11998e;
        position: relative;
    }
    
    .best-price::before {
        content: "🏆 BEST PRICE";
        position: absolute;
        top: -12px;
        right: 20px;
        background: #ffd700;
        color: #333;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
    }
    
    .platform-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 8px;
    }
    
    .amazon { background: #ff9900; color: white; }
    .flipkart { background: #2874f0; color: white; }
    .myntra { background: #ff3f6c; color: white; }
    .ebay { background: #e53238; color: white; }
    .walmart { background: #0071ce; color: white; }
    
    .price-text {
        font-size: 2rem;
        font-weight: 700;
        color: #11998e;
        margin: 0.5rem 0;
    }
    
    .best-price .price-text {
        color: white;
    }
    
    .savings-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stSelectbox {
        background: white;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    div[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #666;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Mock product database
PRODUCTS_DB = {
    "Electronics": [
        {"name": "iPhone 15 Pro Max 256GB","prices": {"Amazon": 144900,"Flipkart": 147999,"Myntra": None,"eBay": 149999,"Walmart": 142999},"image": "📱","rating": 4.7},
        {"name": "Samsung Galaxy S24 Ultra","prices": {"Amazon": 129999,"Flipkart": 126999,"Myntra": None,"eBay": 134999,"Walmart": 128999},"image": "📱","rating": 4.6},
        {"name": "Sony WH-1000XM5 Headphones","prices": {"Amazon": 29990,"Flipkart": 31999,"Myntra": None,"eBay": 32999,"Walmart": 28999},"image": "🎧","rating": 4.8},
        {"name": "MacBook Air M3 13-inch","prices": {"Amazon": 114900,"Flipkart": 119900,"Myntra": None,"eBay": 121900,"Walmart": 112900},"image": "💻","rating": 4.9},
        {"name": "iPad Pro 12.9 inch M2","prices": {"Amazon": 109900,"Flipkart": 112900,"Myntra": None,"eBay": 114900,"Walmart": 107900},"image": "📱","rating": 4.7}
    ],
    "Fashion": [
        {"name": "Nike Air Max 270","prices": {"Amazon": 12995,"Flipkart": 11999,"Myntra": 12495,"eBay": 13995,"Walmart": 11499},"image": "👟","rating": 4.5},
        {"name": "Levi's 501 Original Jeans","prices": {"Amazon": 3999,"Flipkart": 3799,"Myntra": 3499,"eBay": 4299,"Walmart": 3899},"image": "👖","rating": 4.6},
        {"name": "Ray-Ban Aviator Sunglasses","prices": {"Amazon": 8990,"Flipkart": 9499,"Myntra": 8499,"eBay": 9990,"Walmart": 8799},"image": "🕶️","rating": 4.7},
        {"name": "Tommy Hilfiger Polo Shirt","prices": {"Amazon": 2999,"Flipkart": 2799,"Myntra": 2499,"eBay": 3299,"Walmart": 2699},"image": "👕","rating": 4.4}
    ],
    "Home & Kitchen": [
        {"name": "Dyson V15 Detect Vacuum","prices": {"Amazon": 59900,"Flipkart": 62999,"Myntra": None,"eBay": 64999,"Walmart": 57999},"image": "🧹","rating": 4.8},
        {"name": "Instant Pot Duo 7-in-1","prices": {"Amazon": 8999,"Flipkart": 9499,"Myntra": None,"eBay": 9999,"Walmart": 8499},"image": "🍳","rating": 4.7},
        {"name": "Philips Air Fryer XXL","prices": {"Amazon": 18999,"Flipkart": 19999,"Myntra": None,"eBay": 20999,"Walmart": 17999},"image": "🍟","rating": 4.6}
    ],
    "Books": [
        {"name": "Atomic Habits by James Clear","prices": {"Amazon": 599,"Flipkart": 549,"Myntra": None,"eBay": 699,"Walmart": 579},"image": "📚","rating": 4.9},
        {"name": "The Psychology of Money","prices": {"Amazon": 399,"Flipkart": 379,"Myntra": None,"eBay": 449,"Walmart": 389},"image": "📖","rating": 4.8}
    ],
    "Sports": [
        {"name": "Yonex Badminton Racket","prices": {"Amazon": 3499,"Flipkart": 3299,"Myntra": 3599,"eBay": 3799,"Walmart": 3199},"image": "🏸","rating": 4.5},
        {"name": "Adidas Football Size 5","prices": {"Amazon": 1499,"Flipkart": 1399,"Myntra": 1599,"eBay": 1699,"Walmart": 1349},"image": "⚽","rating": 4.4}
    ]
}

def find_best_price(prices):
    available_prices = {k: v for k, v in prices.items() if v is not None}
    if not available_prices:
        return None, None
    best_platform = min(available_prices, key=available_prices.get)
    return best_platform, available_prices[best_platform]

def calculate_savings(current_price, best_price):
    if current_price is None or best_price is None:
        return 0
    return current_price - best_price

st.markdown("""
    <div class="main-header">
        <h1>🛒 PriceHunter</h1>
        <p>Compare prices across multiple platforms and save big!</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    categories = ["All Categories"] + list(PRODUCTS_DB.keys())
    selected_category = st.selectbox("Category", categories)
    search_query = st.text_input("Search Product")

filtered_products = []
for category, products in PRODUCTS_DB.items():
    for product in products:
        filtered_products.append({**product, "category": category})

if search_query:
    filtered_products = [p for p in filtered_products if search_query.lower() in p["name"].lower()]

for product in filtered_products:
    st.write(product["name"])
