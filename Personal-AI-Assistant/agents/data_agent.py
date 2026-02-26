"""
📊 Data Agent
=============
Advanced data analysis and visualization specialist.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasicTool:
    """Basic tool wrapper for LangChain compatibility"""
    def __init__(self, name: str, description: str, func: callable):
        self.name = name
        self.description = description
        self.func = func
    
    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class SimpleDataAgent:
    """Simple data analysis agent that processes queries using available tools"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}
    
    def invoke(self, inputs: dict) -> dict:
        query = inputs.get("input", "")
        
        # Simple keyword-based tool selection for data analysis
        output = ""
        
        if any(keyword in query.lower() for keyword in ['analyze', 'analysis', 'examine', 'study']):
            output = "Data analysis functionality available. I can analyze datasets, files, and provide statistical insights."
        elif any(keyword in query.lower() for keyword in ['visualize', 'chart', 'graph', 'plot', 'visualization']):
            output = "Data visualization functionality available. I can create various charts, graphs, and visual representations."
        elif any(keyword in query.lower() for keyword in ['statistics', 'stats', 'statistical', 'calculate']):
            output = "Statistical analysis functionality available. I can perform statistical calculations and tests."
        elif any(keyword in query.lower() for keyword in ['report', 'summary', 'findings', 'insights']):
            output = "Report generation functionality available. I can create comprehensive data reports and summaries."
        elif any(keyword in query.lower() for keyword in ['file', 'csv', 'excel', 'json', 'data']):
            output = "File analysis functionality available. I can process and analyze various data file formats."
        elif any(keyword in query.lower() for keyword in ['clean', 'process', 'transform', 'prepare']):
            output = "Data processing functionality available. I can clean, transform, and prepare data for analysis."
        else:
            output = f"I can help with: data analysis, visualization, statistics, file processing, and report generation. What would you like to analyze about '{query}'?"
        
        return {"output": output}

# Import our tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.data_tools import FileAnalysisTool, DataVisualizationTool, StatisticsTool, ReportGeneratorTool
from tools.utility_tools import CalculatorTool, FileManagerTool
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class DataAgent:
    """
    📊 Data Agent
    
    Specialized agent for data analysis, visualization, and statistical computing.
    Combines file analysis, data visualization, statistical analysis, and report generation.
    """
    
    def __init__(self, llm=None):
        self.name = "Data Agent"
        self.role = "Data Analysis Specialist"
        self.description = "Analyzes data, creates visualizations, and provides statistical insights"
        
        # Initialize LLM
        if llm is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key is required for Data Agent")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.2  # Lower temperature for precise data analysis
            )
        else:
            self.llm = llm
        
        # Initialize tools with error handling
        try:
            self.file_analysis_tool = FileAnalysisTool()
            self.data_viz_tool = DataVisualizationTool()
            self.stats_tool = StatisticsTool()
            self.report_tool = ReportGeneratorTool()
            self.calc_tool = CalculatorTool()
            self.file_manager_tool = FileManagerTool()
        except Exception as e:
            logger.warning(f"Some tools could not be initialized: {e}")
        
        # Analysis session storage
        self.analysis_sessions = {}
        self.data_cache = {}
        
        # Create agent tools
        self.tools = self._create_tools()
        self.agent = SimpleDataAgent(self.llm, self.tools)
    
    def _create_tools(self):
        """Create the agent's data analysis tools"""
        
        @tool
        def analyze_data_file(file_path: str, analysis_type: str = "overview") -> str:
            """Analyze data file and provide comprehensive insights.
            
            Args:
                file_path: Path to the data file (CSV, Excel, JSON, TXT)
                analysis_type: Type of analysis (overview, detailed, statistical, quality)
                
            Returns:
                Complete data analysis results
            """
            return self.file_analysis_tool.analyze_file(file_path, analysis_type)
        
        @tool
        def create_visualization(file_path: str, chart_type: str, x_column: str, y_column: str = "", title: str = "", options: str = "") -> str:
            """Create data visualizations and charts.
            
            Args:
                file_path: Path to the data file
                chart_type: Type of chart (line, bar, scatter, histogram, pie, box, heatmap)
                x_column: X-axis column name
                y_column: Y-axis column name (required for some charts)
                title: Chart title
                options: Additional chart options (JSON string)
                
            Returns:
                Visualization creation result with file path
            """
            chart_options = {}
            if options:
                try:
                    chart_options = json.loads(options)
                except:
                    pass
            
            return self.data_viz_tool.create_chart(file_path, chart_type, x_column, y_column, title, **chart_options)
        
        @tool
        def calculate_statistics(file_path: str, operation: str, column: str = "", target_column: str = "") -> str:
            """Perform statistical calculations on data.
            
            Args:
                file_path: Path to the data file
                operation: Statistical operation (descriptive, correlation, regression, distribution, outliers)
                column: Primary column for analysis
                target_column: Target column for correlations/regression
                
            Returns:
                Statistical analysis results
            """
            return self.stats_tool.analyze_file_statistics(file_path, operation, column, target_column)
        
        @tool
        def compare_datasets(file_path1: str, file_path2: str, comparison_type: str = "basic") -> str:
            """Compare two datasets and identify differences.
            
            Args:
                file_path1: Path to first dataset
                file_path2: Path to second dataset
                comparison_type: Type of comparison (basic, statistical, detailed)
                
            Returns:
                Dataset comparison results
            """
            try:
                # Load both datasets
                data1_info = self.file_analysis_tool.analyze_file(file_path1, "overview")
                data2_info = self.file_analysis_tool.analyze_file(file_path2, "overview")
                
                # Basic comparison
                comparison = f"""
📊 **Dataset Comparison Analysis**

📁 **Dataset 1:** {file_path1}
📁 **Dataset 2:** {file_path2}

🔍 **Comparison Type:** {comparison_type}

📋 **Dataset 1 Overview:**
{data1_info}

📋 **Dataset 2 Overview:**
{data2_info}

💡 **Comparison Insights:**
"""
                
                if comparison_type == "statistical":
                    stats1 = self.stats_tool.analyze_file_statistics(file_path1, "descriptive")
                    stats2 = self.stats_tool.analyze_file_statistics(file_path2, "descriptive")
                    comparison += f"\n📊 **Statistical Comparison:**\n{stats1}\n\n{stats2}"
                
                return comparison
                
            except Exception as e:
                return f"❌ Error comparing datasets: {str(e)}"
        
        @tool
        def perform_data_calculation(expression: str, data_context: str = "") -> str:
            """Perform mathematical calculations in data analysis context.
            
            Args:
                expression: Mathematical expression or calculation
                data_context: Context about the data being analyzed
                
            Returns:
                Calculation result with data context
            """
            result = self.calc_tool.calculate(expression)
            
            if data_context:
                return f"📊 **Data Analysis Calculation**\n\n🔍 Context: {data_context}\n\n{result}"
            else:
                return result
        
        @tool
        def clean_data(file_path: str, cleaning_operations: str, output_path: str = "") -> str:
            """Clean and preprocess data file.
            
            Args:
                file_path: Path to the data file to clean
                cleaning_operations: Comma-separated list of operations (remove_duplicates, fill_nulls, remove_outliers, normalize)
                output_path: Output path for cleaned data (optional)
                
            Returns:
                Data cleaning results
            """
            try:
                # Load data
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    return "❌ Currently supports CSV and Excel files only for cleaning."
                
                original_shape = df.shape
                operations_performed = []
                
                # Parse cleaning operations
                operations = [op.strip() for op in cleaning_operations.split(",")]
                
                for operation in operations:
                    if operation == "remove_duplicates":
                        initial_rows = len(df)
                        df = df.drop_duplicates()
                        removed = initial_rows - len(df)
                        operations_performed.append(f"Removed {removed} duplicate rows")
                    
                    elif operation == "fill_nulls":
                        null_counts = df.isnull().sum()
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        
                        text_cols = df.select_dtypes(include=['object']).columns
                        df[text_cols] = df[text_cols].fillna('Unknown')
                        
                        operations_performed.append(f"Filled nulls in {len(null_counts[null_counts > 0])} columns")
                    
                    elif operation == "remove_outliers":
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        initial_rows = len(df)
                        
                        for col in numeric_cols:
                            Q1 = df[col].quantile(0.25)
                            Q3 = df[col].quantile(0.75)
                            IQR = Q3 - Q1
                            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
                        
                        removed = initial_rows - len(df)
                        operations_performed.append(f"Removed {removed} outlier rows")
                    
                    elif operation == "normalize":
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
                        operations_performed.append(f"Normalized {len(numeric_cols)} numeric columns")
                
                # Save cleaned data
                if not output_path:
                    output_path = file_path.replace('.', '_cleaned.')
                
                if output_path.endswith('.csv'):
                    df.to_csv(output_path, index=False)
                elif output_path.endswith('.xlsx'):
                    df.to_excel(output_path, index=False)
                
                final_shape = df.shape
                
                return f"""
🧹 **Data Cleaning Results**

📁 **Original File:** {file_path}
📁 **Cleaned File:** {output_path}

📊 **Data Shape Changes:**
- Original: {original_shape[0]} rows × {original_shape[1]} columns
- Final: {final_shape[0]} rows × {final_shape[1]} columns
- Change: {final_shape[0] - original_shape[0]} rows

🔧 **Operations Performed:**
{chr(10).join(f'• {op}' for op in operations_performed)}

✅ **Cleaning completed successfully!**
"""
                
            except Exception as e:
                return f"❌ Error cleaning data: {str(e)}"
        
        @tool
        def generate_data_report(file_path: str, report_type: str = "comprehensive", include_charts: bool = True) -> str:
            """Generate comprehensive data analysis report.
            
            Args:
                file_path: Path to the data file
                report_type: Type of report (comprehensive, summary, statistical, visual)
                include_charts: Whether to include charts in the report
                
            Returns:
                Generated report content
            """
            try:
                sections = []
                
                if report_type in ["comprehensive", "summary"]:
                    sections.append("Data Overview")
                    sections.append("Basic Statistics")
                
                if report_type in ["comprehensive", "statistical"]:
                    sections.append("Statistical Analysis")
                    sections.append("Correlations")
                
                if report_type in ["comprehensive", "visual"] and include_charts:
                    sections.append("Data Visualizations")
                
                return self.report_tool.generate_data_report(file_path, sections, "markdown")
                
            except Exception as e:
                return f"❌ Error generating report: {str(e)}"
        
        @tool
        def manage_data_files(operation: str, source_path: str = "", destination_path: str = "") -> str:
            """Manage data files (list, copy, move, info).
            
            Args:
                operation: File operation (list, copy, move, info)
                source_path: Source file path
                destination_path: Destination path (for copy/move)
                
            Returns:
                File operation result
            """
            if operation == "list":
                return self.file_manager_tool.manage_files("list", source_path or ".")
            elif operation == "info":
                return self.file_manager_tool.manage_files("info", source_path)
            elif operation in ["copy", "move"] and source_path and destination_path:
                return self.file_manager_tool.manage_files(operation, source_path, destination_path)
            else:
                return "❌ Invalid operation or missing parameters"
        
        @tool
        def start_data_analysis_session(dataset_name: str, file_path: str, analysis_goals: str = "") -> str:
            """Start a new data analysis session to track progress.
            
            Args:
                dataset_name: Name for the dataset being analyzed
                file_path: Path to the data file
                analysis_goals: Specific analysis objectives
                
            Returns:
                Analysis session start confirmation
            """
            session_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Basic dataset info
            dataset_info = self.file_analysis_tool.analyze_file(file_path, "overview")
            
            session_data = {
                "id": session_id,
                "dataset_name": dataset_name,
                "file_path": file_path,
                "goals": analysis_goals,
                "started_at": datetime.now().isoformat(),
                "analyses_performed": [],
                "visualizations_created": [],
                "insights": [],
                "dataset_info": dataset_info
            }
            
            self.analysis_sessions[session_id] = session_data
            
            return f"""
📊 **Data Analysis Session Started**

📋 **Session ID:** {session_id}
📁 **Dataset:** {dataset_name}
📂 **File:** {file_path}
🎯 **Goals:** {analysis_goals or "Exploratory analysis"}
⏰ **Started:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

📄 **Dataset Overview:**
{dataset_info}

✅ **Session is now active!** All analyses and visualizations will be tracked.

💡 **Recommended Next Steps:**
1. Explore data structure and quality
2. Calculate descriptive statistics
3. Check for correlations
4. Create visualizations
5. Identify insights and patterns
"""
        
        @tool
        def get_analysis_insights(session_id: str = "", insight_type: str = "summary") -> str:
            """Get insights from data analysis session.
            
            Args:
                session_id: Specific session ID (optional)
                insight_type: Type of insights (summary, detailed, recommendations)
                
            Returns:
                Analysis insights and recommendations
            """
            if session_id and session_id in self.analysis_sessions:
                session = self.analysis_sessions[session_id]
                
                insights_summary = f"""
📊 **Data Analysis Session Insights**

📋 **Session:** {session['dataset_name']} (ID: {session_id})
⏰ **Duration:** {self._calculate_session_duration(session['started_at'])}

📈 **Analysis Progress:**
- Analyses Performed: {len(session.get('analyses_performed', []))}
- Visualizations Created: {len(session.get('visualizations_created', []))}
- Key Insights: {len(session.get('insights', []))}

🔍 **Recent Analyses:**
"""
                
                recent_analyses = session.get('analyses_performed', [])[-3:]
                for i, analysis in enumerate(recent_analyses, 1):
                    insights_summary += f"{i}. {analysis}\n"
                
                if session.get('insights'):
                    insights_summary += "\n💡 **Key Insights:**\n"
                    for i, insight in enumerate(session['insights'][-5:], 1):
                        insights_summary += f"{i}. {insight}\n"
                
                return insights_summary
            
            elif not session_id and self.analysis_sessions:
                # Show all sessions
                summary = "📊 **All Analysis Sessions:**\n\n"
                for sid, session in self.analysis_sessions.items():
                    summary += f"**{session['dataset_name']}** (ID: {sid})\n"
                    summary += f"- File: {session['file_path']}\n"
                    summary += f"- Analyses: {len(session.get('analyses_performed', []))}\n"
                    summary += f"- Started: {session['started_at']}\n\n"
                return summary
            
            else:
                return "📭 No analysis sessions found. Start a new session to begin tracking analysis progress."
        
        return [
            analyze_data_file, create_visualization, calculate_statistics, compare_datasets,
            perform_data_calculation, clean_data, generate_data_report, manage_data_files,
            start_data_analysis_session, get_analysis_insights
        ]
    
    def _calculate_session_duration(self, start_time: str) -> str:
        """Calculate session duration from start time"""
        start = datetime.fromisoformat(start_time)
        duration = datetime.now() - start
        
        if duration.days > 0:
            return f"{duration.days} days, {duration.seconds // 3600} hours"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600} hours, {(duration.seconds % 3600) // 60} minutes"
        else:
            return f"{duration.seconds // 60} minutes"
    
    def _create_agent(self):
        """Create the data agent"""
        system_message = """You are an expert Data Agent, specialized in data analysis, statistical computing, and data visualization. You excel at uncovering insights from data and presenting them clearly.

📊 **Your Role & Expertise:**
- You are a professional data scientist and analyst
- Be precise, methodical, and evidence-based
- Focus on accuracy and statistical validity
- Help users understand their data thoroughly
- Provide actionable insights and recommendations

🛠️ **Your Core Capabilities:**
1. **Data Analysis**: File analysis, data profiling, quality assessment
2. **Statistical Computing**: Descriptive statistics, correlations, regression analysis
3. **Data Visualization**: Charts, graphs, plots for data exploration
4. **Data Cleaning**: Preprocessing, outlier removal, missing data handling
5. **Comparative Analysis**: Dataset comparisons, trend analysis
6. **Report Generation**: Comprehensive analysis reports and summaries
7. **Data Management**: File operations, data organization, format conversions

📈 **Data Analysis Methodology:**
- Always start with exploratory data analysis (EDA)
- Check data quality and identify issues early
- Use appropriate statistical methods for the data type
- Validate assumptions before applying statistical tests
- Provide context and interpretation for all results
- Suggest further analysis based on initial findings

📊 **Visualization Best Practices:**
- Choose appropriate chart types for the data and message
- Ensure visualizations are clear and interpretable
- Use proper scales, labels, and titles
- Highlight key patterns and outliers
- Create multiple views for complex datasets

🔍 **Statistical Analysis Standards:**
- Report confidence intervals and significance levels
- Check for assumptions and data distribution
- Use appropriate statistical tests and measures
- Explain limitations and potential biases
- Provide practical interpretation of results

💡 **Data Insights & Recommendations:**
- Look for patterns, trends, and anomalies
- Identify correlations and potential causations
- Suggest business implications of findings
- Recommend data collection improvements
- Propose follow-up analyses and experiments

🗣️ **Communication Style:**
- Explain technical concepts in accessible terms
- Use data-driven language and evidence
- Provide step-by-step analysis breakdowns
- Show your work and methodology
- Suggest multiple approaches when appropriate

Remember: Your goal is to help users extract maximum value from their data through rigorous analysis, clear visualizations, and actionable insights. Always ensure accuracy and provide comprehensive understanding of the data."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_tool_calling_agent(self.llm, self.tools, prompt)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user data analysis request and return response
        
        Args:
            user_input: User's data analysis request or question
            
        Returns:
            Agent response with metadata
        """
        try:
            result = self.agent.invoke({"input": user_input})
            
            return {
                "success": True,
                "response": result["output"],
                "agent": self.name,
                "role": self.role,
                "timestamp": datetime.now().isoformat(),
                "intermediate_steps": result.get("intermediate_steps", [])
            }
            
        except Exception as e:
            logger.error(f"Data Agent error: {e}")
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
            "active_sessions": len(self.analysis_sessions),
            "capabilities": [
                "Data File Analysis",
                "Statistical Computing",
                "Data Visualization",
                "Data Cleaning & Preprocessing",
                "Comparative Analysis",
                "Report Generation",
                "Data Management",
                "Session Tracking"
            ],
            "supported_formats": ["CSV", "Excel", "JSON", "TXT"],
            "last_activity": datetime.now().isoformat()
        }
    
    def get_data_overview(self) -> str:
        """Get quick data agent overview"""
        try:
            active_sessions = len(self.analysis_sessions)
            
            return f"""
📊 **Data Agent - Quick Overview**

📅 **Current Status:**
- Agent: {self.name}
- Role: {self.role}
- Status: Active and Ready
- Active Analysis Sessions: {active_sessions}

🛠️ **Data Analysis Capabilities:**
- File Analysis & Data Profiling
- Statistical Computing & Analysis
- Data Visualization & Charts
- Data Cleaning & Preprocessing
- Dataset Comparison & Validation
- Comprehensive Report Generation
- Analysis Session Management

📂 **Supported File Formats:**
- CSV (Comma-Separated Values)
- Excel (.xlsx, .xls)
- JSON (JavaScript Object Notation)
- TXT (Text files)

📈 **Analysis Types Available:**
- Descriptive Statistics
- Correlation Analysis
- Regression Analysis
- Distribution Analysis
- Outlier Detection
- Data Quality Assessment

📊 **Visualization Options:**
- Line Charts (trends, time series)
- Bar Charts (categories, comparisons)
- Scatter Plots (correlations)
- Histograms (distributions)
- Pie Charts (proportions)
- Box Plots (distributions, outliers)
- Heatmaps (correlations, patterns)

💡 **Quick Data Commands:**
- "Analyze this data file: [path]"
- "Create a scatter plot of [x] vs [y]"
- "Calculate statistics for [column]"
- "Clean this dataset: [operations]"
- "Compare these two datasets"
- "Generate a comprehensive report"
- "Start an analysis session"

🚀 **Ready to dive deep into your data!**
"""
            
        except Exception as e:
            return f"Data Agent Status: Active (Stats error: {str(e)})"

# Example usage and testing
if __name__ == "__main__":
    print("📊 Testing Data Agent...")
    
    try:
        # Create agent
        agent = DataAgent()
        
        # Test basic functionality
        print("\n1. Agent Status:")
        print(agent.get_data_overview())
        
        print("\n2. File management:")
        result = agent.process_request("List the files in the current directory and show me data files")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n3. Starting analysis session:")
        result = agent.process_request("Start a data analysis session for exploring sales data")
        print(f"Response: {result.get('response', result.get('error'))}")
        
    except Exception as e:
        print(f"❌ Error testing Data Agent: {e}")
        print("💡 Make sure to set up your API keys and have pandas/matplotlib installed")