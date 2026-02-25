"""
🛠️ Utility Tools Module
======================
General utility tools for calculations, weather, date/time, file management.
"""

import os
import math
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json
import logging
import shutil
import re

logger = logging.getLogger(__name__)

class CalculatorTool:
    """
    🧮 Calculator Tool
    Performs mathematical calculations and evaluations.
    """
    
    def __init__(self):
        # Store calculation history
        self.calculation_history = []
    
    def calculate(self, expression: str) -> str:
        """
        Perform mathematical calculations
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Calculation result or error message
        """
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Replace common mathematical terms with Python syntax
            expression = self._preprocess_expression(expression)
            
            # Security check - only allow safe mathematical operations
            if self._is_safe_expression(expression):
                result = eval(expression)
                
                # Format the result nicely
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)  # Avoid floating point precision issues
                
                # Store in history
                calculation_record = {
                    'expression': expression,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                }
                self.calculation_history.append(calculation_record)
                
                # Keep only last 50 calculations
                if len(self.calculation_history) > 50:
                    self.calculation_history.pop(0)
                
                return f"🧮 **Calculation Result:**\n\n📝 Expression: `{expression}`\n✅ Result: **{result}**"
                
            else:
                return "❌ Invalid or unsafe mathematical expression. Please use basic mathematical operations only."
                
        except ZeroDivisionError:
            return "❌ Error: Division by zero is not allowed."
        except TypeError as e:
            return f"❌ Error: Invalid operation - {str(e)}"
        except ValueError as e:
            return f"❌ Error: Invalid value - {str(e)}"
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return f"❌ Error in calculation: {str(e)}"
    
    def _preprocess_expression(self, expression: str) -> str:
        """Preprocess expression to handle common mathematical terms"""
        # Replace common mathematical functions and constants
        replacements = {
            'pi': str(math.pi),
            'e': str(math.e),
            'sqrt': 'math.sqrt',
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'log': 'math.log',
            'ln': 'math.log',
            'log10': 'math.log10',
            'abs': 'abs',
            'pow': 'pow',
            'exp': 'math.exp',
            '^': '**',  # Replace ^ with ** for power
            'factorial': 'math.factorial'
        }
        
        for old, new in replacements.items():
            expression = re.sub(r'\b' + re.escape(old) + r'\b', new, expression)
        
        return expression
    
    def _is_safe_expression(self, expression: str) -> bool:
        """Check if the expression is safe to evaluate"""
        # List of allowed characters and functions
        allowed_chars = set('0123456789+-*/().** ')
        allowed_functions = [
            'math.sqrt', 'math.sin', 'math.cos', 'math.tan',
            'math.log', 'math.log10', 'math.exp', 'math.factorial',
            'abs', 'pow', 'min', 'max'
        ]
        
        # Remove allowed functions from expression for character checking
        temp_expr = expression
        for func in allowed_functions:
            temp_expr = temp_expr.replace(func, '')
        
        # Remove numbers (including decimals) for character checking
        temp_expr = re.sub(r'\d+\.?\d*', '', temp_expr)
        temp_expr = temp_expr.replace(str(math.pi), '').replace(str(math.e), '')
        
        # Check if all remaining characters are allowed
        return all(char in allowed_chars for char in temp_expr)
    
    def get_calculation_history(self) -> str:
        """Get recent calculation history"""
        try:
            if not self.calculation_history:
                return "📭 No calculation history available."
            
            history_text = "🕒 **Recent Calculations:**\n\n"
            
            # Show last 10 calculations
            recent_calculations = self.calculation_history[-10:]
            
            for i, calc in enumerate(reversed(recent_calculations), 1):
                timestamp = datetime.fromisoformat(calc['timestamp']).strftime('%H:%M:%S')
                history_text += f"**{i}.** `{calc['expression']}` = **{calc['result']}** _{timestamp}_\n"
            
            return history_text
            
        except Exception as e:
            return f"❌ Error retrieving calculation history: {str(e)}"
    
    def advanced_calculate(self, operation: str, *args) -> str:
        """Perform advanced mathematical operations"""
        try:
            operation = operation.lower().strip()
            
            if operation == "percentage":
                if len(args) >= 2:
                    value, total = float(args[0]), float(args[1])
                    percentage = (value / total) * 100
                    return f"🧮 **Percentage Calculation:**\n\n{value} is {percentage:.2f}% of {total}"
                else:
                    return "❌ Percentage calculation requires two values: value and total"
            
            elif operation == "compound_interest":
                if len(args) >= 4:
                    principal, rate, time, compound = float(args[0]), float(args[1]), float(args[2]), float(args[3])
                    amount = principal * ((1 + rate/100/compound) ** (compound * time))
                    interest = amount - principal
                    return f"""
🧮 **Compound Interest Calculation:**

💰 Principal: ${principal:,.2f}
📊 Rate: {rate}% per year
⏰ Time: {time} years
🔄 Compounded: {compound} times per year

📈 **Results:**
💲 Final Amount: ${amount:,.2f}
💰 Interest Earned: ${interest:,.2f}
"""
                else:
                    return "❌ Compound interest requires: principal, rate, time, compound frequency"
            
            elif operation == "quadratic":
                if len(args) >= 3:
                    a, b, c = float(args[0]), float(args[1]), float(args[2])
                    discriminant = b**2 - 4*a*c
                    
                    if discriminant > 0:
                        x1 = (-b + math.sqrt(discriminant)) / (2*a)
                        x2 = (-b - math.sqrt(discriminant)) / (2*a)
                        return f"""
🧮 **Quadratic Equation Solution:**

📝 Equation: {a}x² + {b}x + {c} = 0

✅ **Two Real Solutions:**
📍 x₁ = {x1:.4f}
📍 x₂ = {x2:.4f}
"""
                    elif discriminant == 0:
                        x = -b / (2*a)
                        return f"""
🧮 **Quadratic Equation Solution:**

📝 Equation: {a}x² + {b}x + {c} = 0

✅ **One Real Solution:**
📍 x = {x:.4f}
"""
                    else:
                        return f"""
🧮 **Quadratic Equation Solution:**

📝 Equation: {a}x² + {b}x + {c} = 0

❌ **No Real Solutions:**
Discriminant = {discriminant:.4f} (negative)
"""
                else:
                    return "❌ Quadratic equation requires coefficients: a, b, c"
            
            else:
                return f"❌ Unknown advanced operation: {operation}\nAvailable: percentage, compound_interest, quadratic"
                
        except Exception as e:
            return f"❌ Error in advanced calculation: {str(e)}"

class WeatherTool:
    """
    🌤️ Weather Tool
    Gets weather information for locations.
    """
    
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY", "")
        self.base_url = "http://api.openweathermap.org/data/2.5/"
    
    def get_weather(self, location: str) -> str:
        """
        Get current weather for a location
        
        Args:
            location: City name or location
            
        Returns:
            Weather information or error message
        """
        try:
            if not self.api_key:
                return self._get_mock_weather(location)
            
            # Get current weather
            url = f"{self.base_url}weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data, location)
            elif response.status_code == 404:
                return f"❌ Location '{location}' not found. Please check the spelling and try again."
            else:
                return f"❌ Error getting weather data: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Weather service timeout. Please try again later."
        except requests.exceptions.RequestException:
            return "❌ Network error. Please check your internet connection."
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return f"❌ Error getting weather: {str(e)}"
    
    def _format_weather_data(self, data: dict, location: str) -> str:
        """Format weather data into readable text"""
        try:
            main = data['main']
            weather = data['weather'][0]
            wind = data.get('wind', {})
            
            temp = main['temp']
            feels_like = main['feels_like']
            humidity = main['humidity']
            pressure = main['pressure']
            
            description = weather['description'].title()
            wind_speed = wind.get('speed', 0) * 3.6  # Convert m/s to km/h
            
            # Get sunrise/sunset
            sys_data = data.get('sys', {})
            if 'sunrise' in sys_data and 'sunset' in sys_data:
                sunrise = datetime.fromtimestamp(sys_data['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(sys_data['sunset']).strftime('%H:%M')
                sun_info = f"\n🌅 Sunrise: {sunrise}\n🌇 Sunset: {sunset}"
            else:
                sun_info = ""
            
            weather_report = f"""
🌤️ **Weather Report for {location.title()}**

🌡️ **Temperature:**
- Current: {temp:.1f}°C
- Feels like: {feels_like:.1f}°C

☁️ **Conditions:**
- Description: {description}
- Humidity: {humidity}%
- Pressure: {pressure} hPa

💨 **Wind:**
- Speed: {wind_speed:.1f} km/h
{sun_info}

📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            
            return weather_report
            
        except KeyError as e:
            return f"❌ Error parsing weather data: missing {e}"
    
    def _get_mock_weather(self, location: str) -> str:
        """Provide mock weather data when no API key is available"""
        return f"""
🌤️ **Weather Report for {location.title()}**

⚠️ *Mock Data - No API key configured*

🌡️ **Temperature:**
- Current: 22.5°C
- Feels like: 24.1°C

☁️ **Conditions:**
- Description: Partly Cloudy
- Humidity: 65%
- Pressure: 1013 hPa

💨 **Wind:**
- Speed: 12.5 km/h

🌅 Sunrise: 06:30
🌇 Sunset: 18:45

📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

💡 *To get real weather data, add your OpenWeatherMap API key to the .env file*
"""
    
    def get_forecast(self, location: str, days: int = 5) -> str:
        """Get weather forecast"""
        try:
            if not self.api_key:
                return f"🌤️ Weather forecast for {location} requires API key configuration."
            
            url = f"{self.base_url}forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 8 forecasts per day, max 40
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_data(data, location, days)
            else:
                return f"❌ Error getting forecast: {response.status_code}"
                
        except Exception as e:
            return f"❌ Error getting forecast: {str(e)}"
    
    def _format_forecast_data(self, data: dict, location: str, days: int) -> str:
        """Format forecast data"""
        try:
            forecasts = data['list']
            
            forecast_text = f"📊 **{days}-Day Weather Forecast for {location.title()}**\n\n"
            
            # Group by day
            daily_forecasts = {}
            for forecast in forecasts:
                date_str = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
                if date_str not in daily_forecasts:
                    daily_forecasts[date_str] = []
                daily_forecasts[date_str].append(forecast)
            
            # Show daily summaries
            for date_str, day_forecasts in list(daily_forecasts.items())[:days]:
                day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%A, %B %d')
                
                # Get day's temperature range
                temps = [f['main']['temp'] for f in day_forecasts]
                min_temp, max_temp = min(temps), max(temps)
                
                # Get most common weather condition
                conditions = [f['weather'][0]['description'] for f in day_forecasts]
                main_condition = max(set(conditions), key=conditions.count).title()
                
                forecast_text += f"""
📅 **{day_name}**
🌡️ Temperature: {min_temp:.1f}°C - {max_temp:.1f}°C
☁️ Conditions: {main_condition}
"""
            
            return forecast_text
            
        except Exception as e:
            return f"❌ Error formatting forecast: {str(e)}"

class DateTimeTool:
    """
    📅 Date and Time Tool
    Handles date/time calculations and formatting.
    """
    
    def __init__(self):
        pass
    
    def get_current_datetime(self, timezone: str = "local") -> str:
        """Get current date and time"""
        try:
            now = datetime.now()
            
            return f"""
📅 **Current Date & Time**

🕐 **Local Time:**
- Date: {now.strftime('%A, %B %d, %Y')}
- Time: {now.strftime('%I:%M:%S %p')}
- 24-hour: {now.strftime('%H:%M:%S')}

📊 **Details:**
- Week of year: {now.strftime('%U')}
- Day of year: {now.strftime('%j')}
- ISO week: {now.strftime('%V')}

🌍 **Formatted:**
- ISO 8601: {now.isoformat()}
- Unix timestamp: {int(now.timestamp())}
"""
        
        except Exception as e:
            return f"❌ Error getting date/time: {str(e)}"
    
    def calculate_date_difference(self, date1: str, date2: str) -> str:
        """Calculate difference between two dates"""
        try:
            # Try to parse the dates
            formats_to_try = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%Y-%m-%d %H:%M'
            ]
            
            dt1 = dt2 = None
            
            for fmt in formats_to_try:
                try:
                    dt1 = datetime.strptime(date1, fmt)
                    break
                except ValueError:
                    continue
            
            for fmt in formats_to_try:
                try:
                    dt2 = datetime.strptime(date2, fmt)
                    break
                except ValueError:
                    continue
            
            if not dt1 or not dt2:
                return "❌ Unable to parse dates. Please use format: YYYY-MM-DD or DD/MM/YYYY"
            
            diff = abs(dt2 - dt1)
            days = diff.days
            seconds = diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            remaining_seconds = seconds % 60
            
            result = f"""
📅 **Date Difference Calculation**

📍 **From:** {dt1.strftime('%A, %B %d, %Y %H:%M')}
📍 **To:** {dt2.strftime('%A, %B %d, %Y %H:%M')}

⏰ **Difference:**
- Days: {days}
- Hours: {hours}
- Minutes: {minutes}
- Seconds: {remaining_seconds}

📊 **Total:**
- Total days: {diff.total_seconds() / 86400:.2f}
- Total hours: {diff.total_seconds() / 3600:.2f}
- Total minutes: {diff.total_seconds() / 60:.2f}
- Total seconds: {diff.total_seconds():.0f}
"""
            
            if days > 365:
                years = days / 365.25
                result += f"\n🗓️ **Approximately:** {years:.1f} years"
            elif days > 30:
                months = days / 30.44
                result += f"\n🗓️ **Approximately:** {months:.1f} months"
            
            return result
            
        except Exception as e:
            return f"❌ Error calculating date difference: {str(e)}"
    
    def add_time_to_date(self, date_str: str, time_to_add: str) -> str:
        """Add time period to a date"""
        try:
            # Parse the base date
            base_date = None
            formats_to_try = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y']
            
            for fmt in formats_to_try:
                try:
                    base_date = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if not base_date:
                return "❌ Unable to parse date. Please use format: YYYY-MM-DD"
            
            # Parse time to add
            time_parts = time_to_add.lower().strip().split()
            
            if len(time_parts) < 2:
                return "❌ Please specify time to add (e.g., '5 days', '2 weeks', '1 month')"
            
            amount = int(time_parts[0])
            unit = time_parts[1]
            
            if unit.startswith('day'):
                new_date = base_date + timedelta(days=amount)
            elif unit.startswith('week'):
                new_date = base_date + timedelta(weeks=amount)
            elif unit.startswith('month'):
                # Approximate month calculation
                new_date = base_date + timedelta(days=amount * 30)
            elif unit.startswith('year'):
                new_date = base_date + timedelta(days=amount * 365)
            elif unit.startswith('hour'):
                new_date = base_date + timedelta(hours=amount)
            elif unit.startswith('minute'):
                new_date = base_date + timedelta(minutes=amount)
            else:
                return f"❌ Unknown time unit: {unit}. Use: days, weeks, months, years, hours, or minutes"
            
            return f"""
📅 **Date Addition Calculation**

📍 **Starting Date:** {base_date.strftime('%A, %B %d, %Y %H:%M')}
➕ **Adding:** {amount} {unit}
📍 **Result Date:** {new_date.strftime('%A, %B %d, %Y %H:%M')}

📊 **Formatted Results:**
- Standard: {new_date.strftime('%Y-%m-%d')}
- Full: {new_date.strftime('%A, %B %d, %Y')}
- ISO: {new_date.isoformat()}
"""
            
        except ValueError:
            return "❌ Invalid number format. Please use a number followed by time unit."
        except Exception as e:
            return f"❌ Error adding time to date: {str(e)}"

class FileManagerTool:
    """
    📁 File Manager Tool
    Basic file operations and management.
    """
    
    def __init__(self):
        self.allowed_operations = ['list', 'info', 'create_folder', 'copy', 'move', 'delete']
    
    def manage_files(self, operation: str, path: str = "", *args) -> str:
        """
        Perform file management operations
        
        Args:
            operation: Operation to perform
            path: File or directory path
            *args: Additional arguments
            
        Returns:
            Operation result
        """
        try:
            operation = operation.lower().strip()
            
            if operation not in self.allowed_operations:
                return f"❌ Unknown operation: {operation}\nAllowed: {', '.join(self.allowed_operations)}"
            
            if operation == "list":
                return self._list_directory(path or ".")
            elif operation == "info":
                return self._get_file_info(path)
            elif operation == "create_folder":
                return self._create_folder(path)
            elif operation == "copy":
                if len(args) > 0:
                    return self._copy_file(path, args[0])
                return "❌ Copy operation requires source and destination paths"
            elif operation == "move":
                if len(args) > 0:
                    return self._move_file(path, args[0])
                return "❌ Move operation requires source and destination paths"
            elif operation == "delete":
                return self._delete_file(path)
            
        except Exception as e:
            logger.error(f"File management error: {e}")
            return f"❌ Error in file operation: {str(e)}"
    
    def _list_directory(self, directory: str) -> str:
        """List directory contents"""
        try:
            if not os.path.exists(directory):
                return f"❌ Directory not found: {directory}"
            
            if not os.path.isdir(directory):
                return f"❌ Path is not a directory: {directory}"
            
            items = os.listdir(directory)
            
            if not items:
                return f"📁 Directory '{directory}' is empty"
            
            # Separate folders and files
            folders = []
            files = []
            
            for item in items:
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    size = os.path.getsize(item_path)
                    modified = datetime.fromtimestamp(os.path.getmtime(item_path))
                    files.append((item, size, modified))
            
            result = f"📁 **Directory listing for '{directory}':**\n\n"
            
            if folders:
                result += "📂 **Folders:**\n"
                for folder in sorted(folders):
                    result += f"  📁 {folder}/\n"
                result += "\n"
            
            if files:
                result += "📄 **Files:**\n"
                for name, size, modified in sorted(files):
                    size_str = self._format_file_size(size)
                    date_str = modified.strftime('%Y-%m-%d %H:%M')
                    result += f"  📄 {name} ({size_str}) - {date_str}\n"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied accessing directory: {directory}"
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"
    
    def _get_file_info(self, file_path: str) -> str:
        """Get detailed file information"""
        try:
            if not os.path.exists(file_path):
                return f"❌ File or directory not found: {file_path}"
            
            stat = os.stat(file_path)
            
            size = stat.st_size
            created = datetime.fromtimestamp(stat.st_ctime)
            modified = datetime.fromtimestamp(stat.st_mtime)
            accessed = datetime.fromtimestamp(stat.st_atime)
            
            is_dir = os.path.isdir(file_path)
            is_file = os.path.isfile(file_path)
            
            info = f"""
📄 **File Information: {os.path.basename(file_path)}**

📍 **Path:** {os.path.abspath(file_path)}
📂 **Type:** {'Directory' if is_dir else 'File'}
📏 **Size:** {self._format_file_size(size)}

📅 **Timestamps:**
- Created: {created.strftime('%Y-%m-%d %H:%M:%S')}
- Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}
- Accessed: {accessed.strftime('%Y-%m-%d %H:%M:%S')}

🔐 **Permissions:**
- Readable: {'Yes' if os.access(file_path, os.R_OK) else 'No'}
- Writable: {'Yes' if os.access(file_path, os.W_OK) else 'No'}
- Executable: {'Yes' if os.access(file_path, os.X_OK) else 'No'}
"""
            
            if is_file:
                ext = os.path.splitext(file_path)[1].lower()
                if ext:
                    info += f"\n📎 **Extension:** {ext}"
            
            if is_dir:
                try:
                    contents = os.listdir(file_path)
                    folders = sum(1 for item in contents if os.path.isdir(os.path.join(file_path, item)))
                    files = len(contents) - folders
                    info += f"\n📊 **Contents:** {files} files, {folders} folders"
                except PermissionError:
                    info += "\n📊 **Contents:** Permission denied"
            
            return info
            
        except Exception as e:
            return f"❌ Error getting file info: {str(e)}"
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
    
    def _create_folder(self, folder_path: str) -> str:
        """Create a new folder"""
        try:
            if os.path.exists(folder_path):
                return f"❌ Folder already exists: {folder_path}"
            
            os.makedirs(folder_path, exist_ok=True)
            return f"✅ Folder created successfully: {folder_path}"
            
        except Exception as e:
            return f"❌ Error creating folder: {str(e)}"
    
    def _copy_file(self, source: str, destination: str) -> str:
        """Copy a file or directory"""
        try:
            if not os.path.exists(source):
                return f"❌ Source not found: {source}"
            
            if os.path.isdir(source):
                shutil.copytree(source, destination)
                return f"✅ Directory copied successfully: {source} → {destination}"
            else:
                shutil.copy2(source, destination)
                return f"✅ File copied successfully: {source} → {destination}"
                
        except FileExistsError:
            return f"❌ Destination already exists: {destination}"
        except Exception as e:
            return f"❌ Error copying: {str(e)}"
    
    def _move_file(self, source: str, destination: str) -> str:
        """Move/rename a file or directory"""
        try:
            if not os.path.exists(source):
                return f"❌ Source not found: {source}"
            
            shutil.move(source, destination)
            return f"✅ Moved successfully: {source} → {destination}"
            
        except Exception as e:
            return f"❌ Error moving file: {str(e)}"
    
    def _delete_file(self, file_path: str) -> str:
        """Delete a file or directory"""
        try:
            if not os.path.exists(file_path):
                return f"❌ File or directory not found: {file_path}"
            
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                return f"✅ Directory deleted successfully: {file_path}"
            else:
                os.remove(file_path)
                return f"✅ File deleted successfully: {file_path}"
                
        except Exception as e:
            return f"❌ Error deleting: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Utility Tools...")
    
    # Test Calculator Tool
    calc = CalculatorTool()
    print("\n1. Testing Calculator:")
    print(calc.calculate("2 + 3 * 4"))
    print(calc.calculate("sqrt(16) + pi"))
    print(calc.advanced_calculate("percentage", "25", "100"))
    
    # Test Weather Tool
    weather = WeatherTool()
    print("\n2. Testing Weather:")
    print(weather.get_weather("London"))
    
    # Test DateTime Tool
    dt_tool = DateTimeTool()
    print("\n3. Testing DateTime:")
    print(dt_tool.get_current_datetime())
    print(dt_tool.calculate_date_difference("2024-01-01", "2024-12-31"))
    
    # Test File Manager Tool
    file_manager = FileManagerTool()
    print("\n4. Testing File Manager:")
    print(file_manager.manage_files("list", "."))
    print(file_manager.manage_files("info", __file__))