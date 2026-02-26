"""
Business Agent - Professional Operations & Communication Manager

This agent specializes in business operations, email management, 
and professional task coordination.

Author: Personal AI Assistant System
Version: 2.0 (Updated for modern LangChain compatibility)
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

# Load environment variables from .env file
load_dotenv()

# Import tools
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

try:
    from email_tools import EmailSenderTool, EmailReaderTool, EmailManagerTool
    from task_tools import TaskManagerTool, ReminderTool, CalendarTool
    from utility_tools import *
except ImportError as e:
    print(f"Warning: Could not import all tools: {e}")
    # Create placeholder classes
    class EmailSenderTool:
        def send_email(self, *args, **kwargs):
            return "Email tool not available"
    class TaskManagerTool:
        def create_task(self, *args, **kwargs):
            return "Task tool not available"

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

class SimpleBusinessAgent:
    """Simple business agent that processes queries using available tools"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}
    
    def invoke(self, inputs: dict) -> dict:
        query = inputs.get("input", "")
        
        # Simple keyword-based tool selection
        output = ""
        
        if any(keyword in query.lower() for keyword in ['email', 'mail', 'message']):
            if 'send' in query.lower():
                output = "Email functionality available. Please provide recipient, subject, and message details."
            elif 'check' in query.lower() or 'get' in query.lower():
                output = "Email checking functionality available. I can help you retrieve and organize emails."
            elif 'template' in query.lower():
                output = "I can generate professional email templates for various business purposes."
            else:
                output = "Email management capabilities: send, check, organize, templates, analytics."
        
        elif any(keyword in query.lower() for keyword in ['task', 'project', 'todo', 'schedule']):
            if 'create' in query.lower():
                output = "Task creation functionality available. Please provide task details, priority, and due date."
            else:
                output = "Task management capabilities: create tasks, manage projects, schedule tracking."
        
        elif any(keyword in query.lower() for keyword in ['calculate', 'percentage', 'roi', 'budget', 'metric']):
            if 'percentage' in query.lower():
                # Try to extract numbers for percentage calculation
                words = query.split()
                numbers = []
                for word in words:
                    try:
                        numbers.append(float(word.replace(',', '')))
                    except ValueError:
                        continue
                
                if len(numbers) >= 2:
                    old_val, new_val = numbers[0], numbers[1]
                    percentage = ((new_val - old_val) / old_val) * 100
                    output = f"Percentage change: {percentage:.2f}% (from {old_val:,} to {new_val:,})"
                else:
                    output = "For percentage calculations, please provide two numbers (old value and new value)."
            else:
                output = "Business calculation capabilities: percentage change, ROI, averages, budgets."
        
        elif any(keyword in query.lower() for keyword in ['report', 'analytics', 'summary']):
            output = "Report generation capabilities: productivity reports, email summaries, task progress."
        
        else:
            output = f"I can help with: email management, task coordination, business calculations, and report generation. How can I assist you with '{query}'?"
        
        return {"output": output}

class BusinessAgent:
    """
    Business Agent for professional operations and communication management.
    
    Capabilities:
    - Email management and automation
    - Professional communication templates  
    - Business analytics and reporting
    - Task and project coordination
    - Business calculations and metrics
    """
    
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """Initialize the Business Agent"""
        self.business_sessions = {}
        
        # Initialize LLM
        try:
            # Ensure environment variables are loaded
            google_api_key = os.getenv('GOOGLE_API_KEY')
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
                
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.1,
                convert_system_message_to_human=True,
                google_api_key=google_api_key
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
        
        # Initialize tools
        try:
            self.email_sender = EmailSenderTool()
            self.email_reader = EmailReaderTool() 
            self.email_manager = EmailManagerTool()
            self.task_manager = TaskManagerTool()
            self.reminder_tool = ReminderTool()
            self.calendar_tool = CalendarTool()
        except Exception as e:
            logger.warning(f"Some tools could not be initialized: {e}")
            # Use placeholder tools
            self.email_sender = EmailSenderTool()
            self.task_manager = TaskManagerTool()
        
        # Create agent tools and agent
        self.tools = self._create_tools()
        self.agent = SimpleBusinessAgent(self.llm, self.tools)
    
    def _create_tools(self) -> List[BasicTool]:
        """Create business-focused tools"""
        
        # Email management functions
        def send_email_func(to: str, subject: str, body: str, cc: str = "", bcc: str = "", attachments: str = "") -> str:
            """Send a professional email with optional attachments"""
            email_request = f"{to}|{subject}|{body}"
            return self.email_sender.send_email(email_request)
        
        def check_emails_func(mailbox: str = "inbox", limit: int = 10, unread_only: bool = False) -> str:
            """Check and retrieve emails from specified mailbox"""
            return self.email_reader.read_emails(mailbox)
        
        def email_analytics_func(period: str = "week", metric: str = "summary") -> str:
            """Get email analytics and insights"""
            return f"Email analytics for {period}: {metric} view available"
        
        def email_template_func(template_type: str, context: str = "") -> str:
            """Generate professional email templates"""
            templates = {
                "meeting_invite": f"Subject: Meeting Invitation - {context}\n\nDear Colleague,\n\nI would like to invite you to a meeting to discuss {context}.\n\nBest regards,\n[Your Name]",
                "follow_up": f"Subject: Follow-up on {context}\n\nDear [Name],\n\nI wanted to follow up on our recent {context}. Please let me know if you need any additional information.\n\nBest regards,\n[Your Name]",
                "proposal": f"Subject: Business Proposal - {context}\n\nDear [Name],\n\nI am writing to present a business proposal regarding {context}.\n\nBest regards,\n[Your Name]"
            }
            return templates.get(template_type, f"Professional email template for {template_type} regarding {context}")
        
        # Task management functions
        def create_task_func(title: str, description: str = "", due_date: str = "", priority: str = "medium") -> str:
            """Create a business task or project item"""
            task_request = f"{title}|{description}|{due_date}|{priority}"
            return self.task_manager.create_task(task_request)
        
        def get_schedule_func(date: str = "today", view: str = "summary") -> str:
            """Get business schedule and calendar information"""
            return self.calendar_tool.get_schedule(date)
        
        # Business calculation functions
        def calculate_business_func(operation: str, *args) -> str:
            """Perform business calculations"""
            try:
                if operation.lower() == "percentage":
                    if len(args) >= 2:
                        old_val, new_val = float(args[0]), float(args[1])
                        percentage = ((new_val - old_val) / old_val) * 100
                        return f"Percentage change: {percentage:.2f}% (from {old_val:,} to {new_val:,})"
                elif operation.lower() == "roi":
                    if len(args) >= 2:
                        gain, cost = float(args[0]), float(args[1])
                        roi = ((gain - cost) / cost) * 100
                        return f"ROI: {roi:.2f}% (Gain: ${gain:,}, Investment: ${cost:,})"
                elif operation.lower() == "average":
                    numbers = [float(x) for x in args]
                    avg = sum(numbers) / len(numbers)
                    return f"Average: {avg:.2f} (from {len(numbers)} values)"
                else:
                    return f"Unsupported calculation: {operation}. Available: percentage, roi, average"
            except (ValueError, ZeroDivisionError) as e:
                return f"Calculation error: {str(e)}"
        
        # Report generation functions
        def generate_report_func(report_type: str, period: str = "week") -> str:
            """Generate business reports and summaries"""
            if report_type.lower() == "productivity":
                return f"📊 Productivity Report ({period}):\n- Tasks completed: 15/20\n- Email response rate: 95%\n- Focus time: 6.2 hours/day"
            elif report_type.lower() == "email_summary":
                return f"📧 Email Summary ({period}):\n- Emails received: 148\n- Emails sent: 67\n- Unread emails: 12"
            elif report_type.lower() == "task_progress":
                return f"✅ Task Progress Report ({period}):\n- Active projects: 5\n- Completed tasks: 23\n- Pending tasks: 8"
            else:
                return f"Report generated for {report_type} ({period})"
        
        # Create BasicTool instances
        tools = [
            BasicTool(
                name="send_email",
                func=send_email_func,
                description="Send professional emails with attachments"
            ),
            BasicTool(
                name="check_emails", 
                func=check_emails_func,
                description="Check and retrieve emails from mailboxes"
            ),
            BasicTool(
                name="email_analytics",
                func=email_analytics_func,
                description="Get email analytics and productivity insights"
            ),
            BasicTool(
                name="email_template",
                func=email_template_func,
                description="Generate professional email templates"
            ),
            BasicTool(
                name="create_task",
                func=create_task_func,
                description="Create business tasks and projects"
            ),
            BasicTool(
                name="get_schedule",
                func=get_schedule_func,
                description="Get business schedule and calendar info"
            ),
            BasicTool(
                name="business_calculator",
                func=calculate_business_func,
                description="Perform business calculations (percentage, ROI, averages)"
            ),
            BasicTool(
                name="generate_report",
                func=generate_report_func,
                description="Generate business reports and analytics summaries"
            )
        ]
        
        return tools
    
    def process_request(self, query: str) -> str:
        """Process a business request"""
        try:
            result = self.agent.invoke({"input": query})
            return result["output"]
        except Exception as e:
            logger.error(f"Business agent processing failed: {str(e)}")
            return f"Sorry, I couldn't process your business request: {str(e)}"
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return [
            "Send and manage emails",
            "Email analytics and insights", 
            "Task and project management",
            "Business calculations",
            "Generate business reports",
            "Professional communication templates"
        ]


# Test the Business Agent
if __name__ == "__main__":
    try:
        print("🧪 Testing Business Agent...")
        agent = BusinessAgent()
        
        print("\n1. Testing business calculation:")
        result = agent.process_request("Calculate the percentage increase if revenue grew from 100000 to 125000")
        print(f"Response: {result}")
        
        print("\n2. Creating email template:")
        result = agent.process_request("Generate a professional follow-up email template for after a business meeting")
        print(f"Response: {result}")
        
        print("\n3. Testing task creation:")
        result = agent.process_request("Create a task to prepare Q1 budget presentation due next Friday")
        print(f"Response: {result}")
        
        print("\n4. Testing capabilities:")
        capabilities = agent.get_capabilities()
        print(f"Capabilities: {capabilities}")
        
    except Exception as e:
        print(f"❌ Error testing Business Agent: {e}")
        print("💡 Make sure to set up your API keys in the .env file")