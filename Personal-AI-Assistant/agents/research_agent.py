"""
🔍 Research Agent
=================
Intelligent research and information gathering assistant.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import our tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.web_tools import WebSearchTool, WebScrapingTool, NewsSearchTool
from tools.data_tools import FileAnalysisTool, DataVisualizationTool, StatisticsTool, ReportGeneratorTool
from tools.utility_tools import CalculatorTool, WeatherTool

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    🔍 Research Agent
    
    Specialized agent for conducting research, gathering information, and analyzing data.
    Combines web search, data analysis, and report generation capabilities.
    """
    
    def __init__(self, llm=None):
        self.name = "Research Agent"
        self.role = "Information Research Specialist"
        self.description = "Conducts thorough research, gathers information, and provides data-driven insights"
        
        # Initialize LLM
        if llm is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key is required for Research Agent")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.3  # Lower temperature for more factual responses
            )
        else:
            self.llm = llm
        
        # Initialize tools
        self.web_search_tool = WebSearchTool()
        self.web_scraping_tool = WebScrapingTool()
        self.news_tool = NewsSearchTool()
        self.file_analysis_tool = FileAnalysisTool()
        self.data_viz_tool = DataVisualizationTool()
        self.stats_tool = StatisticsTool()
        self.report_tool = ReportGeneratorTool()
        self.calc_tool = CalculatorTool()
        self.weather_tool = WeatherTool()
        
        # Research session storage
        self.research_sessions = {}
        
        # Create agent tools
        self.tools = self._create_tools()
        
        # Create agent
        self.agent = self._create_agent()
        
        # Agent executor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )
    
    def _create_tools(self):
        """Create the agent's research tools"""
        
        @tool
        def search_web(query: str, num_results: int = 5, search_type: str = "general") -> str:
            """Search the web for information on a specific topic.
            
            Args:
                query: Search query
                num_results: Number of results to return
                search_type: Type of search (general, academic, news, shopping)
                
            Returns:
                Search results with summaries
            """
            return self.web_search_tool.search(query, num_results, search_type)
        
        @tool
        def get_website_content(url: str, extract_type: str = "text") -> str:
            """Extract content from a specific website.
            
            Args:
                url: Website URL to analyze
                extract_type: Type of content to extract (text, links, images, tables)
                
            Returns:
                Extracted website content
            """
            return self.web_scraping_tool.scrape_url(url, extract_type)
        
        @tool
        def search_news(query: str, category: str = "general", language: str = "en", country: str = "us") -> str:
            """Search for recent news articles on a topic.
            
            Args:
                query: News search query
                category: News category (general, business, technology, science, health, sports, entertainment)
                language: Language code (en, es, fr, de, etc.)
                country: Country code (us, uk, ca, au, etc.)
                
            Returns:
                Recent news articles and summaries
            """
            return self.news_tool.search_news(query, category, language, country)
        
        @tool
        def analyze_data_file(file_path: str, analysis_type: str = "overview") -> str:
            """Analyze data from a file (CSV, Excel, JSON, etc.).
            
            Args:
                file_path: Path to the data file
                analysis_type: Type of analysis (overview, detailed, statistical)
                
            Returns:
                Data analysis results
            """
            return self.file_analysis_tool.analyze_file(file_path, analysis_type)
        
        @tool
        def create_data_visualization(file_path: str, chart_type: str, x_column: str, y_column: str = "", title: str = "") -> str:
            """Create data visualizations from dataset.
            
            Args:
                file_path: Path to the data file
                chart_type: Type of chart (line, bar, scatter, histogram, pie)
                x_column: X-axis column name
                y_column: Y-axis column name (if needed)
                title: Chart title
                
            Returns:
                Visualization creation result
            """
            return self.data_viz_tool.create_chart(file_path, chart_type, x_column, y_column, title)
        
        @tool
        def calculate_statistics(data_source: str, operation: str, column: str = "") -> str:
            """Perform statistical calculations on data.
            
            Args:
                data_source: Data source (file path or direct data)
                operation: Statistical operation (mean, median, std, correlation, regression)
                column: Column name for analysis
                
            Returns:
                Statistical analysis results
            """
            if os.path.exists(data_source):
                return self.stats_tool.analyze_file_statistics(data_source, operation, column)
            else:
                return self.stats_tool.calculate_basic_stats(data_source, operation)
        
        @tool
        def generate_research_report(topic: str, sections: str = "", format_type: str = "markdown") -> str:
            """Generate a comprehensive research report.
            
            Args:
                topic: Research topic
                sections: Comma-separated list of sections to include
                format_type: Report format (markdown, html, pdf)
                
            Returns:
                Generated research report
            """
            return self.report_tool.generate_report(topic, sections.split(",") if sections else [], format_type)
        
        @tool
        def perform_calculation(expression: str, calculation_type: str = "basic") -> str:
            """Perform mathematical calculations for research analysis.
            
            Args:
                expression: Mathematical expression to calculate
                calculation_type: Type of calculation (basic, advanced, statistical)
                
            Returns:
                Calculation result
            """
            if calculation_type == "advanced":
                # Extract operation and arguments from expression
                parts = expression.split()
                if len(parts) >= 2:
                    operation = parts[0]
                    args = parts[1:]
                    return self.calc_tool.advanced_calculate(operation, *args)
            
            return self.calc_tool.calculate(expression)
        
        @tool
        def get_weather_data(location: str, forecast_days: int = 0) -> str:
            """Get weather information for research purposes.
            
            Args:
                location: Location for weather data
                forecast_days: Number of forecast days (0 for current weather)
                
            Returns:
                Weather information
            """
            if forecast_days > 0:
                return self.weather_tool.get_forecast(location, forecast_days)
            else:
                return self.weather_tool.get_weather(location)
        
        @tool
        def start_research_session(topic: str, research_goals: str = "") -> str:
            """Start a new research session to track findings.
            
            Args:
                topic: Main research topic
                research_goals: Specific research objectives
                
            Returns:
                Research session start confirmation
            """
            session_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            session_data = {
                "id": session_id,
                "topic": topic,
                "goals": research_goals,
                "started_at": datetime.now().isoformat(),
                "findings": [],
                "sources": [],
                "notes": []
            }
            
            self.research_sessions[session_id] = session_data
            
            return f"""
🔍 **Research Session Started**

📋 **Session ID:** {session_id}
🎯 **Topic:** {topic}
📝 **Goals:** {research_goals or "General research"}
⏰ **Started:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

✅ **Session is now active!** All research findings and sources will be tracked.

💡 **Next Steps:**
- Use search tools to gather information
- Analyze any relevant data files
- Add findings and notes as you research
- Generate a comprehensive report when ready
"""
        
        @tool
        def add_research_finding(session_id: str, finding: str, source: str = "", importance: str = "medium") -> str:
            """Add a finding to the current research session.
            
            Args:
                session_id: Research session ID
                finding: Research finding or insight
                source: Source of the information
                importance: Importance level (low, medium, high, critical)
                
            Returns:
                Finding addition confirmation
            """
            if session_id not in self.research_sessions:
                return f"❌ Research session '{session_id}' not found. Start a new session first."
            
            finding_data = {
                "finding": finding,
                "source": source,
                "importance": importance,
                "timestamp": datetime.now().isoformat()
            }
            
            self.research_sessions[session_id]["findings"].append(finding_data)
            
            if source and source not in self.research_sessions[session_id]["sources"]:
                self.research_sessions[session_id]["sources"].append(source)
            
            return f"""
✅ **Finding Added to Research Session**

📊 **Session:** {self.research_sessions[session_id]["topic"]}
🔍 **Finding:** {finding}
📚 **Source:** {source or "Not specified"}
⭐ **Importance:** {importance}

📈 **Session Progress:**
- Total Findings: {len(self.research_sessions[session_id]["findings"])}
- Total Sources: {len(self.research_sessions[session_id]["sources"])}
"""
        
        @tool
        def get_research_summary(session_id: str = "") -> str:
            """Get summary of research session(s).
            
            Args:
                session_id: Specific session ID (optional, shows all if not provided)
                
            Returns:
                Research session summary
            """
            if session_id and session_id in self.research_sessions:
                return self._format_session_summary(self.research_sessions[session_id])
            elif not session_id and self.research_sessions:
                # Show all sessions
                summary = "🔍 **All Research Sessions:**\n\n"
                for sid, session in self.research_sessions.items():
                    summary += f"**{session['topic']}** (ID: {sid})\n"
                    summary += f"- Findings: {len(session['findings'])}\n"
                    summary += f"- Sources: {len(session['sources'])}\n"
                    summary += f"- Started: {session['started_at']}\n\n"
                return summary
            else:
                return "📭 No research sessions found. Start a new session to begin tracking research."
        
        return [
            search_web, get_website_content, search_news,
            analyze_data_file, create_data_visualization, calculate_statistics,
            generate_research_report, perform_calculation, get_weather_data,
            start_research_session, add_research_finding, get_research_summary
        ]
    
    def _format_session_summary(self, session: Dict[str, Any]) -> str:
        """Format a research session summary"""
        summary = f"""
🔍 **Research Session Summary**

📋 **Session Details:**
- **Topic:** {session['topic']}
- **Goals:** {session.get('goals', 'Not specified')}
- **Started:** {session['started_at']}
- **Duration:** {self._calculate_duration(session['started_at'])}

📊 **Progress Overview:**
- **Findings:** {len(session['findings'])}
- **Sources:** {len(session['sources'])}
- **Notes:** {len(session.get('notes', []))}

"""
        
        if session['findings']:
            summary += "🔍 **Key Findings:**\n"
            for i, finding in enumerate(session['findings'][-5:], 1):  # Last 5 findings
                summary += f"{i}. {finding['finding']} "
                if finding['source']:
                    summary += f"*(Source: {finding['source']})*"
                summary += f" [{finding['importance']}]\n"
        
        if session['sources']:
            summary += f"\n📚 **Sources Used:** {', '.join(session['sources'][:5])}"
            if len(session['sources']) > 5:
                summary += f" (and {len(session['sources']) - 5} more)"
        
        return summary
    
    def _calculate_duration(self, start_time: str) -> str:
        """Calculate duration from start time"""
        start = datetime.fromisoformat(start_time)
        duration = datetime.now() - start
        
        if duration.days > 0:
            return f"{duration.days} days, {duration.seconds // 3600} hours"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600} hours, {(duration.seconds % 3600) // 60} minutes"
        else:
            return f"{duration.seconds // 60} minutes"
    
    def _create_agent(self):
        """Create the research agent"""
        system_message = """You are an expert Research Agent, designed to conduct thorough and accurate research on any topic. You excel at gathering information, analyzing data, and providing comprehensive insights.

🔍 **Your Role & Expertise:**
- You are a professional researcher and data analyst
- Be thorough, accurate, and objective in your research
- Provide well-sourced, evidence-based information
- Help users understand complex topics and data
- Focus on credible sources and factual accuracy

🛠️ **Your Capabilities:**
1. **Web Research**: Search engines, websites, news sources
2. **Data Analysis**: Statistical analysis, file processing, visualization
3. **Report Generation**: Comprehensive research reports and summaries
4. **Source Verification**: Cross-reference information from multiple sources
5. **Research Management**: Track findings, organize sources, manage sessions

📊 **Research Methodology:**
- Always start by understanding the research question clearly
- Use multiple sources to verify information
- Distinguish between facts, opinions, and speculation
- Provide context and background for complex topics
- Cite sources and provide links when possible
- Identify potential biases or limitations in data

🔍 **Information Gathering Approach:**
- Begin with broad searches to understand the topic landscape
- Dive deeper into specific aspects based on user needs
- Look for recent and authoritative sources
- Cross-reference information to ensure accuracy
- Summarize key findings clearly and concisely

📈 **Data Analysis Standards:**
- Use appropriate statistical methods for the data type
- Clearly explain methodology and limitations
- Provide visualizations when they enhance understanding
- Interpret results in practical terms
- Suggest further analysis or data collection if needed

🎯 **Research Session Management:**
- Help users structure their research projects
- Track findings and sources systematically
- Provide regular progress updates
- Suggest next steps and research directions
- Generate comprehensive final reports

💡 **Proactive Research Support:**
- Suggest related topics and angles to explore
- Identify gaps in current knowledge or data
- Recommend additional sources or methods
- Provide alternative perspectives on topics
- Help formulate better research questions

🗣️ **Communication Style:**
- Be objective and factual
- Provide clear explanations of complex concepts
- Use evidence to support conclusions
- Acknowledge uncertainty when appropriate
- Structure information logically and clearly

Remember: Your goal is to help users find accurate, comprehensive, and actionable information. Always prioritize quality over quantity, and help users develop their own research and analytical skills."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_tool_calling_agent(self.llm, self.tools, prompt)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user research request and return response
        
        Args:
            user_input: User's research request or question
            
        Returns:
            Agent response with metadata
        """
        try:
            result = self.executor.invoke({"input": user_input})
            
            return {
                "success": True,
                "response": result["output"],
                "agent": self.name,
                "role": self.role,
                "timestamp": datetime.now().isoformat(),
                "intermediate_steps": result.get("intermediate_steps", [])
            }
            
        except Exception as e:
            logger.error(f"Research Agent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and capabilities"""
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "status": "active",
            "tools_count": len(self.tools),
            "active_sessions": len(self.research_sessions),
            "capabilities": [
                "Web Search & Scraping",
                "News Research",
                "Data Analysis",
                "Statistical Computing",
                "Data Visualization",
                "Report Generation",
                "Research Session Management",
                "Source Verification"
            ],
            "last_activity": datetime.now().isoformat()
        }
    
    def get_quick_overview(self) -> str:
        """Get quick research agent overview"""
        try:
            active_sessions = len(self.research_sessions)
            
            return f"""
🔍 **Research Agent - Quick Overview**

📅 **Current Status:**
- Agent: {self.name}
- Role: {self.role}
- Status: Active and Ready
- Active Research Sessions: {active_sessions}

🛠️ **Research Capabilities:**
- Web Search & Information Gathering
- Website Content Extraction
- News & Current Events Research
- Data File Analysis (CSV, Excel, JSON)
- Statistical Analysis & Calculations
- Data Visualization & Charts
- Comprehensive Report Generation
- Research Session Management

📊 **Research Tools Available:**
- Web Search Engine
- Website Scraper
- News Search API
- Data Analysis Suite
- Statistical Calculator
- Chart Generator
- Report Writer
- Weather Data (for research)

💡 **Quick Research Commands:**
- "Research [topic] for me"
- "Search for recent news about [subject]"
- "Analyze this data file: [path]"
- "Start a research session on [topic]"
- "Generate a report about [subject]"
- "Find statistics on [topic]"

🚀 **Ready to conduct thorough research on any topic!**
"""
            
        except Exception as e:
            return f"Research Agent Status: Active (Stats error: {str(e)})"

# Example usage and testing
if __name__ == "__main__":
    print("🔍 Testing Research Agent...")
    
    try:
        # Create agent
        agent = ResearchAgent()
        
        # Test basic functionality
        print("\n1. Agent Status:")
        print(agent.get_quick_overview())
        
        print("\n2. Starting a research session:")
        result = agent.process_request("Start a research session on artificial intelligence trends in 2024")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n3. Web search:")
        result = agent.process_request("Search for recent developments in AI and machine learning")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n4. News search:")
        result = agent.process_request("Find recent news about technology innovations")
        print(f"Response: {result.get('response', result.get('error'))}")
        
    except Exception as e:
        print(f"❌ Error testing Research Agent: {e}")
        print("💡 Make sure to set up your API keys in the .env file")