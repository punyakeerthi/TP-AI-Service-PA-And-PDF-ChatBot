"""
💼 Business Agent
=================
Professional business operations and communication assistant.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import our tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.email_tools import EmailTool, EmailAnalyticsTool, EmailTemplateGenerator, EmailSchedulerTool
from tools.task_tools import TaskManagementTool
from tools.utility_tools import CalculatorTool, DateTimeTool
from tools.data_tools import ReportGeneratorTool

logger = logging.getLogger(__name__)

class BusinessAgent:
    """
    💼 Business Agent
    
    Specialized agent for business operations, email management, and professional tasks.
    Combines email management, business analytics, and professional communication tools.
    """
    
    def __init__(self, llm=None):
        self.name = "Business Agent"
        self.role = "Business Operations Manager"
        self.description = "Manages business communications, email operations, and professional workflows"
        
        # Initialize LLM
        if llm is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key is required for Business Agent")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.5  # Balanced creativity for business communications
            )
        else:
            self.llm = llm
        
        # Initialize tools
        self.email_tool = EmailTool()
        self.email_analytics_tool = EmailAnalyticsTool()
        self.email_template_tool = EmailTemplateGenerator()
        self.email_scheduler_tool = EmailSchedulerTool()
        self.task_tool = TaskManagementTool()
        self.calc_tool = CalculatorTool()
        self.datetime_tool = DateTimeTool()
        self.report_tool = ReportGeneratorTool()
        
        # Business session storage
        self.business_sessions = {}
        self.email_drafts = {}
        
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
        """Create the agent's business tools"""
        
        @tool
        def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "", attachments: str = "") -> str:
            """Send an email to specified recipients.
            
            Args:
                to: Recipient email addresses (comma-separated)
                subject: Email subject
                body: Email body content
                cc: CC recipients (comma-separated, optional)
                bcc: BCC recipients (comma-separated, optional)
                attachments: File paths to attach (comma-separated, optional)
                
            Returns:
                Email sending result
            """
            to_list = [email.strip() for email in to.split(",")]
            cc_list = [email.strip() for email in cc.split(",") if email.strip()] if cc else []
            bcc_list = [email.strip() for email in bcc.split(",") if email.strip()] if bcc else []
            attachment_list = [path.strip() for path in attachments.split(",") if path.strip()] if attachments else []
            
            return self.email_tool.send_email(to_list, subject, body, cc_list, bcc_list, attachment_list)
        
        @tool
        def check_emails(mailbox: str = "inbox", limit: int = 10, unread_only: bool = False) -> str:
            """Check and retrieve emails from mailbox.
            
            Args:
                mailbox: Mailbox to check (inbox, sent, trash, drafts)
                limit: Number of emails to retrieve
                unread_only: Only show unread emails
                
            Returns:
                List of emails with details
            """
            return self.email_tool.check_emails(mailbox, limit, unread_only)
        
        @tool
        def reply_to_email(email_id: str, reply_body: str, reply_all: bool = False) -> str:
            """Reply to a specific email.
            
            Args:
                email_id: ID of the email to reply to
                reply_body: Reply message content
                reply_all: Whether to reply to all recipients
                
            Returns:
                Reply sending result
            """
            return self.email_tool.reply_to_email(email_id, reply_body, reply_all)
        
        @tool
        def forward_email(email_id: str, to: str, message: str = "") -> str:
            """Forward an email to specified recipients.
            
            Args:
                email_id: ID of the email to forward
                to: Recipient email addresses (comma-separated)
                message: Additional message to include
                
            Returns:
                Forward result
            """
            to_list = [email.strip() for email in to.split(",")]
            return self.email_tool.forward_email(email_id, to_list, message)
        
        @tool
        def organize_emails(action: str, email_ids: str, folder: str = "", labels: str = "") -> str:
            """Organize emails by moving, labeling, or archiving.
            
            Args:
                action: Action to perform (move, label, archive, delete, mark_read, mark_unread)
                email_ids: Comma-separated list of email IDs
                folder: Target folder for move action
                labels: Comma-separated labels to apply
                
            Returns:
                Organization result
            """
            id_list = [id.strip() for id in email_ids.split(",")]
            label_list = [label.strip() for label in labels.split(",") if label.strip()] if labels else []
            
            return self.email_tool.organize_emails(action, id_list, folder, label_list)
        
        @tool
        def get_email_analytics(period: str = "week", metric: str = "summary") -> str:
            """Get email analytics and insights.
            
            Args:
                period: Analysis period (day, week, month, year)
                metric: Specific metric (summary, volume, response_time, senders)
                
            Returns:
                Email analytics report
            """
            return self.email_analytics_tool.get_analytics(period, metric)
        
        @tool
        def generate_email_template(template_type: str, context: str = "", tone: str = "professional") -> str:
            """Generate email templates for various business purposes.
            
            Args:
                template_type: Type of template (meeting_request, follow_up, proposal, thank_you, apology, introduction)
                context: Specific context or details
                tone: Email tone (professional, friendly, formal, casual)
                
            Returns:
                Generated email template
            """
            return self.email_template_tool.generate_template(template_type, context, tone)
        
        @tool
        def schedule_email(to: str, subject: str, body: str, send_time: str, cc: str = "", bcc: str = "") -> str:
            """Schedule an email to be sent later.
            
            Args:
                to: Recipient email addresses (comma-separated)
                subject: Email subject
                body: Email body content
                send_time: When to send (YYYY-MM-DD HH:MM format)
                cc: CC recipients (optional)
                bcc: BCC recipients (optional)
                
            Returns:
                Email scheduling result
            """
            to_list = [email.strip() for email in to.split(",")]
            cc_list = [email.strip() for email in cc.split(",") if email.strip()] if cc else []
            bcc_list = [email.strip() for email in bcc.split(",") if email.strip()] if bcc else []
            
            return self.email_scheduler_tool.schedule_email(to_list, subject, body, send_time, cc_list, bcc_list)
        
        @tool
        def manage_email_drafts(action: str, draft_id: str = "", subject: str = "", body: str = "") -> str:
            """Manage email drafts (create, edit, list, send, delete).
            
            Args:
                action: Action to perform (create, edit, list, send, delete)
                draft_id: Draft ID for specific operations
                subject: Draft subject (for create/edit)
                body: Draft body content (for create/edit)
                
            Returns:
                Draft management result
            """
            if action == "create":
                draft_id = f"draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.email_drafts[draft_id] = {
                    "subject": subject,
                    "body": body,
                    "created_at": datetime.now().isoformat(),
                    "modified_at": datetime.now().isoformat()
                }
                return f"✅ Draft created with ID: {draft_id}"
            
            elif action == "list":
                if not self.email_drafts:
                    return "📭 No email drafts found."
                
                draft_list = "📝 **Email Drafts:**\n\n"
                for did, draft in self.email_drafts.items():
                    created = draft["created_at"][:19]
                    draft_list += f"**{did}**\n"
                    draft_list += f"📧 Subject: {draft['subject']}\n"
                    draft_list += f"📅 Created: {created}\n\n"
                
                return draft_list
            
            elif action == "send" and draft_id in self.email_drafts:
                draft = self.email_drafts[draft_id]
                # Here you would integrate with actual email sending
                del self.email_drafts[draft_id]
                return f"📧 Draft '{draft_id}' has been sent."
            
            elif action == "delete" and draft_id in self.email_drafts:
                del self.email_drafts[draft_id]
                return f"🗑️ Draft '{draft_id}' has been deleted."
            
            else:
                return f"❌ Invalid action or draft not found: {action}"
        
        @tool
        def create_business_task(title: str, type: str = "follow_up", priority: str = "medium", due_date: str = "") -> str:
            """Create business-related tasks.
            
            Args:
                title: Task title
                type: Task type (follow_up, meeting, proposal, review, deadline)
                priority: Priority level (low, medium, high, urgent)
                due_date: Due date (YYYY-MM-DD format)
                
            Returns:
                Task creation result
            """
            description = f"Business task - Type: {type}"
            return self.task_tool.create_task(title, description, due_date, priority, "business")
        
        @tool
        def calculate_business_metrics(expression: str, metric_type: str = "general") -> str:
            """Calculate business metrics and financial calculations.
            
            Args:
                expression: Mathematical expression or calculation
                metric_type: Type of metric (general, financial, roi, percentage, growth)
                
            Returns:
                Calculation result with business context
            """
            if metric_type == "financial":
                return self.calc_tool.advanced_calculate("compound_interest", *expression.split())
            elif metric_type == "percentage":
                return self.calc_tool.advanced_calculate("percentage", *expression.split())
            else:
                result = self.calc_tool.calculate(expression)
                return f"💼 **Business Calculation:**\n\n{result}"
        
        @tool
        def get_business_schedule(date: str = "", operation: str = "today") -> str:
            """Get business schedule and time information.
            
            Args:
                date: Specific date (YYYY-MM-DD format)
                operation: Operation type (today, tomorrow, this_week, time_to)
                
            Returns:
                Schedule information
            """
            if operation == "today":
                return self.datetime_tool.get_current_datetime()
            elif operation == "time_to" and date:
                current_date = datetime.now().strftime("%Y-%m-%d")
                return self.datetime_tool.calculate_date_difference(current_date, date)
            else:
                return self.datetime_tool.get_current_datetime()
        
        @tool
        def generate_business_report(report_type: str, data_source: str = "", format_type: str = "markdown") -> str:
            """Generate business reports and summaries.
            
            Args:
                report_type: Type of report (email_summary, task_progress, analytics, general)
                data_source: Data source for the report
                format_type: Output format (markdown, html, pdf)
                
            Returns:
                Generated business report
            """
            if report_type == "email_summary":
                analytics = self.email_analytics_tool.get_analytics("week", "summary")
                return f"📊 **Weekly Email Summary Report**\n\n{analytics}"
            
            elif report_type == "task_progress":
                tasks = self.task_tool.get_productivity_stats()
                return f"📈 **Task Progress Report**\n\n{tasks}"
            
            else:
                return self.report_tool.generate_report(f"Business {report_type}", [], format_type)
        
        @tool
        def start_business_session(session_type: str, topic: str, participants: str = "") -> str:
            """Start a business session (meeting, project, review).
            
            Args:
                session_type: Type of session (meeting, project, review, planning)
                topic: Session topic or title
                participants: Participant emails (comma-separated)
                
            Returns:
                Session start confirmation
            """
            session_id = f"{session_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            session_data = {
                "id": session_id,
                "type": session_type,
                "topic": topic,
                "participants": [p.strip() for p in participants.split(",") if p.strip()],
                "started_at": datetime.now().isoformat(),
                "notes": [],
                "action_items": [],
                "status": "active"
            }
            
            self.business_sessions[session_id] = session_data
            
            return f"""
💼 **Business Session Started**

📋 **Session ID:** {session_id}
📊 **Type:** {session_type.title()}
🎯 **Topic:** {topic}
👥 **Participants:** {len(session_data['participants'])} people
⏰ **Started:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

✅ **Session is now active!** You can add notes and action items.

💡 **Available Commands:**
- Add notes and observations
- Create action items and follow-ups
- Generate meeting summaries
- Send follow-up emails to participants
"""
        
        return [
            send_email, check_emails, reply_to_email, forward_email, organize_emails,
            get_email_analytics, generate_email_template, schedule_email, manage_email_drafts,
            create_business_task, calculate_business_metrics, get_business_schedule,
            generate_business_report, start_business_session
        ]
    
    def _create_agent(self):
        """Create the business agent"""
        system_message = """You are a sophisticated Business Agent, designed to streamline professional operations, communications, and business workflows. You excel at email management, business analytics, and professional task coordination.

💼 **Your Role & Personality:**
- You are a professional business operations manager
- Be efficient, organized, and results-oriented
- Maintain professional communication standards
- Help users optimize their business workflows
- Focus on productivity and effective communication

🛠️ **Your Core Capabilities:**
1. **Email Management**: Send, organize, reply, schedule emails
2. **Communication Templates**: Professional email templates for various purposes
3. **Business Analytics**: Email insights, productivity metrics, reporting
4. **Task Coordination**: Business task management and follow-ups
5. **Schedule Management**: Time planning, deadline tracking, meeting coordination
6. **Business Calculations**: Financial metrics, ROI, growth calculations
7. **Report Generation**: Business summaries, analytics reports, progress tracking

📧 **Email Management Excellence:**
- Help draft professional communications
- Organize email workflows efficiently
- Provide email analytics and insights
- Schedule and manage email campaigns
- Create templates for common business scenarios

💼 **Business Operations Focus:**
- Streamline repetitive business tasks
- Track important deadlines and follow-ups
- Coordinate meetings and project sessions
- Generate business reports and summaries
- Calculate business metrics and KPIs

📊 **Professional Communication Standards:**
- Use appropriate business language and tone
- Follow email etiquette best practices
- Maintain confidentiality and professionalism
- Suggest improvements to communication workflows
- Help create clear, actionable messages

🎯 **Productivity Optimization:**
- Identify workflow bottlenecks and solutions
- Suggest automation opportunities
- Track business task progress and deadlines
- Provide analytics on communication patterns
- Help prioritize business activities

💡 **Proactive Business Support:**
- Suggest follow-up actions after meetings
- Remind about important deadlines
- Identify trends in business communications
- Recommend process improvements
- Help maintain professional relationships

🗣️ **Communication Style:**
- Professional and business-appropriate
- Clear and action-oriented
- Provide specific, actionable recommendations
- Use business terminology appropriately
- Focus on efficiency and results

Remember: Your goal is to help users excel in their professional communications and business operations. Always maintain high standards of professionalism while maximizing efficiency and effectiveness."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_tool_calling_agent(self.llm, self.tools, prompt)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user business request and return response
        
        Args:
            user_input: User's business request or question
            
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
            logger.error(f"Business Agent error: {e}")
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
            "active_sessions": len(self.business_sessions),
            "email_drafts": len(self.email_drafts),
            "capabilities": [
                "Email Management",
                "Business Communications",
                "Email Analytics",
                "Template Generation",
                "Task Coordination",
                "Business Calculations",
                "Report Generation",
                "Schedule Management"
            ],
            "last_activity": datetime.now().isoformat()
        }
    
    def get_business_overview(self) -> str:
        """Get quick business agent overview"""
        try:
            active_sessions = len(self.business_sessions)
            email_drafts = len(self.email_drafts)
            
            return f"""
💼 **Business Agent - Quick Overview**

📅 **Current Status:**
- Agent: {self.name}
- Role: {self.role}
- Status: Active and Ready
- Active Business Sessions: {active_sessions}
- Email Drafts: {email_drafts}

🛠️ **Business Operations:**
- Email Management & Organization
- Professional Communication Templates
- Email Analytics & Insights
- Business Task Coordination
- Meeting & Session Management
- Financial Calculations & Metrics
- Business Report Generation
- Schedule & Deadline Tracking

📧 **Email Capabilities:**
- Send/Reply/Forward emails
- Email organization and labeling
- Template generation for business scenarios
- Email scheduling and automation
- Analytics and communication insights

💼 **Business Tools Available:**
- Email Client Integration
- Communication Templates
- Business Calculator
- Report Generator
- Task Manager
- Schedule Coordinator
- Analytics Dashboard

💡 **Quick Business Commands:**
- "Send an email to [recipient]"
- "Check my inbox for new messages"
- "Generate a meeting follow-up template"
- "Schedule an email for tomorrow"
- "Show my email analytics"
- "Create a business report"
- "Start a meeting session"

🚀 **Ready to optimize your business operations!**
"""
            
        except Exception as e:
            return f"Business Agent Status: Active (Stats error: {str(e)})"

# Example usage and testing
if __name__ == "__main__":
    print("💼 Testing Business Agent...")
    
    try:
        # Create agent
        agent = BusinessAgent()
        
        # Test basic functionality
        print("\n1. Agent Status:")
        print(agent.get_business_overview())
        
        print("\n2. Creating email template:")
        result = agent.process_request("Generate a professional follow-up email template for after a business meeting")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n3. Starting business session:")
        result = agent.process_request("Start a project planning session for Q1 2024 strategy")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n4. Business calculation:")
        result = agent.process_request("Calculate the percentage increase if revenue grew from 100000 to 125000")
        print(f"Response: {result.get('response', result.get('error'))}")
        
    except Exception as e:
        print(f"❌ Error testing Business Agent: {e}")
        print("💡 Make sure to set up your API keys in the .env file")