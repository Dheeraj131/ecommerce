# 🛒 PriceHunter - Real-Time Price Comparison

## ✨ Features

- 🔍 **Search ANY Product** - No limits, search anything!
- 🤖 **AI-Powered Search** - Groq AI understands your queries
- 💰 **Real Price Comparison** - Compare across 5 platforms
- 🏆 **Best Price Detection** - Instantly find the lowest price
- 🔗 **Direct Buy Links** - One click to purchase
- ⚡ **Fast Results** - Get prices in seconds

## 🚀 Platforms Supported

- Amazon India
- Flipkart
- Myntra
- eBay India
- Walmart

## 🛠️ Setup Instructions

### 1. Get Groq API Key (FREE)

1. Go to https://console.groq.com
2. Sign up (free)
3. Go to "API Keys" section
4. Create new API key
5. Copy the key

### 2. Local Setup

```bash
# Install dependencies
pip install -r requirements_v2.txt

# Create secrets file
mkdir .streamlit
echo 'GROQ_API_KEY = "your_key_here"' > .streamlit/secrets.toml

# Run app
streamlit run streamlit_app_v2.py
```

### 3. Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Create new app
4. In Settings → Secrets, add:
   ```toml
   GROQ_API_KEY = "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"
   ```
5. Deploy!

## 📁 Files

```
.
├── streamlit_app_v2.py      # Main application
├── requirements_v2.txt       # Dependencies
├── .streamlit/
│   └── secrets.toml         # API keys (local)
└── README_V2.md             # This file
```

## 🔧 How It Works

1. **User enters product name** → "iPhone 15"
2. **Groq AI refines search** → Understands intent
3. **Web scraping** → Fetches prices from platforms
4. **Price comparison** → Shows best deal
5. **Direct links** → Buy with one click

## 🎯 Usage Examples

- Search: "iPhone 15 Pro"
- Search: "Nike Air Max shoes"
- Search: "Samsung 55 inch TV"
- Search: "Sony WH-1000XM5"
- Search: "MacBook Air M3"

## 🔐 Security

- API keys stored in secrets (not in code)
- Never commit secrets.toml to GitHub
- Use environment variables in production

## 📊 Tech Stack

- **Frontend**: Streamlit
- **AI**: Groq (Llama 3.3 70B)
- **Web Scraping**: BeautifulSoup4, Requests
- **Deployment**: Streamlit Cloud

## 🐛 Troubleshooting

**"Groq API key not found"**
- Add `GROQ_API_KEY` to `.streamlit/secrets.toml`
- Format: `GROQ_API_KEY = "gsk_..."`

**"No prices found"**
- Web scraping may fail (sites update frequently)
- App falls back to intelligent price estimation
- Try different product names

**Deployment errors**
- Verify secrets added in Streamlit Cloud
- Check all dependencies in requirements_v2.txt

## 📝 License

SPL Project 2026 - Educational Purpose

## 👨‍💻 Author

Built for SPL Project Submission

---

**Happy Shopping! 🛍️**
