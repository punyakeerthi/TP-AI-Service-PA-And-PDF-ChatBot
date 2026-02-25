# 📚 Git Basics for Students

## 🤔 What is Git?
Git is a **version control system** that helps you:
- Track changes in your code
- Save different versions of your project
- Collaborate with others
- Never lose your work again!

Think of it like "Save As" but much smarter! 💡

---

## 🛠️ Initial Setup (One Time Only)

### Install Git
- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **Mac**: `brew install git` or download from website
- **Linux**: `sudo apt install git`

### Configure Your Identity
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📂 Starting a Project

### Option 1: Start a New Project
```bash
mkdir my-project
cd my-project
git init
```

### Option 2: Clone an Existing Project
```bash
git clone https://github.com/username/repository-name.git
cd repository-name
```

---

## 🚀 Essential Daily Commands

### 1. Check Status (Use this A LOT!)
```bash
git status
```
*Shows what files have changed*

### 2. Add Files to Staging
```bash
# Add specific file
git add filename.py

# Add all files
git add .

# Add all Python files
git add *.py
```

### 3. Commit Your Changes
```bash
# Commit with message
git commit -m "Add login feature"

# Better commit message examples:
git commit -m "Fix bug in user authentication"
git commit -m "Add new homepage design"
git commit -m "Update documentation"
```

### 4. See Your History
```bash
# See commit history
git log

# See short history
git log --oneline
```

### 5. See What Changed
```bash
# See changes before staging
git diff

# See changes in staged files
git diff --staged
```

---

## 🌐 GitHub CLI Setup & Authentication

### Install GitHub CLI
- **Windows**: Download from [cli.github.com](https://cli.github.com/)
- **Mac**: `brew install gh`
- **Linux**: Follow instructions at [cli.github.com](https://cli.github.com/)

### Authenticate with GitHub
```bash
# Login to GitHub (opens browser)
gh auth login

# Check if you're logged in
gh auth status

# Logout
gh auth logout
```

### Refresh Your Access Token
```bash
gh auth refresh
```

---

## 📂 GitHub CLI Commands for Students

### Create a New Repository
```bash
# Create repo on GitHub and clone it locally
gh repo create my-project --public --clone

# Create repo on GitHub from existing local folder
gh repo create my-project --public --source=. --push
```

### Repository Information
```bash
# View repository in browser
gh repo view --web

# Get repository info
gh repo view

# List your repositories
gh repo list
```

### Working with Issues
```bash
# List issues
gh issue list

# Create new issue
gh issue create --title "Bug in login" --body "Description here"

# View specific issue
gh issue view 1
```

### Pull Requests
```bash
# Create pull request
gh pr create --title "Add new feature" --body "Description"

# List pull requests
gh pr list

# View pull request in browser
gh pr view --web

# Merge pull request
gh pr merge 1
```

### Clone and Fork Repositories
```bash
# Clone any public repository
gh repo clone username/repository-name

# Fork a repository
gh repo fork username/repository-name --clone
```

### Quick Repository Setup
```bash
# Create and setup new project in one go
gh repo create my-awesome-project --public --clone --gitignore=Python
cd my-awesome-project
echo "# My Awesome Project" > README.md
git add .
git commit -m "Initial commit"
git push
```

---

## 🌐 Working with Remote Repositories (Git Commands)

### Push Your Code to GitHub
```bash
# First time setup
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main

# After first time
git push
```

### Get Latest Changes
```bash
git pull
```

### Check Remote URL
```bash
git remote -v
```

---

## 🌿 Branching Basics

### Create and Switch to New Branch
```bash
# Create new branch
git branch feature-login

# Switch to branch
git checkout feature-login

# Create and switch in one command
git checkout -b feature-login
```

### List Branches
```bash
git branch
```

### Switch Back to Main
```bash
git checkout main
```

### Merge Branch
```bash
git checkout main
git merge feature-login
```

---

## 🆘 Common Problems & Solutions

### "I made a mistake in my last commit!"
```bash
# Change the commit message
git commit --amend -m "New better message"
```

### "I want to undo changes to a file"
```bash
# Undo changes before staging
git checkout -- filename.py

# Undo staged changes
git reset HEAD filename.py
```

### "I want to see what I changed"
```bash
git diff filename.py
```

### "I forgot what I was doing"
```bash
git status
git log --oneline -5
```

---

## 📋 Complete Workflow Example

```bash
# 1. Start working
git status                    # Check current state

# 2. Make your changes
# (edit your files)

# 3. Check what changed
git status                    # See what files changed
git diff                      # See specific changes

# 4. Stage your changes
git add .                     # Add all files
# or
git add specific-file.py      # Add specific file

# 5. Commit your changes
git commit -m "Describe what you did"

# 6. Push to GitHub (if working with remote)
git push
```

---

## 🎯 Quick Commands Reference

### Git Commands
| Command | What it does |
|---------|-------------|
| `git status` | Show current status |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save changes with message |
| `git push` | Send changes to GitHub |
| `git pull` | Get latest changes |
| `git log` | Show history |
| `git diff` | Show what changed |
| `git checkout -b new-branch` | Create new branch |
| `git checkout main` | Switch to main branch |

### GitHub CLI Commands
| Command | What it does |
|---------|-------------|
| `gh auth login` | Login to GitHub |
| `gh auth status` | Check login status |
| `gh auth logout` | Logout from GitHub |
| `gh repo create name --public --clone` | Create new repository |
| `gh repo clone user/repo` | Clone any repository |
| `gh repo view --web` | Open repo in browser |
| `gh issue create` | Create new issue |
| `gh pr create` | Create pull request |

---

## ✅ Good Practices for Students

### 1. **Commit Often**
- Make small, focused commits
- Commit every time you complete a small feature
- Better to have too many commits than too few!

### 2. **Write Good Commit Messages**
- ✅ Good: "Fix login button not working"
- ✅ Good: "Add user profile page"
- ❌ Bad: "stuff"
- ❌ Bad: "changes"
- ❌ Bad: "fix"

### 3. **Always Check Status**
```bash
git status  # Use this command constantly!
```

### 4. **Pull Before Push**
```bash
git pull    # Always pull latest changes first
git push    # Then push your changes
```

---

## 🚨 Emergency Commands

### "Help! I broke everything!"
```bash
# See what you have
git status

# Go back to last working commit
git reset --hard HEAD~1

# Or restore specific file
git checkout HEAD -- filename.py
```

### "I need to find when something broke"
```bash
git log --oneline
git show commit-hash
```

---

## 💡 Pro Tips

1. **Use `git status` constantly** - It's your best friend!
2. **Commit early and often** - Small commits are better
3. **Always test before committing** - Make sure your code works
4. **Use branches for new features** - Keep main branch clean
5. **Read error messages** - Git usually tells you what to do
6. **Practice on dummy projects** - Get comfortable before real work

---

## 📱 Common Student Scenarios

### Starting a School Project (Method 1: Traditional)
```bash
mkdir school-project
cd school-project
git init
echo "# My School Project" > README.md
git add README.md
git commit -m "Initial commit"
```

### Starting a School Project (Method 2: With GitHub CLI)
```bash
# Login first (one time only)
gh auth login

# Create project with GitHub repo in one command
gh repo create school-project --public --clone --gitignore=Python
cd school-project
echo "# My School Project" > README.md
git add .
git commit -m "Initial commit"
git push
```

### Daily Work Cycle
```bash
git pull                      # Get latest changes
# Do your work...
git add .                     # Stage changes
git commit -m "Complete homework part 1"
git push                      # Backup to GitHub
```

### Before Assignment Deadline
```bash
git status                    # Make sure nothing is lost
git add .                     # Stage everything
git commit -m "Final submission"
git push                      # Send to GitHub
```

---

## 🎓 Remember

- Git seems scary at first, but you only need these basic commands for 90% of your work
- **Practice makes perfect** - try these commands on a test project
- **Google is your friend** - Git has excellent documentation
- **Ask for help** - Every developer was a beginner once!

---

*🚀 Now go forth and code with confidence! Your future self will thank you for learning Git! 💪*
