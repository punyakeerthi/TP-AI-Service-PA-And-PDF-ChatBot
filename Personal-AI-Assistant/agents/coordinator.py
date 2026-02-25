"""
🎛️ Coordinator Agent
====================
Master coordinator for all AI agents and multi-agent workflows.
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

# Import all specialist agents
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """
    🎛️ Coordinator Agent
    
    Master coordinator that manages all specialist agents and routes requests
    to the most appropriate agent based on the user's needs.
    """
    
    def __init__(self, llm=None):
        self.name = "Coordinator Agent"
        self.role = "Multi-Agent System Coordinator"
        self.description = "Routes requests to appropriate specialist agents and coordinates multi-agent workflows"
        
        # Initialize LLM
        if llm is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key is required for Coordinator Agent")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.6
            )
        else:
            self.llm = llm
        
        # Initialize specialist agents (lazy loading to avoid circular imports)
        self.agents = {}
        self.agent_status = {}
        
        # Request routing history
        self.request_history = []
        self.collaboration_sessions = {}
        
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
    
    def _lazy_load_agents(self):
        """Lazy load specialist agents when needed"""
        if not self.agents:
            try:
                from task_manager import TaskManagerAgent
                from research_agent import ResearchAgent
                from business_agent import BusinessAgent
                from data_agent import DataAgent
                
                self.agents["task_manager"] = TaskManagerAgent(self.llm)
                self.agents["research"] = ResearchAgent(self.llm)
                self.agents["business"] = BusinessAgent(self.llm)
                self.agents["data"] = DataAgent(self.llm)
                
                # Update status
                for agent_name, agent in self.agents.items():
                    self.agent_status[agent_name] = agent.get_status()
                    
                logger.info("All specialist agents loaded successfully")
                
            except Exception as e:
                logger.error(f"Error loading specialist agents: {e}")
                # Create mock agents for demonstration
                self.agents = {
                    "task_manager": None,
                    "research": None,
                    "business": None,
                    "data": None
                }
    
    def _create_tools(self):
        """Create the coordinator's tools"""
        
        @tool
        def route_request(request: str, preferred_agent: str = "") -> str:
            """Route user request to the most appropriate specialist agent.
            
            Args:
                request: User's request or question
                preferred_agent: Preferred agent (task_manager, research, business, data)
                
            Returns:
                Response from the appropriate specialist agent
            """
            # Determine best agent for the request
            if preferred_agent and preferred_agent in ["task_manager", "research", "business", "data"]:
                target_agent = preferred_agent
            else:
                target_agent = self._determine_best_agent(request)
            
            # Load agents if not already loaded
            self._lazy_load_agents()
            
            # Route to specialist agent
            if target_agent in self.agents and self.agents[target_agent]:
                try:
                    result = self.agents[target_agent].process_request(request)
                    
                    # Log the routing decision
                    self.request_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "request": request[:100] + "..." if len(request) > 100 else request,
                        "routed_to": target_agent,
                        "success": result.get("success", False)
                    })
                    
                    if result.get("success"):
                        return f"""
🎛️ **Routed to {target_agent.title().replace('_', ' ')} Agent**

{result['response']}

---
*Processed by: {result.get('agent', target_agent)} | {datetime.now().strftime('%H:%M:%S')}*
"""
                    else:
                        return f"❌ Error from {target_agent} agent: {result.get('error', 'Unknown error')}"
                        
                except Exception as e:
                    return f"❌ Error routing to {target_agent} agent: {str(e)}"
            else:
                return self._handle_without_specialist(request, target_agent)
        
        @tool
        def get_agent_status(agent_name: str = "") -> str:
            """Get status of specialist agents.
            
            Args:
                agent_name: Specific agent name (optional, shows all if not provided)
                
            Returns:
                Agent status information
            """
            self._lazy_load_agents()
            
            if agent_name and agent_name in self.agents:
                if self.agents[agent_name]:
                    status = self.agents[agent_name].get_status()
                    return f"""
📊 **{status['name']} Status**

🎯 **Role:** {status['role']}
📝 **Description:** {status['description']}
⚡ **Status:** {status['status']}
🛠️ **Tools:** {status['tools_count']} available
📅 **Last Activity:** {status['last_activity']}

🔧 **Capabilities:**
{chr(10).join(f'• {capability}' for capability in status.get('capabilities', []))}
"""
                else:
                    return f"❌ {agent_name} agent is not available"
            
            else:
                # Show all agents
                status_report = "🎛️ **Multi-Agent System Status**\n\n"
                
                for name, agent in self.agents.items():
                    if agent:
                        status = agent.get_status()
                        status_report += f"**{status['name']}** ✅\n"
                        status_report += f"- Role: {status['role']}\n"
                        status_report += f"- Tools: {status['tools_count']}\n"
                        status_report += f"- Status: {status['status']}\n\n"
                    else:
                        status_report += f"**{name.title().replace('_', ' ')} Agent** ❌\n"
                        status_report += f"- Status: Not available\n\n"
                
                return status_report
        
        @tool
        def start_collaboration(project_name: str, agents_needed: str, objective: str) -> str:
            """Start a collaborative session between multiple agents.
            
            Args:
                project_name: Name of the collaborative project
                agents_needed: Comma-separated list of agents needed
                objective: Project objective and goals
                
            Returns:
                Collaboration session start confirmation
            """
            session_id = f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            agents_list = [agent.strip() for agent in agents_needed.split(",")]
            
            session_data = {
                "id": session_id,
                "project_name": project_name,
                "objective": objective,
                "agents_involved": agents_list,
                "started_at": datetime.now().isoformat(),
                "status": "active",
                "tasks": [],
                "results": {},
                "coordination_notes": []
            }
            
            self.collaboration_sessions[session_id] = session_data
            
            return f"""
🤝 **Multi-Agent Collaboration Started**

📋 **Session ID:** {session_id}
🎯 **Project:** {project_name}
📝 **Objective:** {objective}
👥 **Agents Involved:** {', '.join(agents_list)}
⏰ **Started:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

✅ **Collaboration session is now active!**

💡 **Next Steps:**
1. Define specific tasks for each agent
2. Coordinate data and information sharing
3. Monitor progress and adjust as needed
4. Compile final results and insights

🎛️ **Use coordination commands to manage the collaboration workflow.**
"""
        
        @tool
        def coordinate_task(session_id: str, task_description: str, assigned_agent: str, dependencies: str = "") -> str:
            """Coordinate a specific task within a collaboration session.
            
            Args:
                session_id: Collaboration session ID
                task_description: Description of the task
                assigned_agent: Agent assigned to the task
                dependencies: Dependencies on other tasks
                
            Returns:
                Task coordination result
            """
            if session_id not in self.collaboration_sessions:
                return f"❌ Collaboration session '{session_id}' not found."
            
            session = self.collaboration_sessions[session_id]
            
            # Route the task to the assigned agent
            if assigned_agent in ["task_manager", "research", "business", "data"]:
                self._lazy_load_agents()
                
                if self.agents.get(assigned_agent):
                    result = self.agents[assigned_agent].process_request(task_description)
                    
                    # Record the task in the session
                    task_record = {
                        "task_id": f"task_{len(session['tasks']) + 1}",
                        "description": task_description,
                        "assigned_agent": assigned_agent,
                        "dependencies": dependencies,
                        "status": "completed" if result.get("success") else "failed",
                        "result": result.get("response", result.get("error")),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    session["tasks"].append(task_record)
                    session["results"][assigned_agent] = result
                    
                    return f"""
🎛️ **Task Coordinated Successfully**

📋 **Session:** {session['project_name']}
🎯 **Task:** {task_description[:100]}...
🤖 **Agent:** {assigned_agent.title().replace('_', ' ')} Agent
✅ **Status:** {task_record['status']}

📝 **Result:**
{result.get("response", result.get("error"))}

📊 **Session Progress:** {len(session['tasks'])} tasks completed
"""
                else:
                    return f"❌ {assigned_agent} agent is not available for task coordination."
            else:
                return f"❌ Unknown agent: {assigned_agent}"
        
        @tool
        def get_collaboration_summary(session_id: str = "") -> str:
            """Get summary of collaboration session(s).
            
            Args:
                session_id: Specific session ID (optional)
                
            Returns:
                Collaboration session summary
            """
            if session_id and session_id in self.collaboration_sessions:
                session = self.collaboration_sessions[session_id]
                
                summary = f"""
🤝 **Collaboration Session Summary**

📋 **Project:** {session['project_name']}
🎯 **Objective:** {session['objective']}
👥 **Agents:** {', '.join(session['agents_involved'])}
⏰ **Duration:** {self._calculate_session_duration(session['started_at'])}
📊 **Status:** {session['status']}

🎯 **Tasks Completed:** {len(session['tasks'])}

📝 **Recent Tasks:**
"""
                
                for task in session['tasks'][-5:]:  # Last 5 tasks
                    summary += f"• {task['description'][:80]}... [{task['assigned_agent']}] - {task['status']}\n"
                
                if session.get('coordination_notes'):
                    summary += f"\n📋 **Coordination Notes:**\n"
                    for note in session['coordination_notes'][-3:]:
                        summary += f"• {note}\n"
                
                return summary
            
            elif not session_id and self.collaboration_sessions:
                # Show all sessions
                summary = "🤝 **All Collaboration Sessions:**\n\n"
                for sid, session in self.collaboration_sessions.items():
                    summary += f"**{session['project_name']}** (ID: {sid})\n"
                    summary += f"- Status: {session['status']}\n"
                    summary += f"- Agents: {len(session['agents_involved'])}\n"
                    summary += f"- Tasks: {len(session['tasks'])}\n"
                    summary += f"- Started: {session['started_at'][:19]}\n\n"
                return summary
            
            else:
                return "📭 No collaboration sessions found. Start a new session to coordinate multi-agent work."
        
        @tool
        def get_system_overview() -> str:
            """Get comprehensive overview of the multi-agent system.
            
            Returns:
                System status and capabilities overview
            """
            self._lazy_load_agents()
            
            total_tools = sum(agent.get_status()['tools_count'] for agent in self.agents.values() if agent)
            active_agents = sum(1 for agent in self.agents.values() if agent)
            recent_requests = len([r for r in self.request_history if 
                                 (datetime.now() - datetime.fromisoformat(r['timestamp'])).hours < 24])
            active_collaborations = len([s for s in self.collaboration_sessions.values() if s['status'] == 'active'])
            
            overview = f"""
🎛️ **Personal AI Assistant - System Overview**

📊 **System Status:**
- Total Agents: {len(self.agents)} ({active_agents} active)
- Total Tools: {total_tools}
- Requests Today: {recent_requests}
- Active Collaborations: {active_collaborations}
- System Uptime: ✅ Operational

🤖 **Specialist Agents:**

🎯 **Task Manager Agent**
- Focus: Productivity, task management, goal tracking
- Tools: Task creation, Pomodoro timer, habit tracking
- Status: {'✅ Active' if self.agents.get('task_manager') else '❌ Offline'}

🔍 **Research Agent**
- Focus: Information gathering, web research, analysis
- Tools: Web search, data analysis, report generation
- Status: {'✅ Active' if self.agents.get('research') else '❌ Offline'}

💼 **Business Agent**
- Focus: Email management, business operations
- Tools: Email handling, templates, business analytics
- Status: {'✅ Active' if self.agents.get('business') else '❌ Offline'}

📊 **Data Agent**
- Focus: Data analysis, statistics, visualizations
- Tools: File analysis, charts, statistical computing
- Status: {'✅ Active' if self.agents.get('data') else '❌ Offline'}

🎛️ **Coordinator Agent**
- Focus: Multi-agent coordination and routing
- Tools: Request routing, collaboration management
- Status: ✅ Active (You're using it now!)

💡 **Quick Commands:**
- "Help me with [task/productivity]" → Task Manager
- "Research [topic]" → Research Agent
- "Send an email to..." → Business Agent
- "Analyze this data..." → Data Agent
- "Start a collaboration on..." → Multi-Agent

🚀 **Ready to assist with any task across all domains!**
"""
            
            return overview
        
        return [
            route_request, get_agent_status, start_collaboration,
            coordinate_task, get_collaboration_summary, get_system_overview
        ]
    
    def _determine_best_agent(self, request: str) -> str:
        """Determine the best agent for handling a request"""
        request_lower = request.lower()
        
        # Task management keywords
        task_keywords = [
            "task", "todo", "reminder", "deadline", "schedule", "productivity",
            "goal", "habit", "pomodoro", "timer", "organize", "priority"
        ]
        
        # Research keywords
        research_keywords = [
            "search", "research", "find", "information", "news", "investigate",
            "study", "analyze", "explore", "discover", "report"
        ]
        
        # Business keywords
        business_keywords = [
            "email", "send", "reply", "business", "meeting", "professional",
            "communication", "template", "schedule", "contact", "follow up"
        ]
        
        # Data keywords
        data_keywords = [
            "data", "csv", "excel", "chart", "graph", "statistics", "analysis",
            "visualization", "calculate", "numbers", "dataset", "correlation"
        ]
        
        # Count keyword matches
        scores = {
            "task_manager": sum(1 for keyword in task_keywords if keyword in request_lower),
            "research": sum(1 for keyword in research_keywords if keyword in request_lower),
            "business": sum(1 for keyword in business_keywords if keyword in request_lower),
            "data": sum(1 for keyword in data_keywords if keyword in request_lower)
        }
        
        # Return agent with highest score, default to task manager
        best_agent = max(scores, key=scores.get)
        
        # If no clear winner, use context clues
        if scores[best_agent] == 0:
            if any(word in request_lower for word in ["help", "what", "how"]):
                return "task_manager"  # General help goes to task manager
            else:
                return "research"  # Unknown requests go to research
        
        return best_agent
    
    def _handle_without_specialist(self, request: str, intended_agent: str) -> str:
        """Handle requests when specialist agents are not available"""
        return f"""
🎛️ **Coordinator Agent Response**

❌ **Specialist Agent Unavailable**
The {intended_agent.title().replace('_', ' ')} Agent is currently not available to handle your request.

📝 **Your Request:** {request[:150]}...

💡 **Alternative Options:**
1. I can provide general guidance on your request
2. The request can be queued for when the agent becomes available
3. You can try rephrasing your request for a different type of assistance

🛠️ **Available Coordination Services:**
- Request routing and planning
- Multi-agent workflow coordination
- System status and monitoring
- General task breakdown and guidance

Would you like me to help break down your request or provide general guidance?

---
*Coordinator Agent | {datetime.now().strftime('%H:%M:%S')}*
"""
    
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
        """Create the coordinator agent"""
        system_message = """You are the Coordinator Agent for a sophisticated multi-agent AI system. You serve as the central hub that routes requests to specialist agents and manages complex multi-agent workflows.

🎛️ **Your Role & Responsibilities:**
- You are the system coordinator and traffic controller
- Route user requests to the most appropriate specialist agents
- Manage multi-agent collaborations and workflows
- Monitor system status and agent performance
- Provide system overview and guidance
- Coordinate complex tasks that require multiple agents

🤖 **Your Specialist Team:**
1. **Task Manager Agent**: Productivity, task management, goal tracking, habit formation
2. **Research Agent**: Information gathering, web research, data analysis, reporting  
3. **Business Agent**: Email management, professional communications, business operations
4. **Data Agent**: Data analysis, statistics, visualizations, file processing

🎯 **Coordination Excellence:**
- Analyze user requests to determine the best agent match
- Route requests efficiently to specialist agents
- Coordinate multi-agent collaborations when needed
- Track request history and system performance
- Provide clear feedback on agent assignments and results

🔄 **Multi-Agent Workflow Management:**
- Start collaboration sessions for complex projects
- Assign specific tasks to appropriate specialist agents
- Monitor progress across multiple agents
- Compile and synthesize results from different agents
- Manage dependencies and task sequencing

📊 **System Monitoring:**
- Track agent status and availability
- Monitor request routing efficiency
- Identify patterns in user requests
- Suggest system optimizations
- Provide comprehensive system overviews

💡 **Intelligent Routing Logic:**
- Analyze request content and intent
- Consider agent capabilities and current load
- Route to most appropriate specialist
- Fall back gracefully when agents unavailable
- Suggest alternative approaches when needed

🗣️ **Communication Style:**
- Be clear about routing decisions
- Explain which agent is handling what
- Provide context for multi-agent workflows
- Keep users informed of coordination progress
- Offer guidance on system capabilities

🚀 **Coordination Principles:**
- Maximize the strengths of each specialist agent
- Minimize redundancy and optimize efficiency
- Provide seamless user experience across agents
- Enable complex multi-agent problem solving
- Ensure users get the most appropriate help

Remember: You are the conductor of this AI orchestra. Your job is to ensure each user request gets to the right specialist agent and that complex tasks are broken down and coordinated effectively across the team."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_tool_calling_agent(self.llm, self.tools, prompt)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user request through the coordinator
        
        Args:
            user_input: User's request or question
            
        Returns:
            Coordinated response from appropriate agent(s)
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
            logger.error(f"Coordinator Agent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current coordinator status"""
        self._lazy_load_agents()
        
        active_agents = sum(1 for agent in self.agents.values() if agent)
        total_requests = len(self.request_history)
        active_collaborations = len([s for s in self.collaboration_sessions.values() if s['status'] == 'active'])
        
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "status": "active",
            "tools_count": len(self.tools),
            "specialist_agents": len(self.agents),
            "active_agents": active_agents,
            "total_requests": total_requests,
            "active_collaborations": active_collaborations,
            "capabilities": [
                "Request Routing",
                "Multi-Agent Coordination",
                "System Monitoring",
                "Workflow Management",
                "Agent Status Tracking"
            ],
            "last_activity": datetime.now().isoformat()
        }

# Example usage and testing
if __name__ == "__main__":
    print("🎛️ Testing Coordinator Agent...")
    
    try:
        # Create coordinator
        coordinator = CoordinatorAgent()
        
        # Test basic functionality
        print("\n1. System Overview:")
        result = coordinator.process_request("Show me the system overview")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n2. Agent Status:")
        result = coordinator.process_request("What's the status of all agents?")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n3. Request Routing:")
        result = coordinator.process_request("I need help organizing my daily tasks and setting up a productivity system")
        print(f"Response: {result.get('response', result.get('error'))}")
        
    except Exception as e:
        print(f"❌ Error testing Coordinator Agent: {e}")
        print("💡 Make sure to set up your Google API key in the .env file")