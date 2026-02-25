"""
🛠️ Tools Module
=============
Collection of tools used by various agents in the Personal AI Assistant.

Available Tool Categories:
- web_tools: Web search, scraping, and online information gathering
- email_tools: Email sending, reading, and management
- task_tools: Task management, reminders, and scheduling
- data_tools: Data analysis, visualization, and file processing
- utility_tools: General utilities like calculator, weather, etc.
"""

from .web_tools import (
    WebSearchTool,
    WebScrapingTool,
    NewsSearchTool,
    AcademicSearchTool
)

from .email_tools import (
    EmailSenderTool,
    EmailReaderTool
)

from .task_tools import (
    TaskManagerTool,
    ReminderTool,
    CalendarTool,
    NoteTool
)

from .data_tools import (
    FileAnalysisTool,
    DataVisualizationTool,
    StatisticsTool,
    ReportGeneratorTool
)

from .utility_tools import (
    CalculatorTool,
    WeatherTool,
    DateTimeTool,
    FileManagerTool
)

# Tool registry for easy access
TOOL_REGISTRY = {
    # Web Tools
    "web_search": WebSearchTool,
    "web_scraping": WebScrapingTool,
    "news_search": NewsSearchTool,
    "academic_search": AcademicSearchTool,
    
    # Email Tools
    "email_sender": EmailSenderTool,
    "email_reader": EmailReaderTool,
    
    # Task Tools
    "task_manager": TaskManagerTool,
    "reminder": ReminderTool,
    "calendar": CalendarTool,
    "note": NoteTool,
    
    # Data Tools
    "file_analysis": FileAnalysisTool,
    "data_visualization": DataVisualizationTool,
    "statistics": StatisticsTool,
    "report_generator": ReportGeneratorTool,
    
    # Utility Tools
    "calculator": CalculatorTool,
    "weather": WeatherTool,
    "datetime": DateTimeTool,
    "file_manager": FileManagerTool
}

def get_tool(tool_name: str):
    """Get a tool instance by name"""
    tool_class = TOOL_REGISTRY.get(tool_name)
    if tool_class:
        return tool_class()
    else:
        raise ValueError(f"Tool '{tool_name}' not found in registry")

def list_available_tools():
    """List all available tools"""
    return list(TOOL_REGISTRY.keys())

__all__ = [
    'TOOL_REGISTRY',
    'get_tool', 
    'list_available_tools',
    'WebSearchTool',
    'EmailSenderTool', 
    'TaskManagerTool',
    'FileAnalysisTool',
    'CalculatorTool'
]