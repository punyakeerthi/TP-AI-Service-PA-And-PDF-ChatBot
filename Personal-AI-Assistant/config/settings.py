"""
🔧 Personal AI Assistant Configuration Settings
===========================================
Central configuration for all agents, tools, and settings.
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """LLM Model configuration"""
    name: str = "gemini-1.5-flash"
    temperature: float = 0.1
    max_tokens: int = 1000
    timeout: int = 60

@dataclass
class AgentConfig:
    """Agent-specific configuration"""
    max_iterations: int = 5
    max_execution_time: int = 120
    verbose: bool = True
    memory_window: int = 10

@dataclass
class AppConfig:
    """Application-level configuration"""
    app_name: str = "Personal AI Assistant"
    app_icon: str = "🤖"
    layout: str = "wide"
    theme: str = "light"
    
    # Data storage paths
    data_dir: str = "data"
    tasks_file: str = "data/tasks.json"
    memory_file: str = "data/memory.json"
    
    # UI Settings
    sidebar_initial_state: str = "expanded"
    max_chat_history: int = 50

# =============================
# 🔧 Configuration Instances
# =============================

# Model configurations for different use cases
MODEL_CONFIGS = {
    "default": ModelConfig(
        name="gemini-1.5-flash",
        temperature=0.1,
        max_tokens=1000
    ),
    "creative": ModelConfig(
        name="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=1500
    ),
    "analytical": ModelConfig(
        name="gemini-1.5-flash",
        temperature=0.0,
        max_tokens=2000
    )
}

# Agent-specific configurations
AGENT_CONFIGS = {
    "task_manager": AgentConfig(
        max_iterations=3,
        max_execution_time=60,
        memory_window=15
    ),
    "research_agent": AgentConfig(
        max_iterations=6,
        max_execution_time=180,
        memory_window=20
    ),
    "business_agent": AgentConfig(
        max_iterations=4,
        max_execution_time=90,
        memory_window=10
    ),
    "data_agent": AgentConfig(
        max_iterations=5,
        max_execution_time=120,
        memory_window=8
    ),
    "coordinator": AgentConfig(
        max_iterations=7,
        max_execution_time=200,
        memory_window=25
    )
}

# Application configuration
APP_CONFIG = AppConfig()

# =============================
# 🛠️ Tool Configurations
# =============================

TOOL_CONFIGS = {
    "web_search": {
        "timeout": 10,
        "max_results": 5,
        "user_agent": "PersonalAI-Assistant/1.0"
    },
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "timeout": 30
    },
    "weather": {
        "timeout": 10,
        "units": "metric",
        "default_location": "New York"
    },
    "file_processing": {
        "max_file_size_mb": 10,
        "supported_formats": [".pdf", ".txt", ".csv", ".xlsx", ".docx"],
        "temp_dir": "temp"
    }
}

# =============================
# 🎯 Agent Capabilities Matrix
# =============================

AGENT_CAPABILITIES = {
    "task_manager": {
        "description": "Manages tasks, reminders, schedules, and personal organization",
        "tools": ["task_management", "calendar", "reminders", "notes"],
        "specialties": ["productivity", "organization", "scheduling"]
    },
    "research_agent": {
        "description": "Handles web search, academic research, and information gathering",
        "tools": ["web_search", "arxiv_search", "news_search", "fact_check"],
        "specialties": ["research", "information_gathering", "fact_checking"]
    },
    "business_agent": {
        "description": "Manages business operations, email, weather, calculations",
        "tools": ["email", "weather", "calculator", "calendar_scheduling"],
        "specialties": ["communication", "business_ops", "calculations"]
    },
    "data_agent": {
        "description": "Handles data analysis, visualization, and file processing",
        "tools": ["file_analysis", "data_viz", "statistics", "report_generation"],
        "specialties": ["data_analysis", "visualization", "reporting"]
    },
    "coordinator": {
        "description": "Routes tasks to appropriate agents and manages workflows",
        "tools": ["agent_routing", "task_delegation", "workflow_management"],
        "specialties": ["coordination", "workflow", "task_routing"]
    }
}

# =============================
# 🌟 Feature Flags
# =============================

FEATURE_FLAGS = {
    "multi_agent_mode": True,
    "memory_persistence": True,
    "email_functionality": True,
    "web_search": True,
    "file_processing": True,
    "data_visualization": True,
    "academic_research": True,
    "weather_integration": True,
    "task_management": True,
    "conversation_history": True,
    "agent_coordination": True,
    "auto_tool_selection": True
}

# =============================
# 📊 Logging Configuration
# =============================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": ["console", "file"],
    "file_path": "logs/assistant.log"
}

# =============================
# 🚀 Performance Settings
# =============================

PERFORMANCE_SETTINGS = {
    "enable_caching": True,
    "cache_ttl": 3600,  # 1 hour
    "max_concurrent_agents": 3,
    "request_timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 2
}

def get_api_key(service: str) -> str:
    """Get API key for a service"""
    key_map = {
        "google": "GOOGLE_API_KEY",
        "serpapi": "SERPAPI_API_KEY",
        "weather": "WEATHER_API_KEY",
        "email": "EMAIL_ADDRESS"
    }
    
    env_var = key_map.get(service.lower())
    if env_var:
        return os.getenv(env_var, "")
    return ""

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature, False)

def get_model_config(config_name: str = "default") -> ModelConfig:
    """Get model configuration"""
    return MODEL_CONFIGS.get(config_name, MODEL_CONFIGS["default"])

def get_agent_config(agent_name: str) -> AgentConfig:
    """Get agent configuration"""
    return AGENT_CONFIGS.get(agent_name, AgentConfig())

def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """Get tool configuration"""
    return TOOL_CONFIGS.get(tool_name, {})

# =============================
# 🎨 UI Constants
# =============================

UI_CONSTANTS = {
    "colors": {
        "primary": "#FF6B6B",
        "secondary": "#4ECDC4", 
        "success": "#45B7D1",
        "warning": "#FFA07A",
        "error": "#FF6B9D"
    },
    "icons": {
        "task": "📋",
        "research": "🔍", 
        "business": "💼",
        "data": "📊",
        "coordinator": "🎯",
        "user": "👤",
        "assistant": "🤖"
    },
    "messages": {
        "welcome": "👋 Welcome to your Personal AI Assistant! How can I help you today?",
        "processing": "🤔 Thinking and processing your request...",
        "error": "❌ I encountered an error. Please try again.",
        "success": "✅ Task completed successfully!"
    }
}