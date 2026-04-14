"\"\"\"
E-Commerce Price Comparison Application
A full-stack Streamlit app for comparing product prices across multiple platforms
\"\"\"

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
from typing import List, Dict, Optional
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================

# Try to load API keys from Streamlit secrets (for deployment)
try:
    API_KEYS = {
        'amazon': st.secrets.get('AMAZON_API_KEY', ''),
        'flipkart': st.secrets.get('FLIPKART_API_KEY', ''),
        'myntra': st.secrets.get('MYNTRA_API_KEY', ''),
        'ebay': st.secrets.get('EBAY_API_KEY', ''),
        'walmart': st.secrets.get('WALMART_API_KEY', ''),
    }
except:
    # Fallback for local development
    API_KEYS = {
        'amazon': '',
        'flipkart': '',
        'myntra': '',
        'ebay': '',
        'walmart': '',
    }

# Platform configurations
PLATFORMS = {
    'Amazon': {'color': '#FF9900', 'icon': '📦'},
    'Flipkart': {'color': '#2874F0', 'icon': '🛒'},
    'Myntra': {'color': '#FF3F6C', 'icon': '👗'},
    'eBay': {'color': '#E53238', 'icon': '🏪'},
    'Walmart': {'color': '#0071CE', 'icon': '🏬'}
}

CATEGORIES = [
    \"All Categories\",
    \"Electronics\",
    \"Clothing & Fashion\",
    \"Home & Kitchen\",
    \"Books & Media\",
    \"Sports & Fitness\",
    \"Beauty & Personal Care\",
    \"Toys & Games\",
    \"Automotive\",
    \"Furniture\",
    \"Mobile & Accessories\"
]

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=\"Price Comparison - Find Best Deals\",
    page_icon=\"🛍️\",
    layout=\"wide\",
    initial_sidebar_state=\"expanded\"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown(\"\"\"
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Work+Sans:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Manrope', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Work Sans', sans-serif;
        font-weight: 700;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Product Card Styling */
    .product-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #f0f2f6;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        border-color: #667eea;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Price tag styling */
    .price-tag {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        margin: 1rem 0;
    }
    
    .price-tag-best {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .old-price {
        text-decoration: line-through;
        color: #999;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    /* Discount badge */
    .discount-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
    }
    
    /* Platform badge */
    .platform-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.5rem 0.5rem 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Rating stars */
    .rating {
        color: #FFA500;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* View button */
    .view-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.7rem 1.8rem;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .view-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5);
        text-decoration: none;
        color: white;
    }
    
    /* Availability badge */
    .in-stock {
        color: #10b981;
        font-weight: 600;
        background: #d1fae5;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
    }
    
    .out-of-stock {
        color: #ef4444;
        font-weight: 600;
        background: #fee2e2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
    }
    
    /* Filter section */
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Loading animation */
    .loading-text {
        text-align: center;
        font-size: 1.2rem;
        color: #667eea;
        font-weight: 600;
    }
    
    /* Comparison table */
    .comparison-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 700;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)

# ============================================================================
# MOCK DATA GENERATION (Replace with real API calls)
# ============================================================================

def generate_mock_products(query: str, category: str, min_price: float, max_price: float, platforms: List[str]) -> List[Dict]:
    \"\"\"
    Generate realistic mock product data for demonstration.
    In production, replace this with actual API calls to e-commerce platforms.
    \"\"\"
    
    # Sample product templates based on common searches
    product_templates = {
        \"laptop\": [
            \"Dell Inspiron 15 3000 Series Laptop\",
            \"HP Pavilion Gaming Laptop 15-DK\",
            \"Lenovo IdeaPad Slim 3 Laptop\",
            \"ASUS VivoBook 15 Thin and Light Laptop\",
            \"Acer Aspire 5 Slim Laptop\",
            \"MacBook Air M2 13-inch Laptop\",
            \"MSI GF63 Thin Gaming Laptop\"
        ],
        \"phone\": [
            \"Samsung Galaxy S24 5G Smartphone\",
            \"iPhone 15 Pro Max 256GB\",
            \"OnePlus 12R 5G Mobile Phone\",
            \"Google Pixel 8 Pro Smartphone\",
            \"Xiaomi Redmi Note 13 Pro\",
            \"OPPO Reno 11 5G Smartphone\",
            \"Motorola Edge 40 Neo 5G\"
        ],
        \"headphone\": [
            \"Sony WH-1000XM5 Wireless Headphones\",
            \"Bose QuietComfort 45 Bluetooth Headphones\",
            \"Apple AirPods Pro (2nd Generation)\",
            \"JBL Tune 760NC Wireless Headphones\",
            \"Sennheiser HD 450BT Bluetooth Headphones\",
            \"boAt Rockerz 550 Wireless Headphones\"
        ],
        \"watch\": [
            \"Apple Watch Series 9 GPS Smartwatch\",
            \"Samsung Galaxy Watch 6 Classic\",
            \"Fitbit Versa 4 Fitness Smartwatch\",
            \"Amazfit GTR 4 Smart Watch\",
            \"Noise ColorFit Pro 4 Alpha Smartwatch\",
            \"Fire-Boltt Phoenix Pro Smartwatch\"
        ],
        \"shoe\": [
            \"Nike Air Max 270 Running Shoes\",
            \"Adidas Ultraboost 22 Running Shoes\",
            \"Puma RS-X3 Puzzle Sneakers\",
            \"Reebok Zig Kinetica II Running Shoes\",
            \"New Balance 574 Core Sneakers\",
            \"Skechers Go Walk 6 Walking Shoes\"
        ],
        \"shirt\": [
            \"Levi's Men's Regular Fit Casual Shirt\",
            \"Allen Solly Men's Slim Fit Formal Shirt\",
            \"Van Heusen Men's Solid Regular Fit Shirt\",
            \"US Polo Assn. Men's Checkered Casual Shirt\",
            \"Peter England Men's Slim Fit Shirt\",
            \"Arrow Men's Formal Regular Fit Shirt\"
        ],
        \"tv\": [
            \"Samsung 55-inch Crystal 4K UHD Smart TV\",
            \"LG 43-inch Full HD Smart LED TV\",
            \"Sony Bravia 55-inch 4K Ultra HD Smart TV\",
            \"Mi 50-inch 4K Ultra HD Android TV\",
            \"OnePlus 55-inch U Series 4K Smart TV\",
            \"TCL 43-inch Full HD Smart Android TV\"
        ],
        \"default\": [
            f\"{query.title()} Premium Edition\",
            f\"{query.title()} Pro Model\",
            f\"{query.title()} Essential Version\",
            f\"{query.title()} Standard Series\",
            f\"{query.title()} Advanced Model\"
        ]
    }
    
    # Find matching template
    query_lower = query.lower()
    products_list = product_templates.get(\"default\", [])
    for key in product_templates.keys():
        if key in query_lower or query_lower in key:
            products_list = product_templates[key]
            break
    
    # Generate products for each platform
    mock_products = []
    base_price = (min_price + max_price) / 2 if max_price > min_price else 500
    
    for platform in platforms:
        num_products = random.randint(3, 6)  # Each platform returns 3-6 products
        
        for i in range(min(num_products, len(products_list))):
            # Generate price with some variation
            price_variation = random.uniform(0.7, 1.3)
            price = round(base_price * price_variation, 2)
            
            # Ensure price is within range
            if price < min_price or price > max_price:
                price = round(random.uniform(min_price, max_price), 2)
            
            # Generate discount
            has_discount = random.random() > 0.4
            original_price = round(price * random.uniform(1.1, 1.5), 2) if has_discount else price
            discount_percent = round(((original_price - price) / original_price) * 100) if has_discount else 0
            
            # Generate rating
            rating = round(random.uniform(3.5, 5.0), 1)
            reviews = random.randint(50, 5000)
            
            # Availability
            in_stock = random.random() > 0.15  # 85% in stock
            
            product = {
                'platform': platform,
                'title': products_list[i],
                'price': price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'category': category if category != \"All Categories\" else random.choice(CATEGORIES[1:]),
                'rating': rating,
                'reviews': reviews,
                'in_stock': in_stock,
                'url': f\"https://{platform.lower()}.com/product/{random.randint(10000, 99999)}\"
            }
            
            mock_products.append(product)
    
    return mock_products

# ============================================================================
# REAL API INTEGRATION FUNCTIONS (To be implemented)
# ============================================================================

def search_amazon(query: str, category: str, min_price: float, max_price: float) -> List[Dict]:
    \"\"\"
    Search products on Amazon using Amazon Product Advertising API.
    Replace this with actual API implementation.
    \"\"\"
    # TODO: Implement Amazon PA-API integration
    # API Documentation: https://webservices.amazon.com/paapi5/documentation/
    return []

def search_flipkart(query: str, category: str, min_price: float, max_price: float) -> List[Dict]:
    \"\"\"
    Search products on Flipkart using Flipkart Marketplace API.
    Replace this with actual API implementation.
    \"\"\"
    # TODO: Implement Flipkart API integration
    # API Documentation: https://seller.flipkart.com/api-docs/
    return []

def search_walmart(query: str, category: str, min_price: float, max_price: float) -> List[Dict]:
    \"\"\"
    Search products on Walmart using Walmart Marketplace API.
    Replace this with actual API implementation.
    \"\"\"
    # TODO: Implement Walmart API integration
    # API Documentation: https://developer.walmart.com/
    return []

def search_ebay(query: str, category: str, min_price: float, max_price: float) -> List[Dict]:
    \"\"\"
    Search products on eBay using eBay Finding API.
    Replace this with actual API implementation.
    \"\"\"
    # TODO: Implement eBay API integration
    # API Documentation: https://developer.ebay.com/
    return []

def search_myntra(query: str, category: str, min_price: float, max_price: float) -> List[Dict]:
    \"\"\"
    Search products on Myntra using Myntra API.
    Replace this with actual API implementation.
    \"\"\"
    # TODO: Implement Myntra API integration
    return []

# ============================================================================
# MAIN SEARCH FUNCTION
# ============================================================================

def search_all_platforms(query: str, category: str, min_price: float, max_price: float, platforms: List[str]) -> List[Dict]:
    \"\"\"
    Search across all selected platforms and aggregate results.
    Currently uses mock data. Replace with real API calls.
    \"\"\"
    
    all_products = []
    
    # For demonstration, using mock data
    # In production, call respective platform APIs based on selected platforms
    
    use_mock_data = True  # Set to False when implementing real APIs
    
    if use_mock_data:
        all_products = generate_mock_products(query, category, min_price, max_price, platforms)
    else:
        # Real API calls (implement when you have API keys)
        if 'Amazon' in platforms:
            all_products.extend(search_amazon(query, category, min_price, max_price))
        
        if 'Flipkart' in platforms:
            all_products.extend(search_flipkart(query, category, min_price, max_price))
        
        if 'Walmart' in platforms:
            all_products.extend(search_walmart(query, category, min_price, max_price))
        
        if 'eBay' in platforms:
            all_products.extend(search_ebay(query, category, min_price, max_price))
        
        if 'Myntra' in platforms:
            all_products.extend(search_myntra(query, category, min_price, max_price))
    
    return all_products

# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_header():
    \"\"\"Display the main header\"\"\"
    st.markdown(\"\"\"
        <div class=\"main-header\">
            <h1>🛍️ Smart Price Comparison</h1>
            <p>Compare prices across Amazon, Flipkart, Myntra, eBay & Walmart - Find the best deals instantly!</p>
        </div>
    \"\"\", unsafe_allow_html=True)

def display_product_card(product: Dict, is_best_price: bool = False):
    \"\"\"Display a single product card\"\"\"
    
    platform = product['platform']
    platform_config = PLATFORMS.get(platform, {'color': '#666', 'icon': '🏪'})
    
    # Card HTML
    st.markdown(f\"\"\"
        <div class=\"product-card\">
            <div style=\"display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;\">
                <div style=\"flex: 1;\">
                    <span class=\"platform-badge\" style=\"background: {platform_config['color']}; color: white;\">
                        {platform_config['icon']} {platform}
                    </span>
                    <h3 style=\"margin: 0.8rem 0 0.5rem 0; font-size: 1.3rem; color: #1a1a1a;\">
                        {product['title']}
                    </h3>
                    <div style=\"color: #666; font-size: 0.95rem; margin: 0.5rem 0;\">
                        📂 {product['category']}
                    </div>
                </div>
            </div>
            
            <div style=\"display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;\">
                <div style=\"flex: 1; min-width: 200px;\">
                    <div class=\"rating\">
                        {'⭐' * int(product['rating'])}{'☆' * (5 - int(product['rating']))} 
                        {product['rating']} ({product['reviews']:,} reviews)
                    </div>
                    <div style=\"margin: 0.5rem 0;\">
                        <span class=\"{'in-stock' if product['in_stock'] else 'out-of-stock'}\">
                            {'✓ In Stock' if product['in_stock'] else '✗ Out of Stock'}
                        </span>
                    </div>
                </div>
                
                <div style=\"text-align: right;\">
                    <div class=\"price-tag {'price-tag-best' if is_best_price else ''}\">
                        ${product['price']:.2f}
                    </div>
                    {f'''
                    <div style=\"margin: 0.5rem 0;\">
                        <span class=\"old-price\">${product['original_price']:.2f}</span>
                        <span class=\"discount-badge\">Save {product['discount_percent']:.0f}%</span>
                    </div>
                    ''' if product['discount_percent'] > 0 else ''}
                    <a href=\"{product['url']}\" target=\"_blank\" class=\"view-button\">
                        View on {platform} →
                    </a>
                </div>
            </div>
            
            {f'<div style=\"margin-top: 1rem; padding: 0.8rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 10px; text-align: center; font-weight: 700; font-size: 1.1rem;\">🏆 BEST PRICE FOUND!</div>' if is_best_price else ''}
        </div>
    \"\"\", unsafe_allow_html=True)

def display_price_comparison_chart(products: List[Dict]):
    \"\"\"Display price comparison chart\"\"\"
    
    if not products:
        return
    
    # Prepare data for chart
    df = pd.DataFrame(products)
    
    # Group by platform and get average price
    platform_avg = df.groupby('platform')['price'].mean().reset_index()
    platform_avg = platform_avg.sort_values('price')
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=platform_avg['platform'],
            y=platform_avg['price'],
            marker=dict(
                color=[PLATFORMS[p]['color'] for p in platform_avg['platform']],
                line=dict(color='white', width=2)
            ),
            text=[f'${p:.2f}' for p in platform_avg['price']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Average Price: $%{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=\"Average Price Comparison by Platform\",
        xaxis_title=\"Platform\",
        yaxis_title=\"Average Price ($)\",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=\"Manrope, sans-serif\", size=14),
        title_font=dict(size=20, family=\"Work Sans, sans-serif\", color='#1a1a1a'),
        showlegend=False,
        margin=dict(t=80, b=60, l=60, r=40)
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)

def display_stats(products: List[Dict], response_time: float):
    \"\"\"Display search statistics\"\"\"
    
    if not products:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f\"\"\"
            <div class=\"stat-card\">
                <div class=\"stat-number\">{len(products)}</div>
                <div class=\"stat-label\">Products Found</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    
    with col2:
        platforms_count = len(set(p['platform'] for p in products))
        st.markdown(f\"\"\"
            <div class=\"stat-card\" style=\"background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);\">
                <div class=\"stat-number\">{platforms_count}</div>
                <div class=\"stat-label\">Platforms</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    
    with col3:
        min_price = min(p['price'] for p in products)
        st.markdown(f\"\"\"
            <div class=\"stat-card\" style=\"background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);\">
                <div class=\"stat-number\">${min_price:.2f}</div>
                <div class=\"stat-label\">Best Price</div>
            </div>
        \"\"\", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f\"\"\"
            <div class=\"stat-card\" style=\"background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);\">
                <div class=\"stat-number\">{response_time:.1f}s</div>
                <div class=\"stat-label\">Search Time</div>
            </div>
        \"\"\", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    \"\"\"Main application logic\"\"\"
    
    # Display header
    display_header()
    
    # Initialize session state
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'last_search_time' not in st.session_state:
        st.session_state.last_search_time = None
    
    # Sidebar filters
    with st.sidebar:
        st.markdown(\"### 🔍 Search Filters\")
        
        # Product search
        search_query = st.text_input(
            \"Product Name\",
            placeholder=\"e.g., laptop, phone, headphones...\",
            help=\"Enter the product you want to search for\"
        )
        
        # Category filter
        category = st.selectbox(
            \"Category\",
            options=CATEGORIES,
            help=\"Filter by product category\"
        )
        
        # Price range
        st.markdown(\"#### 💰 Price Range\")
        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input(
                \"Min ($)\",
                min_value=0.0,
                value=0.0,
                step=50.0
            )
        with col2:
            max_price = st.number_input(
                \"Max ($)\",
                min_value=0.0,
                value=5000.0,
                step=100.0
            )
        
        # Platform selection
        st.markdown(\"#### 🏪 Platforms\")
        platforms = st.multiselect(
            \"Select platforms to search\",
            options=list(PLATFORMS.keys()),
            default=list(PLATFORMS.keys()),
            help=\"Choose which e-commerce platforms to compare\"
        )
        
        # Search button
        st.markdown(\"<br>\", unsafe_allow_html=True)
        search_button = st.button(\"🔎 Search Products\", use_container_width=True, type=\"primary\")
        
        # Info section
        st.markdown(\"---\")
        st.markdown(\"\"\"
            <div style=\"background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; font-size: 0.85rem;\">
                <strong>💡 Tips:</strong><br>
                • Try searching: laptop, phone, shoes<br>
                • Adjust price range for better results<br>
                • Select multiple platforms to compare
            </div>
        \"\"\", unsafe_allow_html=True)
    
    # Main content area
    if search_button:
        # Validation
        if not search_query:
            st.error(\"⚠️ Please enter a product name to search\")
            return
        
        if not platforms:
            st.error(\"⚠️ Please select at least one platform\")
            return
        
        if min_price >= max_price:
            st.error(\"⚠️ Maximum price must be greater than minimum price\")
            return
        
        # Perform search
        with st.spinner(\"🔄 Searching across platforms... Please wait\"):
            start_time = time.time()
            
            # Simulate API delay for realism
            time.sleep(1.5)
            
            # Search products
            results = search_all_platforms(
                query=search_query,
                category=category,
                min_price=min_price,
                max_price=max_price,
                platforms=platforms
            )
            
            search_time = time.time() - start_time
            
            # Store in session state
            st.session_state.search_results = results
            st.session_state.last_search_time = search_time
    
    # Display results
    if st.session_state.search_results is not None:
        results = st.session_state.search_results
        search_time = st.session_state.last_search_time
        
        if len(results) == 0:
            st.info(\"📭 No products found. Try adjusting your search criteria or price range.\")
            return
        
        # Display statistics
        display_stats(results, search_time)
        
        st.markdown(\"<br>\", unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs([\"📋 All Products\", \"📊 Price Comparison\", \"📈 Analytics\"])
        
        with tab1:
            st.markdown(\"### All Products\")
            
            # Sorting options
            col1, col2 = st.columns([3, 1])
            with col1:
                sort_by = st.selectbox(
                    \"Sort by\",
                    options=[\"Price: Low to High\", \"Price: High to Low\", \"Rating\", \"Discount\", \"Platform\"],
                    key=\"sort_products\"
                )
            
            with col2:
                show_stock_only = st.checkbox(\"In Stock Only\", value=False)
            
            # Filter and sort products
            filtered_products = results
            if show_stock_only:
                filtered_products = [p for p in filtered_products if p['in_stock']]
            
            # Sort products
            if sort_by == \"Price: Low to High\":
                filtered_products = sorted(filtered_products, key=lambda x: x['price'])
            elif sort_by == \"Price: High to Low\":
                filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
            elif sort_by == \"Rating\":
                filtered_products = sorted(filtered_products, key=lambda x: x['rating'], reverse=True)
            elif sort_by == \"Discount\":
                filtered_products = sorted(filtered_products, key=lambda x: x['discount_percent'], reverse=True)
            elif sort_by == \"Platform\":
                filtered_products = sorted(filtered_products, key=lambda x: x['platform'])
            
            # Find best price
            best_price = min(p['price'] for p in filtered_products) if filtered_products else 0
            
            # Display products
            for product in filtered_products:
                is_best = product['price'] == best_price
                display_product_card(product, is_best)
        
        with tab2:
            st.markdown(\"### Price Comparison by Platform\")
            display_price_comparison_chart(results)
            
            # Price distribution
            st.markdown(\"#### Price Distribution\")
            df = pd.DataFrame(results)
            
            fig = px.box(
                df,
                x='platform',
                y='price',
                color='platform',
                color_discrete_map={p: PLATFORMS[p]['color'] for p in PLATFORMS.keys()},
                title=\"Price Range by Platform\"
            )
            
            fig.update_layout(
                showlegend=False,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family=\"Manrope, sans-serif\")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown(\"### Analytics & Insights\")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Platform distribution
                st.markdown(\"#### Products per Platform\")
                platform_counts = pd.DataFrame(results)['platform'].value_counts().reset_index()
                platform_counts.columns = ['Platform', 'Count']
                
                fig = px.pie(
                    platform_counts,
                    values='Count',
                    names='Platform',
                    color='Platform',
                    color_discrete_map={p: PLATFORMS[p]['color'] for p in PLATFORMS.keys()},
                    hole=0.4
                )
                
                fig.update_layout(
                    height=350,
                    font=dict(family=\"Manrope, sans-serif\")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Rating distribution
                st.markdown(\"#### Average Rating by Platform\")
                df = pd.DataFrame(results)
                rating_avg = df.groupby('platform')['rating'].mean().reset_index()
                
                fig = px.bar(
                    rating_avg,
                    x='platform',
                    y='rating',
                    color='platform',
                    color_discrete_map={p: PLATFORMS[p]['color'] for p in PLATFORMS.keys()},
                    text='rating'
                )
                
                fig.update_traces(texttemplate='%{text:.1f}⭐', textposition='outside')
                fig.update_layout(
                    showlegend=False,
                    height=350,
                    yaxis_range=[0, 5],
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family=\"Manrope, sans-serif\")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Summary table
            st.markdown(\"#### Platform Summary\")
            df = pd.DataFrame(results)
            summary = df.groupby('platform').agg({
                'price': ['min', 'max', 'mean'],
                'rating': 'mean',
                'in_stock': lambda x: (x.sum() / len(x) * 100)
            }).round(2)
            
            summary.columns = ['Min Price ($)', 'Max Price ($)', 'Avg Price ($)', 'Avg Rating', 'Stock Availability (%)']
            summary = summary.reset_index()
            
            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True
            )
    
    else:
        # Welcome screen when no search has been performed
        st.markdown(\"\"\"
            <div style=\"text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 20px; margin: 2rem 0;\">
                <h2 style=\"color: #667eea; margin-bottom: 1rem;\">👋 Welcome to Smart Price Comparison!</h2>
                <p style=\"font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;\">
                    Start by entering a product name in the sidebar and select your preferred platforms.
                    We'll search across multiple e-commerce sites to find you the best deals!
                </p>
                <div style=\"margin-top: 2rem; padding: 1.5rem; background: white; border-radius: 15px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1);\">
                    <p style=\"margin: 0; font-size: 1rem; color: #333;\">
                        <strong>Try searching for:</strong><br>
                        💻 laptop &nbsp;&nbsp;|&nbsp;&nbsp; 📱 phone &nbsp;&nbsp;|&nbsp;&nbsp; 🎧 headphones &nbsp;&nbsp;|&nbsp;&nbsp; ⌚ watch &nbsp;&nbsp;|&nbsp;&nbsp; 👟 shoes
                    </p>
                </div>
            </div>
        \"\"\", unsafe_allow_html=True)
        
        # Features showcase
        st.markdown(\"### ✨ Features\")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(\"\"\"
                <div style=\"padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); height: 100%;\">
                    <div style=\"font-size: 2.5rem; margin-bottom: 0.5rem;\">🔍</div>
                    <h4 style=\"color: #667eea; margin: 0.5rem 0;\">Multi-Platform Search</h4>
                    <p style=\"color: #666; font-size: 0.95rem;\">Search across Amazon, Flipkart, Myntra, eBay, and Walmart simultaneously</p>
                </div>
            \"\"\", unsafe_allow_html=True)
        
        with col2:
            st.markdown(\"\"\"
                <div style=\"padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); height: 100%;\">
                    <div style=\"font-size: 2.5rem; margin-bottom: 0.5rem;\">💰</div>
                    <h4 style=\"color: #667eea; margin: 0.5rem 0;\">Price Comparison</h4>
                    <p style=\"color: #666; font-size: 0.95rem;\">Compare prices with advanced filters for category and price range</p>
                </div>
            \"\"\", unsafe_allow_html=True)
        
        with col3:
            st.markdown(\"\"\"
                <div style=\"padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); height: 100%;\">
                    <div style=\"font-size: 2.5rem; margin-bottom: 0.5rem;\">📊</div>
                    <h4 style=\"color: #667eea; margin: 0.5rem 0;\">Analytics Dashboard</h4>
                    <p style=\"color: #666; font-size: 0.95rem;\">Visualize price trends and platform comparisons with interactive charts</p>
                </div>
            \"\"\", unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == \"__main__\":
    main()
"
