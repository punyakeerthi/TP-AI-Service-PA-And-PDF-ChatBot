# 🤖 Personal AI Assistant with Multiple Agents

A comprehensive Personal AI Assistant featuring multiple specialized agents that work together to help with daily tasks, research, productivity, and more!

## ✨ Features

### 🧠 **Multiple Specialized Agents:**
- **📋 Task Manager Agent** - Handle todos, schedules, and reminders
- **🔍 Research Agent** - Web search, academic papers, fact-checking
- **💼 Business Agent** - Email, calculations, weather, meetings
- **📊 Data Agent** - File analysis, charts, reports
- **🎯 Coordinator Agent** - Routes tasks to appropriate agents

### 🛠️ **Powerful Tools:**
- Web search and information gathering
- Email sending and management
- Task and calendar management
- Data analysis and visualization
- Weather and location services
- File processing and analysis
- Mathematical calculations
- Academic research tools

### 🚀 **Smart Features:**
- **Multi-agent coordination** - Agents work together on complex tasks
- **Context sharing** - Agents remember conversation history
- **Error handling** - Robust error management and retries
- **Extensible design** - Easy to add new agents and tools
- **Web interface** - Beautiful Streamlit UI

## 🏁 Quick Start (100% FREE Setup!)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get FREE API Keys

#### 🆓 **Google Gemini AI** (Required - FREE)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key" 
4. Copy your free API key (15 requests/min, 1M tokens/day FREE!)

#### 🆓 **Gmail App Password** (Optional - FREE)
1. Enable 2-factor authentication on Gmail
2. Go to [Google Account Settings](https://myaccount.google.com/apppasswords)  
3. Generate app password for "Mail"
4. Use this password (not your regular gmail password)

#### 🆓 **OpenWeatherMap** (Optional - FREE)
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key (1000 calls/day FREE!)

#### 🆓 **NewsAPI** (Optional - FREE)  
1. Register at [NewsAPI](https://newsapi.org/register)
2. Get free API key (500 requests/day FREE!)

### 3. Setup Environment (Only FREE APIs!)
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your FREE API keys:
GOOGLE_API_KEY=your_free_google_gemini_key
EMAIL_ADDRESS=your_email@gmail.com  
EMAIL_PASSWORD=your_gmail_app_password
WEATHER_API_KEY=your_free_openweather_key
NEWS_API_KEY=your_free_newsapi_key
```

### 4. Run the Assistant (FREE!)
```bash
streamlit run main.py
```

## 💰 **100% FREE - No Payment Required!**

This Personal AI Assistant uses **ONLY FREE tools and APIs!**

### 🆓 **What's Completely Free:**
- ✅ **Google Gemini AI** - 1M tokens/day FREE
- ✅ **Gmail Email** - FREE with any Gmail account  
- ✅ **DuckDuckGo Search** - FREE unlimited web search
- ✅ **Wikipedia API** - FREE encyclopedia access
- ✅ **OpenWeatherMap** - 1000 calls/day FREE
- ✅ **NewsAPI** - 500 requests/day FREE
- ✅ **All built-in tools** - Calculator, file manager, etc.

### 📖 **Need Help with FREE Setup?**
👉 **[Complete FREE Tools Guide](FREE_TOOLS_GUIDE.md)** - Step-by-step setup for all FREE APIs!

**💡 Total Cost: $0.00/month for full functionality!**

## 🎯 Example Tasks

The assistant can handle complex multi-step tasks:

```
🗣️ "Research AI trends, create a summary report, and email it to my team"

🤖 Agent Workflow:
1. Research Agent → Search for AI trends and papers
2. Data Agent → Analyze findings and create report
3. Business Agent → Format and email the report
```

```
🗣️ "Check weather in Tokyo, add it to my travel notes, and set a reminder"

🤖 Agent Workflow:
1. Business Agent → Get Tokyo weather
2. Task Manager → Add to travel notes
3. Task Manager → Set weather reminder
```

## 📁 Project Structure

```
Personal-AI-Assistant/
├── main.py                 # Main Streamlit app
├── agents/                 # Agent definitions
│   ├── __init__.py        
│   ├── task_manager.py    # Task management agent
│   ├── research_agent.py  # Research and search agent
│   ├── business_agent.py  # Business operations agent
│   ├── data_agent.py      # Data analysis agent
│   └── coordinator.py     # Master coordinator agent
├── tools/                 # Tool implementations
│   ├── __init__.py       
│   ├── web_tools.py      # Web search and scraping
│   ├── email_tools.py    # Email functionality
│   ├── task_tools.py     # Task management tools
│   ├── data_tools.py     # Data processing tools
│   └── utility_tools.py  # General utilities
├── config/               # Configuration
│   └── settings.py      # App settings and config
├── data/                # Data storage
│   ├── tasks.json       # Task storage
│   └── memory.json      # Conversation memory
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
├── README.md          # This file
└── STUDENT_NOTES.md   # Learning guide
```

## 🔧 Configuration

### 🆓 **FREE Tools & APIs**
- **✅ Google Gemini AI** - FREE tier: 15 requests/minute, 1M tokens/day
- **✅ Email (Gmail SMTP)** - FREE with Gmail account (use App Password)
- **✅ OpenWeatherMap** - FREE tier: 1000 calls/day
- **✅ NewsAPI** - FREE tier: 500 requests/day
- **✅ All built-in tools** - Calculator, file manager, date/time tools (100% FREE)

### 🔄 **FREE Alternatives to Paid Services**

#### Instead of SerpAPI (Paid) → Use These FREE Options:
- **DuckDuckGo Search** - Completely free web search
- **Wikipedia API** - Free encyclopedia data
- **Google Custom Search** - 100 searches/day free
- **Bing Search API** - 1000 searches/month free

### Environment Variables Setup
```bash
# 🆓 FREE - Required for core functionality
GOOGLE_API_KEY=your_free_google_api_key

# 🆓 FREE - Optional email features (Gmail App Password)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# 🆓 FREE - Optional weather data
WEATHER_API_KEY=your_free_openweather_key

# 🆓 FREE - Optional news search
NEWS_API_KEY=your_free_newsapi_key

# ❌ PAID - Not needed! We use free alternatives
# SERPAPI_API_KEY=not_needed_we_use_free_alternatives
```

### Agent Settings
Customize agent behavior in `config/settings.py`:
- Model selection (Gemini models)
- Temperature and creativity settings
- Maximum iterations and timeouts
- Tool availability per agent

## 💡 Usage Examples

### Simple Tasks
```python
# Ask any agent directly
"What's the weather in London?"
"Add 'buy milk' to my todo list"
"Search for recent Python tutorials"
```

### Complex Multi-Agent Tasks
```python
# Coordinator will route to appropriate agents
"Research sustainable energy, create a presentation, and schedule a meeting to discuss it"
"Analyze my expense data, find trends, and set budget reminders"
"Find academic papers on machine learning, summarize key points, and save to my research notes"
```

## 🧪 Testing

Each agent and tool includes test examples:

```bash
# Test individual agents
python -m agents.research_agent
python -m agents.task_manager

# Test specific tools
python -m tools.web_tools
python -m tools.email_tools
```

## 🔒 Privacy & Security

- **Local data storage** - Tasks and notes stored locally
- **Secure API handling** - Environment variables for keys
- **No data sharing** - Your data stays on your machine
- **Optional features** - Email and external APIs are optional

## 🚀 Extending the Assistant

### Add New Agents
1. Create new agent file in `agents/`
2. Implement required methods
3. Register in coordinator
4. Add to main interface

### Add New Tools
1. Create tool function
2. Add proper error handling
3. Include in appropriate agent
4. Update documentation

## 📚 Learning Resources

- **STUDENT_NOTES.md** - Comprehensive learning guide
- **Code comments** - Detailed explanations in all files
- **Agent examples** - Working examples for each agent type
- **Tool tutorials** - Step-by-step tool creation guides

## 🆘 Troubleshooting

### Common Issues:
1. **API Key Errors** - Check .env file setup
2. **Import Errors** - Ensure all dependencies installed
3. **Agent Timeouts** - Check internet connection and API limits
4. **Memory Issues** - Restart app to clear conversation history

### Getting Help:
- Check STUDENT_NOTES.md for detailed explanations
- Review code comments for implementation details
- Test individual components using built-in examples

## 🤝 Contributing

Feel free to:
- Add new agents and tools
- Improve error handling
- Enhance the UI
- Add new features
- Submit bug reports

## 📄 License

This project is open source and available under the MIT License.

---

**🎉 Ready to explore the future of personal AI assistance? Start with simple tasks and work your way up to complex multi-agent workflows!**