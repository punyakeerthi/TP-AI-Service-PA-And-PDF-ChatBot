"""
🎯 Task Manager Agent
====================
Intelligent task management and productivity assistant.
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
from tools.task_tools import TaskManagementTool, PomodoroTool, HabitTrackerTool, GoalTrackerTool
from tools.utility_tools import CalculatorTool, DateTimeTool

logger = logging.getLogger(__name__)

class TaskManagerAgent:
    """
    🎯 Task Manager Agent
    
    Specialized agent for task management, productivity tracking, and goal achievement.
    Combines task management, pomodoro technique, habit tracking, and goal tracking tools.
    """
    
    def __init__(self, llm=None):
        self.name = "Task Manager Agent"
        self.role = "Personal Productivity Assistant"
        self.description = "Manages tasks, tracks goals, monitors habits, and optimizes productivity"
        
        # Initialize LLM
        if llm is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key is required for Task Manager Agent")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
        else:
            self.llm = llm
        
        # Initialize tools
        self.task_tool = TaskManagementTool()
        self.pomodoro_tool = PomodoroTool()
        self.habit_tool = HabitTrackerTool()
        self.goal_tool = GoalTrackerTool()
        self.calc_tool = CalculatorTool()
        self.datetime_tool = DateTimeTool()
        
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
        """Create the agent's tools"""
        
        @tool
        def create_task(title: str, description: str = "", due_date: str = "", priority: str = "medium", category: str = "general") -> str:
            """Create a new task with specified details.
            
            Args:
                title: Task title (required)
                description: Task description
                due_date: Due date (YYYY-MM-DD format)
                priority: Priority level (low, medium, high, urgent)
                category: Task category
                
            Returns:
                Task creation result
            """
            return self.task_tool.create_task(title, description, due_date, priority, category)
        
        @tool
        def list_tasks(filter_by: str = "all") -> str:
            """List tasks with optional filtering.
            
            Args:
                filter_by: Filter criteria (all, pending, completed, overdue, today, this_week, high_priority)
                
            Returns:
                List of filtered tasks
            """
            return self.task_tool.list_tasks(filter_by)
        
        @tool
        def update_task(task_id: int, field: str, value: str) -> str:
            """Update a specific field of a task.
            
            Args:
                task_id: ID of the task to update
                field: Field to update (title, description, due_date, priority, category, status)
                value: New value for the field
                
            Returns:
                Update result
            """
            return self.task_tool.update_task(task_id, field, value)
        
        @tool
        def delete_task(task_id: int) -> str:
            """Delete a task by ID.
            
            Args:
                task_id: ID of the task to delete
                
            Returns:
                Deletion result
            """
            return self.task_tool.delete_task(task_id)
        
        @tool
        def get_productivity_stats() -> str:
            """Get productivity statistics and insights.
            
            Returns:
                Detailed productivity analysis
            """
            return self.task_tool.get_productivity_stats()
        
        @tool
        def start_pomodoro(task_description: str = "") -> str:
            """Start a Pomodoro work session.
            
            Args:
                task_description: Optional description of what you're working on
                
            Returns:
                Pomodoro session start confirmation
            """
            return self.pomodoro_tool.start_pomodoro(task_description)
        
        @tool
        def get_pomodoro_status() -> str:
            """Check current Pomodoro session status.
            
            Returns:
                Current session status and remaining time
            """
            return self.pomodoro_tool.get_session_status()
        
        @tool
        def stop_pomodoro() -> str:
            """Stop current Pomodoro session.
            
            Returns:
                Session stop confirmation and summary
            """
            return self.pomodoro_tool.stop_session()
        
        @tool
        def get_pomodoro_stats() -> str:
            """Get Pomodoro session statistics.
            
            Returns:
                Detailed session statistics
            """
            return self.pomodoro_tool.get_session_stats()
        
        @tool
        def add_habit(name: str, description: str = "", frequency: str = "daily") -> str:
            """Add a new habit to track.
            
            Args:
                name: Habit name
                description: Habit description
                frequency: Frequency (daily, weekly, monthly)
                
            Returns:
                Habit creation result
            """
            return self.habit_tool.add_habit(name, description, frequency)
        
        @tool
        def record_habit(habit_id: int, completed: bool = True, notes: str = "") -> str:
            """Record habit completion for today.
            
            Args:
                habit_id: ID of the habit
                completed: Whether habit was completed
                notes: Optional notes
                
            Returns:
                Recording result
            """
            return self.habit_tool.record_habit(habit_id, completed, notes)
        
        @tool
        def get_habit_progress(habit_id: int = None, days: int = 30) -> str:
            """Get habit progress and statistics.
            
            Args:
                habit_id: Specific habit ID (optional, shows all if not provided)
                days: Number of days to analyze
                
            Returns:
                Habit progress analysis
            """
            return self.habit_tool.get_habit_progress(habit_id, days)
        
        @tool
        def create_goal(title: str, description: str = "", deadline: str = "", category: str = "personal") -> str:
            """Create a new goal to track.
            
            Args:
                title: Goal title
                description: Goal description
                deadline: Goal deadline (YYYY-MM-DD format)
                category: Goal category
                
            Returns:
                Goal creation result
            """
            return self.goal_tool.create_goal(title, description, deadline, category)
        
        @tool
        def update_goal_progress(goal_id: int, progress_percentage: int, notes: str = "") -> str:
            """Update progress on a goal.
            
            Args:
                goal_id: ID of the goal
                progress_percentage: Current progress (0-100)
                notes: Progress notes
                
            Returns:
                Progress update result
            """
            return self.goal_tool.update_goal_progress(goal_id, progress_percentage, notes)
        
        @tool
        def get_goal_dashboard() -> str:
            """Get comprehensive goal dashboard and analytics.
            
            Returns:
                Goal progress dashboard
            """
            return self.goal_tool.get_goal_dashboard()
        
        @tool
        def calculate_productivity_metrics(expression: str) -> str:
            """Calculate productivity-related metrics and statistics.
            
            Args:
                expression: Mathematical expression to calculate
                
            Returns:
                Calculation result
            """
            return self.calc_tool.calculate(expression)
        
        @tool
        def get_time_information(operation: str = "current", date1: str = "", date2: str = "") -> str:
            """Get time-related information and calculations.
            
            Args:
                operation: Operation type ('current', 'difference', 'add')
                date1: First date (for operations)
                date2: Second date (for difference calculations)
                
            Returns:
                Time information or calculation result
            """
            if operation == "current":
                return self.datetime_tool.get_current_datetime()
            elif operation == "difference" and date1 and date2:
                return self.datetime_tool.calculate_date_difference(date1, date2)
            else:
                return "Please specify valid operation and required dates."
        
        return [
            create_task, list_tasks, update_task, delete_task, get_productivity_stats,
            start_pomodoro, get_pomodoro_status, stop_pomodoro, get_pomodoro_stats,
            add_habit, record_habit, get_habit_progress,
            create_goal, update_goal_progress, get_goal_dashboard,
            calculate_productivity_metrics, get_time_information
        ]
    
    def _create_agent(self):
        """Create the task manager agent"""
        system_message = """You are a highly intelligent and supportive Task Manager Agent, designed to help users achieve maximum productivity and reach their goals.

🎯 **Your Role & Personality:**
- You are a personal productivity coach and task manager
- Be encouraging, motivational, and positive
- Provide actionable insights and suggestions
- Help users build sustainable productivity habits
- Focus on goal achievement and continuous improvement

🛠️ **Your Capabilities:**
1. **Task Management**: Create, organize, prioritize, and track tasks
2. **Time Management**: Pomodoro technique, time tracking, scheduling
3. **Habit Formation**: Track habits, build routines, monitor streaks
4. **Goal Achievement**: Set SMART goals, track progress, provide milestones
5. **Productivity Analytics**: Generate insights, identify patterns, suggest improvements

📋 **Task Management Best Practices:**
- Always ask for clarification if task details are unclear
- Suggest realistic deadlines and priorities
- Break down large tasks into smaller, manageable steps
- Recommend appropriate categories and organization
- Provide deadline reminders and progress updates

⏰ **Time & Productivity Optimization:**
- Suggest Pomodoro sessions for focused work
- Recommend optimal work schedules based on user patterns
- Help identify and eliminate time-wasting activities
- Encourage regular breaks and work-life balance

🎯 **Goal-Oriented Approach:**
- Help users set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Break goals into actionable steps and milestones
- Regularly review and adjust goal progress
- Celebrate achievements and provide motivational support

💡 **Proactive Assistance:**
- Suggest productivity improvements based on data
- Remind users of upcoming deadlines
- Identify patterns in task completion and habit formation
- Recommend new habits or routines for better productivity

🗣️ **Communication Style:**
- Be conversational and supportive
- Use emojis to make interactions engaging
- Provide clear, actionable advice
- Ask follow-up questions to better understand needs
- Offer alternatives and multiple solutions when possible

Remember: Your goal is to help users become more organized, productive, and successful in achieving their personal and professional objectives. Always focus on practical, actionable advice that users can implement immediately."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        return create_tool_calling_agent(self.llm, self.tools, prompt)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process user request and return response
        
        Args:
            user_input: User's request or question
            
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
            logger.error(f"Task Manager Agent error: {e}")
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
            "capabilities": [
                "Task Management",
                "Pomodoro Timer",
                "Habit Tracking",
                "Goal Setting",
                "Productivity Analytics",
                "Time Management",
                "Progress Tracking"
            ],
            "last_activity": datetime.now().isoformat()
        }
    
    def get_quick_stats(self) -> str:
        """Get quick productivity overview"""
        try:
            # Get counts from tools
            tasks_summary = self.task_tool.get_productivity_stats()
            goals_summary = self.goal_tool.get_goal_dashboard()
            pomodoro_summary = self.pomodoro_tool.get_session_stats()
            habits_summary = self.habit_tool.get_habit_progress()
            
            return f"""
🎯 **Task Manager Agent - Quick Overview**

📅 **Today's Status:**
- Agent: {self.name}
- Role: {self.role}
- Status: Active and Ready

🔧 **Available Tools:**
- Task Management (Create, Update, Track)
- Pomodoro Timer (Focus Sessions)
- Habit Tracker (Build Routines)
- Goal Setting (Achievement Tracking)
- Productivity Analytics
- Time & Date Calculations

💡 **Quick Actions:**
- "Create a new task"
- "Start a pomodoro session"
- "Check my productivity stats"
- "Add a new habit to track"
- "Set a new goal"
- "Show my goal progress"

🚀 **Ready to help you boost your productivity!**
"""
            
        except Exception as e:
            return f"Task Manager Agent Status: Active (Stats error: {str(e)})"

# Example usage and testing
if __name__ == "__main__":
    print("🎯 Testing Task Manager Agent...")
    
    try:
        # Create agent
        agent = TaskManagerAgent()
        
        # Test basic functionality
        print("\n1. Agent Status:")
        print(agent.get_quick_stats())
        
        print("\n2. Creating a sample task:")
        result = agent.process_request("Create a task to finish the project report by tomorrow with high priority")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n3. Getting task list:")
        result = agent.process_request("Show me all my tasks")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n4. Starting a pomodoro:")
        result = agent.process_request("Start a 25-minute pomodoro session for working on the report")
        print(f"Response: {result.get('response', result.get('error'))}")
        
        print("\n5. Goal setting:")
        result = agent.process_request("Help me set a goal to improve my productivity by 20% this month")
        print(f"Response: {result.get('response', result.get('error'))}")
        
    except Exception as e:
        print(f"❌ Error testing Task Manager Agent: {e}")
        print("💡 Make sure to set up your Google API key in the .env file")