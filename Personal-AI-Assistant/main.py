"""
🤖 Personal AI Assistant
========================
Multi-Agent AI Assistant with Specialized Capabilities

A comprehensive AI assistant system featuring multiple specialized agents:
- Task Manager: Productivity, goals, habits, time management
- Research Agent: Information gathering, analysis, reporting
- Business Agent: Email management, professional communications  
- Data Agent: Data analysis, visualization, statistics
- Coordinator: Routes requests and manages multi-agent workflows
"""

import streamlit as st
import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import pandas as pd

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import configuration and agents
from config.settings import AppConfig
from agents.coordinator import CoordinatorAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ai_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}

.agent-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    background-color: #f8f9fa;
}

.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 5px;
}

.status-active {
    background-color: #28a745;
}

.status-inactive {
    background-color: #dc3545;
}

.chat-message {
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 10px;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.assistant-message {
    background-color: #f1f8e9;
    border-left: 4px solid #4caf50;
}

.sidebar-section {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'coordinator' not in st.session_state:
    st.session_state.coordinator = None

if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False

def initialize_system():
    """Initialize the AI assistant system"""
    try:
        # Check if Google API key is available
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("🔑 Google API key not found! Please add it to your .env file.")
            st.info("Create a .env file in the project root with: GOOGLE_API_KEY=your_key_here")
            return False
        
        # Create coordinator agent
        if st.session_state.coordinator is None:
            with st.spinner("🤖 Initializing AI Assistant System..."):
                st.session_state.coordinator = CoordinatorAgent()
                st.session_state.system_initialized = True
                logger.info("AI Assistant system initialized successfully")
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error initializing system: {str(e)}")
        logger.error(f"System initialization error: {e}")
        return False

def display_sidebar():
    """Display the sidebar with system information and controls"""
    with st.sidebar:
        st.markdown("# 🎛️ System Control")
        
        # System status
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 📊 System Status")
        
        if st.session_state.system_initialized:
            st.markdown('🟢 **System Active**')
            
            # Get system status
            try:
                status_response = st.session_state.coordinator.process_request("Get system overview")
                if status_response.get("success"):
                    with st.expander("📋 Detailed Status", expanded=False):
                        st.markdown(status_response["response"])
                
            except Exception as e:
                st.warning(f"⚠️ Status check failed: {str(e)}")
        else:
            st.markdown('🔴 **System Offline**')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick actions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Tasks", help="Task management"):
                add_message("user", "Show me my task dashboard")
                process_user_request("Show me my task dashboard")
            
            if st.button("🔍 Research", help="Research tools"):
                add_message("user", "What research capabilities do you have?")
                process_user_request("What research capabilities do you have?")
        
        with col2:
            if st.button("💼 Business", help="Business tools"):
                add_message("user", "Show me business tools overview")
                process_user_request("Show me business tools overview")
            
            if st.button("📊 Data", help="Data analysis"):
                add_message("user", "What data analysis tools are available?")
                process_user_request("What data analysis tools are available?")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Agent selection
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 🤖 Direct Agent Access")
        
        agent_choice = st.selectbox(
            "Choose specific agent:",
            ["Auto-Route", "Task Manager", "Research Agent", "Business Agent", "Data Agent"],
            help="Select an agent to route your message directly"
        )
        
        if agent_choice != "Auto-Route":
            st.session_state.preferred_agent = agent_choice.lower().replace(" ", "_").replace("_agent", "")
        else:
            st.session_state.preferred_agent = ""
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo Guide
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 🎯 Demo Guide")
        
        with st.expander("💡 Try These Questions", expanded=False):
            st.markdown("""
**📋 Task Manager:**
- "Help me organize my daily tasks"
- "Set a reminder for tomorrow"
- "Create a project timeline"

**🔍 Research Agent:**
- "Research the latest AI trends"
- "Find info about renewable energy"
- "Search for market data"

**💼 Business Agent:**
- "Send an email to my team" 
- "Draft a meeting agenda"
- "Create a professional email"

**📊 Data Agent:**
- "Analyze this sales data"
- "Create a data visualization"
- "Generate insights from data"

**🎛️ Coordinator:**
- "Start a collaboration between agents"
- "Show me available agents"
- "Plan a multi-agent workflow"
            """)
            
        with st.expander("📊 Sample Data", expanded=False):
            st.markdown("""
**Sales Data (copy & paste):**
```
Order_ID,Date,Customer,Amount
1001,2026-01-15,Acme Corp,15000
1002,2026-01-16,Tech Solutions,8500
1003,2026-01-17,Global Industries,3200
```

**Task Data:**
```
Task,Priority,Due_Date,Status
Budget Review,High,2026-03-01,Pending
Team Meeting,Medium,2026-02-28,In Progress
Client Call,High,2026-02-27,Not Started
```
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Settings
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## ⚙️ Settings")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("🔄 Reset System"):
            st.session_state.coordinator = None
            st.session_state.system_initialized = False
            st.session_state.chat_history = []
            st.rerun()
        
        # Export chat
        if st.button("💾 Export Chat"):
            export_chat_history()
        
        st.markdown('</div>', unsafe_allow_html=True)

def add_message(sender: str, message: str, metadata: Dict = None):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        "sender": sender,
        "message": message,
        "timestamp": datetime.now(),
        "metadata": metadata or {}
    })

def process_user_request(user_input: str):
    """Process user request through the coordinator"""
    try:
        if not st.session_state.system_initialized:
            add_message("assistant", "❌ System not initialized. Please check your configuration.")
            return
        
        # Add preferred agent to request if specified
        preferred_agent = getattr(st.session_state, 'preferred_agent', '')
        if preferred_agent:
            request_text = f"Route to {preferred_agent}: {user_input}"
        else:
            request_text = user_input
        
        # Process request through coordinator
        with st.spinner("🤖 Processing your request..."):
            response = st.session_state.coordinator.process_request(request_text)
        
        if response.get("success"):
            add_message("assistant", response["response"], {
                "agent": response.get("agent", "Coordinator"),
                "timestamp": response.get("timestamp")
            })
        else:
            error_msg = f"❌ Error: {response.get('error', 'Unknown error occurred')}"
            add_message("assistant", error_msg)
        
    except Exception as e:
        error_msg = f"❌ System error: {str(e)}"
        add_message("assistant", error_msg)
        logger.error(f"Request processing error: {e}")

def display_chat():
    """Display the chat interface"""
    st.markdown('<h1 class="main-header">🤖 Personal AI Assistant</h1>', unsafe_allow_html=True)
    
    # Display welcome message if no chat history
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="chat-message assistant-message">
            <h3>👋 Welcome to Your Personal AI Assistant!</h3>
            <p>I'm your multi-agent AI assistant with specialized capabilities:</p>
            <ul>
                <li><strong>🎯 Task Manager:</strong> Productivity, goals, habits, time management</li>
                <li><strong>🔍 Research Agent:</strong> Information gathering, analysis, reporting</li>
                <li><strong>💼 Business Agent:</strong> Email management, professional communications</li>
                <li><strong>📊 Data Agent:</strong> Data analysis, visualization, statistics</li>
                <li><strong>🎛️ Coordinator:</strong> Routes requests and manages workflows</li>
            </ul>
            <p><strong>💡 Try asking:</strong></p>
            <ul>
                <li>"Help me organize my daily tasks"</li>
                <li>"Research the latest AI trends"</li>
                <li>"Send an email to my team"</li>
                <li>"Analyze this sales data"</li>
                <li>"Start a collaboration between agents"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for i, chat in enumerate(st.session_state.chat_history):
        timestamp = chat["timestamp"].strftime("%H:%M:%S")
        
        if chat["sender"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You</strong> <small>({timestamp})</small><br>
                {chat["message"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            agent_name = chat["metadata"].get("agent", "Assistant")
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 {agent_name}</strong> <small>({timestamp})</small><br>
                {chat["message"]}
            </div>
            """, unsafe_allow_html=True)

def display_input_area():
    """Display the user input area"""
    st.markdown("---")
    
    # Input methods
    input_method = st.radio(
        "Choose input method:",
        ["💬 Chat", "📝 Detailed Request", "🎯 Quick Commands"],
        horizontal=True
    )
    
    if input_method == "💬 Chat":
        user_input = st.chat_input("Type your message here...", key="chat_input")
        
        if user_input:
            add_message("user", user_input)
            process_user_request(user_input)
            st.rerun()
    
    elif input_method == "📝 Detailed Request":
        with st.form("detailed_request_form"):
            user_input = st.text_area(
                "Detailed Request:",
                height=100,
                placeholder="Describe your request in detail..."
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"])
            with col2:
                submitted = st.form_submit_button("🚀 Submit Request", type="primary")
            
            if submitted and user_input:
                priority_prefix = f"[{priority} Priority] " if priority != "Normal" else ""
                full_request = f"{priority_prefix}{user_input}"
                
                add_message("user", full_request)
                process_user_request(full_request)
                st.rerun()
    
    elif input_method == "🎯 Quick Commands":
        st.markdown("**💡 Try These Demo Questions:**")
        
        # Agent-specific demo questions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📋 Task Manager:**")
            if st.button("Help me organize my daily tasks", key="task1"):
                command = "Help me organize my daily tasks"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
            
            if st.button("Set a reminder for tomorrow", key="task2"):
                command = "Set a reminder to call the client tomorrow"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
                
            st.markdown("**💼 Business Agent:**")
            if st.button("Send an email to my team", key="business1"):
                command = "Send an email to my team"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
        
        with col2:
            st.markdown("**🔍 Research Agent:**")
            if st.button("Research the latest AI trends", key="research1"):
                command = "Research the latest AI trends"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
            
            if st.button("Find info about renewable energy", key="research2"):
                command = "Find information about renewable energy technologies"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
                
            st.markdown("**📊 Data Analysis:**")
            if st.button("Analyze sample sales data", key="data1"):
                sample_data = """Analyze this sales data
Order_ID,Date,Customer,Product,Amount
1001,2026-01-15,Acme Corp,Software License,15000
1002,2026-01-16,Tech Solutions,Consulting,8500
1003,2026-01-17,Global Industries,Support,3200"""
                add_message("user", sample_data)
                process_user_request(sample_data)
                st.rerun()
        
        with col3:
            st.markdown("**🎛️ Coordinator:**")
            if st.button("Start a collaboration between agents", key="coord1"):
                command = "Start a collaboration between agents"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
            
            if st.button("Show me available agents", key="coord2"):
                command = "Show me available agents"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
                
            if st.button("Plan a multi-agent workflow", key="coord3"):
                command = "Plan a multi-agent workflow for market research"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
        
        # Additional helpful examples
        st.markdown("---")
        st.markdown("**🎯 More Examples:**")
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            if st.button("📈 Business Intelligence Demo", key="demo1"):
                command = "Coordinate a comprehensive market analysis using research and data agents"
                add_message("user", command)
                process_user_request(command)
                st.rerun()
        
        with example_col2:
            if st.button("📋 Project Planning Demo", key="demo2"):
                command = "Create a project timeline and coordinate tasks across multiple agents"
                add_message("user", command)
                process_user_request(command)
                st.rerun()

def export_chat_history():
    """Export chat history as JSON"""
    try:
        chat_data = {
            "exported_at": datetime.now().isoformat(),
            "total_messages": len(st.session_state.chat_history),
            "conversations": []
        }
        
        for chat in st.session_state.chat_history:
            chat_data["conversations"].append({
                "sender": chat["sender"],
                "message": chat["message"],
                "timestamp": chat["timestamp"].isoformat(),
                "metadata": chat["metadata"]
            })
        
        json_data = json.dumps(chat_data, indent=2)
        
        st.download_button(
            label="📥 Download Chat History",
            data=json_data,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
    except Exception as e:
        st.error(f"Error exporting chat: {str(e)}")

def main():
    """Main application function"""
    try:
        # Initialize system
        if not st.session_state.system_initialized:
            if not initialize_system():
                st.stop()
        
        # Display sidebar
        display_sidebar()
        
        # Main content area
        display_chat()
        display_input_area()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8em;">
            🤖 Personal AI Assistant | Built with LangChain & Streamlit | 
            Multi-Agent Architecture © 2024
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Application error: {str(e)}")
        logger.error(f"Main application error: {e}")
        
        st.markdown("### 🔧 Troubleshooting")
        st.markdown("""
        1. **Check Configuration**: Ensure your .env file has all required API keys
        2. **Reset System**: Use the reset button in the sidebar
        3. **Check Logs**: Look at logs/ai_assistant.log for details
        4. **Dependencies**: Make sure all required packages are installed
        """)

if __name__ == "__main__":
    main()