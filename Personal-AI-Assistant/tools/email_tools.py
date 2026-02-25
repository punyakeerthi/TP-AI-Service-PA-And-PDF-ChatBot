"""
📧 Email Tools Module
==================
Tools for sending, reading, and managing emails.
"""

import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailSenderTool:
    """
    📤 Email Sender Tool
    Sends emails through SMTP (Gmail, Outlook, etc.)
    """
    
    def __init__(self):
        self.email_address = os.getenv("EMAIL_ADDRESS", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, email_request: str) -> str:
        """
        Send an email
        
        Args:
            email_request: Email details in format "recipient|subject|body"
            
        Returns:
            Success or error message
        """
        try:
            # Parse email request
            parts = email_request.split('|')
            if len(parts) < 3:
                return "Error: Email format should be 'recipient@email.com|Subject|Message body'"
            
            recipient = parts[0].strip()
            subject = parts[1].strip()
            body = parts[2].strip()
            
            # Validate inputs
            if not self._is_valid_email(recipient):
                return f"Error: Invalid email address '{recipient}'"
            
            if not self.email_address or not self.email_password:
                return "Error: Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
            
            return self._send_email_internal(recipient, subject, body)
            
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            return f"Error sending email: {str(e)}"
    
    def _send_email_internal(self, recipient: str, subject: str, body: str, attachment_path: str = "") -> str:
        """Internal method to send email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.email_address, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_address, recipient, text)
            server.quit()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return f"✅ Email sent successfully to {recipient} at {timestamp}\nSubject: {subject}"
            
        except smtplib.SMTPAuthenticationError:
            return "❌ Email authentication failed. Please check your email credentials and enable 'App Passwords' for Gmail."
        except smtplib.SMTPRecipientsRefused:
            return f"❌ Invalid recipient email address: {recipient}"
        except smtplib.SMTPServerDisconnected:
            return "❌ SMTP server connection lost. Please try again."
        except Exception as e:
            return f"❌ Error sending email: {str(e)}"
    
    def send_email_with_attachment(self, email_request: str) -> str:
        """
        Send email with attachment
        
        Args:
            email_request: Format "recipient|subject|body|attachment_path"
            
        Returns:
            Success or error message
        """
        try:
            parts = email_request.split('|')
            if len(parts) < 4:
                return "Error: Format should be 'recipient|subject|body|attachment_path'"
            
            recipient = parts[0].strip()
            subject = parts[1].strip()
            body = parts[2].strip()
            attachment_path = parts[3].strip()
            
            if not os.path.exists(attachment_path):
                return f"Error: Attachment file not found: {attachment_path}"
            
            return self._send_email_internal(recipient, subject, body, attachment_path)
            
        except Exception as e:
            return f"Error sending email with attachment: {str(e)}"
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email address format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

class EmailReaderTool:
    """
    📥 Email Reader Tool
    Reads emails from IMAP servers (Gmail, Outlook, etc.)
    """
    
    def __init__(self):
        self.email_address = os.getenv("EMAIL_ADDRESS", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
    
    def read_recent_emails(self, num_emails: int = 5) -> str:
        """
        Read recent emails from inbox
        
        Args:
            num_emails: Number of recent emails to read
            
        Returns:
            Formatted email list
        """
        try:
            if not self.email_address or not self.email_password:
                return "Error: Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            
            # Select inbox
            mail.select('INBOX')
            
            # Search for all emails
            status, messages = mail.search(None, 'ALL')
            
            if status != 'OK':
                return "Error: Could not retrieve emails"
            
            # Get message IDs
            message_ids = messages[0].split()
            
            if not message_ids:
                return "📭 No emails found in inbox"
            
            # Get the most recent emails
            recent_ids = message_ids[-num_emails:] if len(message_ids) >= num_emails else message_ids
            recent_ids.reverse()  # Most recent first
            
            email_list = []
            for i, msg_id in enumerate(recent_ids, 1):
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                
                if status == 'OK':
                    email_message = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract email details
                    subject = email_message['Subject'] or "No Subject"
                    sender = email_message['From'] or "Unknown Sender"
                    date = email_message['Date'] or "Unknown Date"
                    
                    # Get email body (simplified)
                    body = self._extract_email_body(email_message)
                    
                    email_list.append(f"""
**Email {i}:**
📧 From: {sender}
📅 Date: {date}
📋 Subject: {subject}
📄 Preview: {body[:200]}{'...' if len(body) > 200 else ''}
""")
            
            mail.close()
            mail.logout()
            
            return f"📬 Recent {len(recent_ids)} emails:\n" + "\n".join(email_list)
            
        except imaplib.IMAP4.error as e:
            return f"IMAP error: {str(e)}. Please check your email settings and enable IMAP access."
        except Exception as e:
            logger.error(f"Email reading error: {str(e)}")
            return f"Error reading emails: {str(e)}"
    
    def search_emails(self, search_query: str, num_results: int = 10) -> str:
        """
        Search emails by subject or sender
        
        Args:
            search_query: Search term
            num_results: Maximum number of results
            
        Returns:
            Formatted search results
        """
        try:
            if not self.email_address or not self.email_password:
                return "Error: Email credentials not configured."
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_address, self.email_password)
            mail.select('INBOX')
            
            # Search emails (by subject or from)
            search_criteria = f'(OR (SUBJECT "{search_query}") (FROM "{search_query}"))'
            status, messages = mail.search(None, search_criteria)
            
            if status != 'OK':
                return f"Error searching emails for: {search_query}"
            
            message_ids = messages[0].split()
            
            if not message_ids:
                return f"📭 No emails found matching: {search_query}"
            
            # Get recent results
            result_ids = message_ids[-num_results:] if len(message_ids) >= num_results else message_ids
            result_ids.reverse()
            
            search_results = []
            for i, msg_id in enumerate(result_ids, 1):
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                
                if status == 'OK':
                    email_message = email.message_from_bytes(msg_data[0][1])
                    
                    subject = email_message['Subject'] or "No Subject"
                    sender = email_message['From'] or "Unknown Sender"
                    date = email_message['Date'] or "Unknown Date"
                    
                    search_results.append(f"""
**Result {i}:**
📧 From: {sender}
📅 Date: {date}
📋 Subject: {subject}
""")
            
            mail.close()
            mail.logout()
            
            return f"🔍 Search results for '{search_query}' ({len(result_ids)} found):\n" + "\n".join(search_results)
            
        except Exception as e:
            return f"Error searching emails: {str(e)}"
    
    def _extract_email_body(self, email_message) -> str:
        """Extract plain text body from email message"""
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        if isinstance(body, bytes):
                            body = body.decode('utf-8', errors='ignore')
                        return body
                return "Multipart email - content not readable"
            else:
                body = email_message.get_payload(decode=True)
                if isinstance(body, bytes):
                    body = body.decode('utf-8', errors='ignore')
                return body
        except Exception:
            return "Could not read email content"

class EmailManagerTool:
    """
    📨 Email Manager Tool
    Combined email management functionality
    """
    
    def __init__(self):
        self.sender = EmailSenderTool()
        self.reader = EmailReaderTool()
    
    def manage_email(self, action_request: str) -> str:
        """
        Handle various email management tasks
        
        Args:
            action_request: Action in format "action|parameters"
            
        Returns:
            Result of the email action
        """
        try:
            parts = action_request.split('|', 1)
            if len(parts) < 2:
                return """
❌ Invalid format. Use one of:
- send|recipient@email.com|Subject|Message
- read|5 (number of recent emails)
- search|search_term
"""
            
            action = parts[0].strip().lower()
            parameters = parts[1].strip()
            
            if action == "send":
                return self.sender.send_email(parameters)
            elif action == "read":
                try:
                    num_emails = int(parameters) if parameters.isdigit() else 5
                    return self.reader.read_recent_emails(num_emails)
                except ValueError:
                    return self.reader.read_recent_emails(5)
            elif action == "search":
                return self.reader.search_emails(parameters)
            else:
                return f"❌ Unknown email action: {action}. Use 'send', 'read', or 'search'"
                
        except Exception as e:
            return f"Error managing email: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Email Tools...")
    
    # Test Email Sender
    email_sender = EmailSenderTool()
    print("\n1. Testing Email Sender:")
    
    # Note: This test will only work with actual email credentials
    test_send = "test@example.com|Test Subject|This is a test email body"
    result = email_sender.send_email(test_send)
    print(result)
    
    # Test Email Reader
    email_reader = EmailReaderTool()
    print("\n2. Testing Email Reader:")
    
    # Note: This test will only work with actual email credentials
    read_result = email_reader.read_recent_emails(3)
    print(read_result)
    
    # Test Email Manager
    email_manager = EmailManagerTool()
    print("\n3. Testing Email Manager:")
    
    # Test various commands
    commands = [
        "send|test@example.com|Hello|Test message",
        "read|5",
        "search|important"
    ]
    
    for command in commands:
        print(f"\nCommand: {command}")
        result = email_manager.manage_email(command)
        print(result[:200] + "..." if len(result) > 200 else result)