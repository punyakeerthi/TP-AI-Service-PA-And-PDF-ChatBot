"""
📊 Data Analysis Tools Module
===========================
Tools for data processing, analysis, visualization, and reporting.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Any, Union
import json
import logging
from datetime import datetime
import tempfile

logger = logging.getLogger(__name__)

# Set matplotlib to use non-interactive backend
plt.switch_backend('Agg')

class FileAnalysisTool:
    """
    📄 File Analysis Tool
    Analyzes various file types (CSV, Excel, JSON, etc.)
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.txt']
        self.current_data = None
        self.file_info = {}
    
    def analyze_file(self, file_path: str) -> str:
        """
        Analyze a data file and provide insights
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Analysis results
        """
        try:
            if not os.path.exists(file_path):
                return f"❌ File not found: {file_path}"
            
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                return f"❌ Unsupported file format: {file_ext}. Supported: {', '.join(self.supported_formats)}"
            
            # Load data based on file type
            if file_ext == '.csv':
                self.current_data = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                self.current_data = pd.read_excel(file_path)
            elif file_ext == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.current_data = pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
            elif file_ext == '.txt':
                with open(file_path, 'r') as f:
                    content = f.read()
                return self._analyze_text_file(content, file_path)
            
            self.file_info = {
                'path': file_path,
                'format': file_ext,
                'size': os.path.getsize(file_path),
                'modified': datetime.fromtimestamp(os.path.getmtime(file_path))
            }
            
            return self._generate_data_analysis()
            
        except Exception as e:
            logger.error(f"File analysis error: {e}")
            return f"❌ Error analyzing file: {str(e)}"
    
    def _generate_data_analysis(self) -> str:
        """Generate comprehensive data analysis"""
        try:
            if self.current_data is None:
                return "❌ No data loaded"
            
            analysis = f"""
📊 **File Analysis Report**

📁 **File Information:**
- Path: {self.file_info['path']}
- Format: {self.file_info['format']}
- Size: {self.file_info['size']} bytes
- Last Modified: {self.file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}

📈 **Data Overview:**
- Shape: {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns
- Memory Usage: {self.current_data.memory_usage(deep=True).sum()} bytes

📋 **Column Information:**
"""
            
            # Column details
            for col in self.current_data.columns:
                dtype = self.current_data[col].dtype
                null_count = self.current_data[col].isnull().sum()
                unique_count = self.current_data[col].nunique()
                
                analysis += f"- **{col}:** {dtype} ({null_count} nulls, {unique_count} unique)\n"
            
            # Data quality insights
            analysis += "\n🔍 **Data Quality:**\n"
            total_cells = self.current_data.shape[0] * self.current_data.shape[1]
            null_cells = self.current_data.isnull().sum().sum()
            completeness = ((total_cells - null_cells) / total_cells) * 100
            
            analysis += f"- Completeness: {completeness:.1f}%\n"
            analysis += f"- Missing Values: {null_cells}\n"
            analysis += f"- Duplicate Rows: {self.current_data.duplicated().sum()}\n"
            
            # Quick statistics for numeric columns
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                analysis += "\n📊 **Numeric Summary:**\n"
                for col in numeric_cols[:5]:  # Show top 5 numeric columns
                    stats = self.current_data[col].describe()
                    analysis += f"- **{col}:** Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}, Range: [{stats['min']:.2f}, {stats['max']:.2f}]\n"
            
            # Sample data
            analysis += "\n📄 **Sample Data (First 3 rows):**\n"
            analysis += self.current_data.head(3).to_string()
            
            return analysis
            
        except Exception as e:
            return f"❌ Error generating analysis: {str(e)}"
    
    def _analyze_text_file(self, content: str, file_path: str) -> str:
        """Analyze text file content"""
        try:
            lines = content.split('\n')
            words = content.split()
            characters = len(content)
            
            analysis = f"""
📄 **Text File Analysis**

📁 **File:** {os.path.basename(file_path)}
📊 **Statistics:**
- Lines: {len(lines)}
- Words: {len(words)}
- Characters: {characters}
- Average words per line: {len(words)/max(len(lines), 1):.1f}

📝 **Content Preview:**
{content[:500]}{'...' if len(content) > 500 else ''}
"""
            return analysis
            
        except Exception as e:
            return f"❌ Error analyzing text file: {str(e)}"
    
    def analyze_csv_data(self, csv_content: str, data_name: str = "Provided Data") -> str:
        """
        Analyze CSV data from text content directly
        
        Args:
            csv_content: CSV data as string
            data_name: Name to display for the data
            
        Returns:
            Analysis results
        """
        try:
            # Parse CSV from string
            from io import StringIO
            csv_buffer = StringIO(csv_content)
            self.current_data = pd.read_csv(csv_buffer)
            
            # Set file info for the analysis
            self.file_info = {
                'path': data_name,
                'format': 'CSV (from text)',
                'size': len(csv_content.encode('utf-8')),
                'modified': datetime.now()
            }
            
            return self._generate_data_analysis()
            
        except Exception as e:
            logger.error(f"CSV analysis error: {e}")
            return f"❌ Error analyzing CSV data: {str(e)}"
    
    def get_column_analysis(self, column_name: str) -> str:
        """Get detailed analysis of a specific column"""
        try:
            if self.current_data is None:
                return "❌ No data loaded. Please analyze a file first."
            
            if column_name not in self.current_data.columns:
                return f"❌ Column '{column_name}' not found. Available columns: {list(self.current_data.columns)}"
            
            col_data = self.current_data[column_name]
            
            analysis = f"""
🔍 **Column Analysis: {column_name}**

📊 **Basic Info:**
- Data Type: {col_data.dtype}
- Non-null Count: {col_data.count()}
- Null Count: {col_data.isnull().sum()}
- Unique Values: {col_data.nunique()}

"""
            
            if pd.api.types.is_numeric_dtype(col_data):
                stats = col_data.describe()
                analysis += f"""
📈 **Statistical Summary:**
- Mean: {stats['mean']:.3f}
- Median: {stats['50%']:.3f}
- Std Deviation: {stats['std']:.3f}
- Min: {stats['min']:.3f}
- Max: {stats['max']:.3f}
- Q1: {stats['25%']:.3f}
- Q3: {stats['75%']:.3f}
"""
            else:
                value_counts = col_data.value_counts().head(10)
                analysis += f"""
📋 **Top 10 Values:**
{value_counts.to_string()}
"""
            
            return analysis
            
        except Exception as e:
            return f"❌ Error analyzing column: {str(e)}"

class DataVisualizationTool:
    """
    📈 Data Visualization Tool
    Creates charts and graphs from data.
    """
    
    def __init__(self):
        self.output_dir = "data/charts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.current_data = None
    
    def set_data(self, data: pd.DataFrame):
        """Set the data for visualization"""
        self.current_data = data
    
    def create_chart(self, chart_request: str) -> str:
        """
        Create a chart based on user request
        
        Args:
            chart_request: Description of the chart to create
            
        Returns:
            Path to generated chart or error message
        """
        try:
            if self.current_data is None:
                return "❌ No data available. Please analyze a file first."
            
            # Parse chart request (simplified)
            chart_type = self._detect_chart_type(chart_request)
            columns = self._detect_columns(chart_request)
            
            if chart_type == "histogram":
                return self._create_histogram(columns)
            elif chart_type == "scatter":
                return self._create_scatter_plot(columns)
            elif chart_type == "bar":
                return self._create_bar_chart(columns)
            elif chart_type == "line":
                return self._create_line_chart(columns)
            elif chart_type == "correlation":
                return self._create_correlation_heatmap()
            else:
                return self._create_default_chart()
                
        except Exception as e:
            logger.error(f"Chart creation error: {e}")
            return f"❌ Error creating chart: {str(e)}"
    
    def _detect_chart_type(self, request: str) -> str:
        """Detect chart type from user request"""
        request_lower = request.lower()
        if any(word in request_lower for word in ["histogram", "distribution", "freq"]):
            return "histogram"
        elif any(word in request_lower for word in ["scatter", "correlation", "relationship"]):
            return "scatter"
        elif any(word in request_lower for word in ["bar", "count", "category"]):
            return "bar"
        elif any(word in request_lower for word in ["line", "trend", "time"]):
            return "line"
        elif any(word in request_lower for word in ["heatmap", "correlation"]):
            return "correlation"
        else:
            return "default"
    
    def _detect_columns(self, request: str) -> List[str]:
        """Detect column names mentioned in request"""
        columns = []
        for col in self.current_data.columns:
            if col.lower() in request.lower():
                columns.append(col)
        return columns[:2]  # Limit to 2 columns for simplicity
    
    def _create_histogram(self, columns: List[str]) -> str:
        """Create histogram"""
        try:
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            if not columns:
                columns = [numeric_cols[0]] if len(numeric_cols) > 0 else []
            
            if not columns:
                return "❌ No numeric columns found for histogram"
            
            plt.figure(figsize=(10, 6))
            plt.hist(self.current_data[columns[0]].dropna(), bins=20, alpha=0.7, edgecolor='black')
            plt.title(f'Histogram of {columns[0]}')
            plt.xlabel(columns[0])
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            filename = f"histogram_{columns[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"📈 Histogram created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating histogram: {str(e)}"
    
    def _create_scatter_plot(self, columns: List[str]) -> str:
        """Create scatter plot"""
        try:
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            if len(columns) < 2:
                columns = list(numeric_cols[:2]) if len(numeric_cols) >= 2 else []
            
            if len(columns) < 2:
                return "❌ Need at least 2 numeric columns for scatter plot"
            
            plt.figure(figsize=(10, 8))
            plt.scatter(self.current_data[columns[0]], self.current_data[columns[1]], alpha=0.6)
            plt.title(f'Scatter Plot: {columns[0]} vs {columns[1]}')
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])
            plt.grid(True, alpha=0.3)
            
            filename = f"scatter_{columns[0]}_{columns[1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"📊 Scatter plot created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating scatter plot: {str(e)}"
    
    def _create_bar_chart(self, columns: List[str]) -> str:
        """Create bar chart"""
        try:
            if not columns:
                # Use first categorical column
                cat_cols = self.current_data.select_dtypes(include=['object']).columns
                columns = [cat_cols[0]] if len(cat_cols) > 0 else [self.current_data.columns[0]]
            
            value_counts = self.current_data[columns[0]].value_counts().head(10)
            
            plt.figure(figsize=(10, 6))
            value_counts.plot(kind='bar')
            plt.title(f'Bar Chart of {columns[0]}')
            plt.xlabel(columns[0])
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            filename = f"bar_{columns[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"📊 Bar chart created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating bar chart: {str(e)}"
    
    def _create_line_chart(self, columns: List[str]) -> str:
        """Create line chart"""
        try:
            if not columns:
                numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
                columns = [numeric_cols[0]] if len(numeric_cols) > 0 else []
            
            if not columns:
                return "❌ No numeric columns found for line chart"
            
            plt.figure(figsize=(10, 6))
            plt.plot(self.current_data.index, self.current_data[columns[0]])
            plt.title(f'Line Chart of {columns[0]}')
            plt.xlabel('Index')
            plt.ylabel(columns[0])
            plt.grid(True, alpha=0.3)
            
            filename = f"line_{columns[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"📈 Line chart created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating line chart: {str(e)}"
    
    def _create_correlation_heatmap(self) -> str:
        """Create correlation heatmap"""
        try:
            numeric_data = self.current_data.select_dtypes(include=[np.number])
            
            if numeric_data.shape[1] < 2:
                return "❌ Need at least 2 numeric columns for correlation heatmap"
            
            plt.figure(figsize=(10, 8))
            correlation_matrix = numeric_data.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
            
            filename = f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"🔥 Correlation heatmap created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating correlation heatmap: {str(e)}"
    
    def _create_default_chart(self) -> str:
        """Create a default overview chart"""
        try:
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return "❌ No numeric columns found for visualization"
            
            # Create a simple overview with histograms of numeric columns
            num_plots = min(len(numeric_cols), 4)
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            axes = axes.flatten()
            
            for i, col in enumerate(numeric_cols[:num_plots]):
                axes[i].hist(self.current_data[col].dropna(), bins=20, alpha=0.7)
                axes[i].set_title(f'Distribution of {col}')
                axes[i].grid(True, alpha=0.3)
            
            # Hide unused subplots
            for i in range(num_plots, 4):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            
            filename = f"overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"📊 Data overview chart created successfully!\n📁 Saved to: {filepath}"
            
        except Exception as e:
            return f"❌ Error creating default chart: {str(e)}"

class StatisticsTool:
    """
    📊 Statistics Tool
    Performs statistical analysis and calculations.
    """
    
    def __init__(self):
        self.current_data = None
    
    def set_data(self, data: pd.DataFrame):
        """Set data for statistical analysis"""
        self.current_data = data
    
    def descriptive_statistics(self, column_name: str = "") -> str:
        """Calculate descriptive statistics"""
        try:
            if self.current_data is None:
                return "❌ No data available. Please analyze a file first."
            
            if column_name and column_name in self.current_data.columns:
                # Statistics for specific column
                col_data = self.current_data[column_name]
                if pd.api.types.is_numeric_dtype(col_data):
                    stats = col_data.describe()
                    return f"""
📊 **Descriptive Statistics for {column_name}:**

📈 **Central Tendencies:**
- Mean: {stats['mean']:.4f}
- Median: {stats['50%']:.4f}
- Mode: {col_data.mode().iloc[0] if not col_data.mode().empty else 'N/A'}

📏 **Variability:**
- Standard Deviation: {stats['std']:.4f}
- Variance: {col_data.var():.4f}
- Range: {stats['max'] - stats['min']:.4f}
- IQR: {stats['75%'] - stats['25%']:.4f}

🎯 **Distribution:**
- Min: {stats['min']:.4f}
- Q1: {stats['25%']:.4f}
- Q2 (Median): {stats['50%']:.4f}
- Q3: {stats['75%']:.4f}
- Max: {stats['max']:.4f}

📋 **Additional Info:**
- Count: {stats['count']:.0f}
- Skewness: {col_data.skew():.4f}
- Kurtosis: {col_data.kurtosis():.4f}
"""
                else:
                    value_counts = col_data.value_counts()
                    return f"""
📊 **Descriptive Statistics for {column_name} (Categorical):**

📋 **Basic Info:**
- Total Count: {len(col_data)}
- Unique Values: {col_data.nunique()}
- Most Frequent: {value_counts.index[0]} ({value_counts.iloc[0]} times)

🔝 **Top 5 Values:**
{value_counts.head().to_string()}
"""
            else:
                # Overall statistics for numeric columns
                numeric_data = self.current_data.select_dtypes(include=[np.number])
                if numeric_data.empty:
                    return "❌ No numeric columns found for statistical analysis"
                
                stats = numeric_data.describe()
                return f"""
📊 **Descriptive Statistics Summary:**

{stats.round(4).to_string()}

📈 **Additional Statistics:**
{numeric_data.agg(['skew', 'kurt']).round(4).to_string()}
"""
                
        except Exception as e:
            return f"❌ Error calculating statistics: {str(e)}"
    
    def correlation_analysis(self) -> str:
        """Perform correlation analysis"""
        try:
            if self.current_data is None:
                return "❌ No data available. Please analyze a file first."
            
            numeric_data = self.current_data.select_dtypes(include=[np.number])
            
            if numeric_data.shape[1] < 2:
                return "❌ Need at least 2 numeric columns for correlation analysis"
            
            correlation_matrix = numeric_data.corr()
            
            # Find strongest correlations
            corr_pairs = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    corr_value = correlation_matrix.iloc[i, j]
                    corr_pairs.append((col1, col2, corr_value))
            
            # Sort by absolute correlation value
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
            
            result = "🔗 **Correlation Analysis:**\n\n"
            result += "🎯 **Strongest Correlations:**\n"
            
            for i, (col1, col2, corr_value) in enumerate(corr_pairs[:5], 1):
                strength = "Very Strong" if abs(corr_value) > 0.8 else "Strong" if abs(corr_value) > 0.6 else "Moderate" if abs(corr_value) > 0.4 else "Weak"
                direction = "Positive" if corr_value > 0 else "Negative"
                result += f"{i}. **{col1} vs {col2}:** {corr_value:.4f} ({strength} {direction})\n"
            
            result += f"\n📊 **Correlation Matrix:**\n"
            result += correlation_matrix.round(4).to_string()
            
            return result
            
        except Exception as e:
            return f"❌ Error in correlation analysis: {str(e)}"

class ReportGeneratorTool:
    """
    📋 Report Generator Tool
    Creates comprehensive data analysis reports.
    """
    
    def __init__(self):
        self.report_dir = "data/reports"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_report(self, data: pd.DataFrame, file_path: str = "") -> str:
        """Generate comprehensive data analysis report"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"data_report_{timestamp}.txt"
            report_path = os.path.join(self.report_dir, report_filename)
            
            # Initialize tools
            file_tool = FileAnalysisTool()
            stats_tool = StatisticsTool()
            
            file_tool.current_data = data
            stats_tool.set_data(data)
            
            # Generate report content
            report_content = f"""
📊 DATA ANALYSIS REPORT
{'='*50}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source File: {file_path if file_path else 'Data provided directly'}

{file_tool._generate_data_analysis()}

{'='*50}
📈 STATISTICAL ANALYSIS
{'='*50}

{stats_tool.descriptive_statistics()}

{stats_tool.correlation_analysis()}

{'='*50}
💡 KEY INSIGHTS
{'='*50}

{self._generate_insights(data)}

{'='*50}
📋 RECOMMENDATIONS
{'='*50}

{self._generate_recommendations(data)}

{'='*50}
Report generated by Personal AI Assistant
"""
            
            # Save report
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            # Also generate a summary for immediate viewing
            summary = f"""
📋 **Data Analysis Report Generated!**

📁 **Report saved to:** {report_path}

🔍 **Quick Summary:**
- Dataset Shape: {data.shape[0]} rows × {data.shape[1]} columns
- Numeric Columns: {len(data.select_dtypes(include=[np.number]).columns)}
- Text Columns: {len(data.select_dtypes(include=['object']).columns)}
- Missing Values: {data.isnull().sum().sum()}
- Completeness: {((data.shape[0] * data.shape[1] - data.isnull().sum().sum()) / (data.shape[0] * data.shape[1]) * 100):.1f}%

📊 **Report includes:**
- Comprehensive data overview
- Statistical analysis
- Correlation analysis
- Key insights and recommendations

🔗 **Next steps:**
- Review the full report at {report_path}
- Create visualizations with 'create chart' command
- Perform specific column analysis
"""
            
            return summary
            
        except Exception as e:
            return f"❌ Error generating report: {str(e)}"
    
    def _generate_insights(self, data: pd.DataFrame) -> str:
        """Generate key insights from data"""
        insights = []
        
        try:
            # Data quality insights
            missing_pct = (data.isnull().sum().sum() / (data.shape[0] * data.shape[1])) * 100
            if missing_pct > 10:
                insights.append(f"⚠️  High missing data rate ({missing_pct:.1f}%) - consider data cleaning")
            elif missing_pct < 1:
                insights.append(f"✅ Excellent data quality - very low missing data rate ({missing_pct:.1f}%)")
            
            # Numeric column insights
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for col in numeric_cols[:3]:  # Top 3 numeric columns
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        cv = col_data.std() / col_data.mean() if col_data.mean() != 0 else 0
                        if cv > 1:
                            insights.append(f"📊 {col} shows high variability (CV: {cv:.2f})")
                        
                        skewness = col_data.skew()
                        if abs(skewness) > 2:
                            direction = "right" if skewness > 0 else "left"
                            insights.append(f"📈 {col} is highly skewed to the {direction} ({skewness:.2f})")
            
            # Categorical insights
            cat_cols = data.select_dtypes(include=['object']).columns
            if len(cat_cols) > 0:
                for col in cat_cols[:2]:  # Top 2 categorical columns
                    unique_ratio = data[col].nunique() / len(data[col].dropna())
                    if unique_ratio > 0.9:
                        insights.append(f"🔤 {col} has very high cardinality ({data[col].nunique()} unique values)")
                    elif unique_ratio < 0.1:
                        insights.append(f"📊 {col} has low diversity - dominated by few values")
            
            # Size insights
            if data.shape[0] > 100000:
                insights.append("💾 Large dataset - consider sampling for faster processing")
            elif data.shape[0] < 100:
                insights.append("📏 Small dataset - statistical conclusions may have limited power")
            
            if not insights:
                insights.append("📊 Data appears well-structured with no major quality issues detected")
            
            return "\n".join(f"• {insight}" for insight in insights)
            
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _generate_recommendations(self, data: pd.DataFrame) -> str:
        """Generate actionable recommendations"""
        recommendations = []
        
        try:
            # Missing data recommendations
            missing_cols = data.columns[data.isnull().any()].tolist()
            if missing_cols:
                recommendations.append("🔧 Handle missing data in columns: " + ", ".join(missing_cols[:5]))
            
            # Outlier detection recommendations
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols[:3]:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = data[(data[col] < Q1 - 1.5*IQR) | (data[col] > Q3 + 1.5*IQR)][col]
                if len(outliers) > 0:
                    recommendations.append(f"🎯 Investigate {len(outliers)} potential outliers in {col}")
            
            # Correlation recommendations
            if len(numeric_cols) >= 2:
                corr_matrix = data[numeric_cols].corr()
                high_corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        if abs(corr_matrix.iloc[i, j]) > 0.8:
                            high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j]))
                
                if high_corr_pairs:
                    recommendations.append("🔗 Consider multicollinearity between highly correlated variables")
            
            # Visualization recommendations
            categorical_cols = data.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                recommendations.append("📊 Create bar charts for categorical variables distribution")
            if len(numeric_cols) >= 2:
                recommendations.append("📈 Generate correlation heatmap and scatter plots for numeric variables")
            
            # Analysis recommendations
            if data.shape[1] > 10:
                recommendations.append("🔍 Consider dimensionality reduction techniques for high-dimensional data")
            
            if not recommendations:
                recommendations.append("✅ Data is in good shape for analysis - proceed with modeling or deeper investigation")
            
            return "\n".join(f"• {rec}" for rec in recommendations)
            
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Data Analysis Tools...")
    
    # Create sample data for testing
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'A': np.random.normal(100, 15, 1000),
        'B': np.random.normal(50, 10, 1000),
        'C': np.random.choice(['Category1', 'Category2', 'Category3'], 1000),
        'D': np.random.exponential(2, 1000)
    })
    
    # Add some missing values
    sample_data.loc[sample_data.sample(50).index, 'A'] = np.nan
    
    # Test File Analysis Tool
    file_tool = FileAnalysisTool()
    file_tool.current_data = sample_data
    print("\n1. Testing File Analysis:")
    print(file_tool._generate_data_analysis())
    
    # Test Data Visualization Tool
    viz_tool = DataVisualizationTool()
    viz_tool.set_data(sample_data)
    print("\n2. Testing Data Visualization:")
    print(viz_tool.create_chart("histogram of A"))
    
    # Test Statistics Tool
    stats_tool = StatisticsTool()
    stats_tool.set_data(sample_data)
    print("\n3. Testing Statistics:")
    print(stats_tool.descriptive_statistics("A"))
    
    # Test Report Generator
    report_tool = ReportGeneratorTool()
    print("\n4. Testing Report Generator:")
    print(report_tool.generate_report(sample_data, "sample_data.csv"))