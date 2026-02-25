"""
Configuration utility for PDF QA Bot
This script helps users set up their environment and API keys
"""

import os
import sys

def setup_environment():
    """Setup the environment file with API key"""
    print("🤖 PDF QA Bot Configuration Setup")
    print("=" * 40)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        choice = input("📄 .env file already exists. Overwrite? (y/n): ").lower().strip()
        if choice != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📝 Let's set up your Google API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the API key")
    print()
    
    api_key = input("🔑 Enter your Google API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Validate API key format (basic check)
    if len(api_key) < 20:
        print("⚠️  Warning: API key seems too short. Please verify it's correct.")
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"# Google API Key for Gemini AI\n")
        f.write(f"GOOGLE_API_KEY={api_key}\n")
    
    print("✅ Configuration saved successfully!")
    print("📄 .env file created with your API key")
    print("\n🚀 You can now run the application with:")
    print("   python app.py (or streamlit run app.py)")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'langchain',
        'google-generativeai',
        'PyPDF2',
        'python-dotenv',
        'faiss-cpu'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 All dependencies are installed!")
        return True

def main():
    """Main configuration function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_dependencies()
    else:
        setup_environment()
        check_dependencies()
    
    print("\n" + "=" * 40)
    print("🤖 PDF QA Bot is ready to use!")
    print("Run: streamlit run app.py")

if __name__ == "__main__":
    main()