"""
📋 Task Management Tools Module
=============================
Tools for managing tasks, reminders, calendars, and notes.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TaskManagerTool:
    """
    ✅ Task Manager Tool
    Manages todo lists, task completion, and task organization.
    """
    
    def __init__(self, tasks_file: str = "data/tasks.json"):
        self.tasks_file = tasks_file
        self._ensure_data_dir()
        self.tasks = self._load_tasks()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            return []
    
    def _save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def add_task(self, task_description: str) -> str:
        """
        Add a new task
        
        Args:
            task_description: Description of the task
            
        Returns:
            Confirmation message
        """
        try:
            new_task = {
                'id': len(self.tasks) + 1,
                'description': task_description.strip(),
                'completed': False,
                'created': datetime.now().isoformat(),
                'due_date': None,
                'priority': 'medium',
                'category': 'general'
            }
            
            self.tasks.append(new_task)
            self._save_tasks()
            
            return f"✅ Task added successfully!\n📋 Task ID: {new_task['id']}\n📝 Description: '{task_description}'"
            
        except Exception as e:
            return f"❌ Error adding task: {str(e)}"
    
    def list_tasks(self, filter_type: str = "all") -> str:
        """
        List tasks with optional filtering
        
        Args:
            filter_type: 'all', 'pending', 'completed', 'today', 'overdue'
            
        Returns:
            Formatted task list
        """
        try:
            if not self.tasks:
                return "📭 No tasks found. Add your first task to get started!"
            
            filtered_tasks = self._filter_tasks(filter_type.lower())
            
            if not filtered_tasks:
                return f"📭 No {filter_type} tasks found."
            
            task_list = []
            for task in filtered_tasks:
                status_icon = "✅" if task['completed'] else "⏳"
                priority_icon = self._get_priority_icon(task.get('priority', 'medium'))
                
                due_info = ""
                if task.get('due_date'):
                    due_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                    due_info = f"📅 Due: {due_date.strftime('%Y-%m-%d %H:%M')}"
                
                task_info = f"{status_icon} {priority_icon} **{task['id']}:** {task['description']}"
                if due_info:
                    task_info += f"\n     {due_info}"
                
                task_list.append(task_info)
            
            header = f"📋 **{filter_type.title()} Tasks ({len(filtered_tasks)} found):**\n"
            return header + "\n".join(task_list)
            
        except Exception as e:
            return f"❌ Error listing tasks: {str(e)}"
    
    def complete_task(self, task_id: str) -> str:
        """
        Mark a task as completed
        
        Args:
            task_id: ID of the task to complete
            
        Returns:
            Confirmation message
        """
        try:
            task_id = int(task_id)
            
            for task in self.tasks:
                if task['id'] == task_id:
                    if task['completed']:
                        return f"ℹ️ Task {task_id} is already completed: '{task['description']}'"
                    
                    task['completed'] = True
                    task['completed_date'] = datetime.now().isoformat()
                    self._save_tasks()
                    
                    return f"🎉 Task {task_id} completed successfully!\n✅ '{task['description']}'"
            
            return f"❌ Task {task_id} not found. Use 'list tasks' to see available tasks."
            
        except ValueError:
            return "❌ Invalid task ID. Please provide a number."
        except Exception as e:
            return f"❌ Error completing task: {str(e)}"
    
    def delete_task(self, task_id: str) -> str:
        """
        Delete a task
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            Confirmation message
        """
        try:
            task_id = int(task_id)
            
            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    deleted_task = self.tasks.pop(i)
                    self._save_tasks()
                    return f"🗑️ Task {task_id} deleted successfully: '{deleted_task['description']}'"
            
            return f"❌ Task {task_id} not found."
            
        except ValueError:
            return "❌ Invalid task ID. Please provide a number."
        except Exception as e:
            return f"❌ Error deleting task: {str(e)}"
    
    def set_task_priority(self, task_id: str, priority: str) -> str:
        """
        Set task priority
        
        Args:
            task_id: ID of the task
            priority: 'low', 'medium', 'high', 'urgent'
            
        Returns:
            Confirmation message
        """
        try:
            task_id = int(task_id)
            priority = priority.lower()
            
            if priority not in ['low', 'medium', 'high', 'urgent']:
                return "❌ Invalid priority. Use: low, medium, high, or urgent"
            
            for task in self.tasks:
                if task['id'] == task_id:
                    task['priority'] = priority
                    self._save_tasks()
                    return f"📊 Task {task_id} priority set to '{priority}'"
            
            return f"❌ Task {task_id} not found."
            
        except ValueError:
            return "❌ Invalid task ID. Please provide a number."
        except Exception as e:
            return f"❌ Error setting priority: {str(e)}"
    
    def _filter_tasks(self, filter_type: str) -> List[Dict]:
        """Filter tasks based on type"""
        if filter_type == "pending" or filter_type == "todo":
            return [t for t in self.tasks if not t['completed']]
        elif filter_type == "completed" or filter_type == "done":
            return [t for t in self.tasks if t['completed']]
        elif filter_type == "today":
            today = datetime.now().date()
            return [t for t in self.tasks if not t['completed'] and 
                   t.get('due_date') and 
                   datetime.fromisoformat(t['due_date'].replace('Z', '+00:00')).date() == today]
        elif filter_type == "overdue":
            now = datetime.now()
            return [t for t in self.tasks if not t['completed'] and 
                   t.get('due_date') and 
                   datetime.fromisoformat(t['due_date'].replace('Z', '+00:00')) < now]
        else:
            return self.tasks
    
    def _get_priority_icon(self, priority: str) -> str:
        """Get icon for task priority"""
        icons = {
            'low': '🟢',
            'medium': '🟡', 
            'high': '🟠',
            'urgent': '🔴'
        }
        return icons.get(priority, '🟡')

    def get_task_stats(self) -> str:
        """Get task statistics"""
        try:
            total = len(self.tasks)
            completed = len([t for t in self.tasks if t['completed']])
            pending = total - completed
            
            if total == 0:
                return "📊 No tasks yet. Add some tasks to see statistics!"
            
            completion_rate = (completed / total) * 100
            
            stats = f"""
📊 **Task Statistics:**

📈 Total Tasks: {total}
✅ Completed: {completed}
⏳ Pending: {pending}
📊 Completion Rate: {completion_rate:.1f}%
"""
            
            # Priority breakdown
            priority_counts = {}
            for task in self.tasks:
                if not task['completed']:
                    priority = task.get('priority', 'medium')
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            if priority_counts:
                stats += "\n🎯 **Pending by Priority:**\n"
                for priority, count in priority_counts.items():
                    icon = self._get_priority_icon(priority)
                    stats += f"{icon} {priority.title()}: {count}\n"
            
            return stats
            
        except Exception as e:
            return f"❌ Error getting task stats: {str(e)}"

class ReminderTool:
    """
    ⏰ Reminder Tool
    Manages reminders and notifications.
    """
    
    def __init__(self, reminders_file: str = "data/reminders.json"):
        self.reminders_file = reminders_file
        self._ensure_data_dir()
        self.reminders = self._load_reminders()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
    
    def _load_reminders(self) -> List[Dict]:
        """Load reminders from JSON file"""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading reminders: {e}")
            return []
    
    def _save_reminders(self):
        """Save reminders to JSON file"""
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving reminders: {e}")
    
    def set_reminder(self, reminder_details: str) -> str:
        """
        Set a new reminder
        
        Args:
            reminder_details: Reminder description and optional time
            
        Returns:
            Confirmation message
        """
        try:
            # Parse reminder details (simple format for now)
            new_reminder = {
                'id': len(self.reminders) + 1,
                'description': reminder_details.strip(),
                'created': datetime.now().isoformat(),
                'reminder_time': None,
                'completed': False,
                'type': 'general'
            }
            
            self.reminders.append(new_reminder)
            self._save_reminders()
            
            return f"⏰ Reminder set successfully!\n📝 '{reminder_details}'\n🆔 Reminder ID: {new_reminder['id']}"
            
        except Exception as e:
            return f"❌ Error setting reminder: {str(e)}"
    
    def list_reminders(self) -> str:
        """List all active reminders"""
        try:
            active_reminders = [r for r in self.reminders if not r['completed']]
            
            if not active_reminders:
                return "📭 No active reminders. Set new reminders with 'set reminder [description]'"
            
            reminder_list = []
            for reminder in active_reminders:
                created_date = datetime.fromisoformat(reminder['created']).strftime('%Y-%m-%d %H:%M')
                reminder_info = f"⏰ **{reminder['id']}:** {reminder['description']}\n     📅 Created: {created_date}"
                reminder_list.append(reminder_info)
            
            return f"⏰ **Active Reminders ({len(active_reminders)} found):**\n\n" + "\n\n".join(reminder_list)
            
        except Exception as e:
            return f"❌ Error listing reminders: {str(e)}"
    
    def complete_reminder(self, reminder_id: str) -> str:
        """Mark reminder as completed"""
        try:
            reminder_id = int(reminder_id)
            
            for reminder in self.reminders:
                if reminder['id'] == reminder_id:
                    reminder['completed'] = True
                    reminder['completed_date'] = datetime.now().isoformat()
                    self._save_reminders()
                    return f"✅ Reminder {reminder_id} completed: '{reminder['description']}'"
            
            return f"❌ Reminder {reminder_id} not found."
            
        except ValueError:
            return "❌ Invalid reminder ID. Please provide a number."
        except Exception as e:
            return f"❌ Error completing reminder: {str(e)}"

class CalendarTool:
    """
    📅 Calendar Tool
    Basic calendar and scheduling functionality.
    """
    
    def __init__(self, events_file: str = "data/events.json"):
        self.events_file = events_file
        self._ensure_data_dir()
        self.events = self._load_events()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.events_file), exist_ok=True)
    
    def _load_events(self) -> List[Dict]:
        """Load events from JSON file"""
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading events: {e}")
            return []
    
    def _save_events(self):
        """Save events to JSON file"""
        try:
            with open(self.events_file, 'w') as f:
                json.dump(self.events, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving events: {e}")
    
    def schedule_event(self, event_details: str) -> str:
        """
        Schedule a new event
        
        Args:
            event_details: Event description
            
        Returns:
            Confirmation message
        """
        try:
            new_event = {
                'id': len(self.events) + 1,
                'title': event_details.strip(),
                'description': '',
                'start_time': None,
                'end_time': None,
                'created': datetime.now().isoformat(),
                'location': '',
                'attendees': []
            }
            
            self.events.append(new_event)
            self._save_events()
            
            return f"📅 Event scheduled successfully!\n🎯 '{event_details}'\n🆔 Event ID: {new_event['id']}"
            
        except Exception as e:
            return f"❌ Error scheduling event: {str(e)}"
    
    def list_events(self, days_ahead: int = 7) -> str:
        """List upcoming events"""
        try:
            if not self.events:
                return "📭 No events scheduled. Schedule new events with 'schedule event [description]'"
            
            event_list = []
            for event in self.events:
                created_date = datetime.fromisoformat(event['created']).strftime('%Y-%m-%d %H:%M')
                event_info = f"📅 **{event['id']}:** {event['title']}\n     📅 Created: {created_date}"
                
                if event.get('location'):
                    event_info += f"\n     📍 Location: {event['location']}"
                
                event_list.append(event_info)
            
            return f"📅 **Scheduled Events ({len(self.events)} found):**\n\n" + "\n\n".join(event_list)
            
        except Exception as e:
            return f"❌ Error listing events: {str(e)}"

class NoteTool:
    """
    📝 Note Tool
    Simple note-taking functionality.
    """
    
    def __init__(self, notes_file: str = "data/notes.json"):
        self.notes_file = notes_file
        self._ensure_data_dir()
        self.notes = self._load_notes()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.notes_file), exist_ok=True)
    
    def _load_notes(self) -> List[Dict]:
        """Load notes from JSON file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading notes: {e}")
            return []
    
    def _save_notes(self):
        """Save notes to JSON file"""
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(self.notes, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving notes: {e}")
    
    def add_note(self, note_content: str) -> str:
        """Add a new note"""
        try:
            new_note = {
                'id': len(self.notes) + 1,
                'content': note_content.strip(),
                'created': datetime.now().isoformat(),
                'updated': datetime.now().isoformat(),
                'tags': [],
                'category': 'general'
            }
            
            self.notes.append(new_note)
            self._save_notes()
            
            return f"📝 Note added successfully!\n🆔 Note ID: {new_note['id']}\n📄 Content preview: '{note_content[:100]}{'...' if len(note_content) > 100 else ''}'"
            
        except Exception as e:
            return f"❌ Error adding note: {str(e)}"
    
    def list_notes(self, limit: int = 10) -> str:
        """List recent notes"""
        try:
            if not self.notes:
                return "📭 No notes found. Add new notes with 'add note [content]'"
            
            recent_notes = self.notes[-limit:] if len(self.notes) > limit else self.notes
            recent_notes.reverse()  # Most recent first
            
            note_list = []
            for note in recent_notes:
                created_date = datetime.fromisoformat(note['created']).strftime('%Y-%m-%d %H:%M')
                preview = note['content'][:150] + "..." if len(note['content']) > 150 else note['content']
                note_info = f"📝 **Note {note['id']}:**\n{preview}\n     📅 Created: {created_date}"
                note_list.append(note_info)
            
            return f"📝 **Recent Notes ({len(recent_notes)} shown):**\n\n" + "\n\n".join(note_list)
            
        except Exception as e:
            return f"❌ Error listing notes: {str(e)}"
    
    def search_notes(self, search_term: str) -> str:
        """Search notes by content"""
        try:
            matching_notes = []
            search_term = search_term.lower()
            
            for note in self.notes:
                if search_term in note['content'].lower():
                    matching_notes.append(note)
            
            if not matching_notes:
                return f"🔍 No notes found containing '{search_term}'"
            
            result_list = []
            for note in matching_notes:
                preview = note['content'][:200] + "..." if len(note['content']) > 200 else note['content']
                result_list.append(f"📝 **Note {note['id']}:** {preview}")
            
            return f"🔍 **Search results for '{search_term}' ({len(matching_notes)} found):**\n\n" + "\n\n".join(result_list)
            
        except Exception as e:
            return f"❌ Error searching notes: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Task Management Tools...")
    
    # Test Task Manager
    task_manager = TaskManagerTool()
    print("\n1. Testing Task Manager:")
    print(task_manager.add_task("Buy groceries"))
    print(task_manager.add_task("Call dentist"))
    print(task_manager.list_tasks())
    print(task_manager.complete_task("1"))
    print(task_manager.get_task_stats())
    
    # Test Reminder Tool
    reminder_tool = ReminderTool()
    print("\n2. Testing Reminder Tool:")
    print(reminder_tool.set_reminder("Water the plants"))
    print(reminder_tool.list_reminders())
    
    # Test Calendar Tool
    calendar_tool = CalendarTool()
    print("\n3. Testing Calendar Tool:")
    print(calendar_tool.schedule_event("Team meeting"))
    print(calendar_tool.list_events())
    
    # Test Note Tool
    note_tool = NoteTool()
    print("\n4. Testing Note Tool:")
    print(note_tool.add_note("Remember to check email regularly"))
    print(note_tool.list_notes())
    print(note_tool.search_notes("email"))