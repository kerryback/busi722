# BUSI 722 Setup Guide — Windows

## 1. Claude Pro

1. Visit [claude.ai](https://claude.ai) and create an account.
2. Click **Upgrade to Pro** in the sidebar and complete payment.

## 2. Git for Windows (Required)

Claude Code on Windows requires Git for Windows regardless of which installation method you use.

Download and install from [git-scm.com/downloads/win](https://git-scm.com/downloads/win).  Accept the defaults (this includes Git Bash).

## 3. Claude Code

Anthropic now provides a **native installer** (recommended) that requires no dependencies and auto-updates in the background.  The older **npm** method still works but is officially deprecated — it requires Node.js 18+ and you must update manually.

### Option A: Native Installer (Recommended)

Open **PowerShell** and run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

That's it.  The binary auto-updates silently.

### Option B: WinGet

```powershell
winget install Anthropic.ClaudeCode
```

WinGet does **not** auto-update.  Run `winget upgrade Anthropic.ClaudeCode` periodically.

### Option C: npm (Deprecated)

If you need npm for compatibility reasons:

1. Install Node.js 18+ (LTS) from [nodejs.org](https://nodejs.org).
2. Open PowerShell and run:

```powershell
npm install -g @anthropic-ai/claude-code
```

### Verify

Open PowerShell and run:

```powershell
claude --version
claude doctor
```

## 4. VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com).
2. Open your course folder: **File → Open Folder**.
3. Install extensions: **Python**, **Jupyter**, **Claude Code**, **Data Wrangler**, **Rainbow CSV**.

## 5. Python

Open the Claude Code panel in VS Code (click the orange Claude icon in the toolbar, or **View → Command Palette → "Claude Code: Open in New Tab"**) and give it these prompts:

- *"Install Python 3.13 and add it to the path."*
- *"Upgrade pip."*
- *"Create a virtual environment using Python 3.13 in my current directory."*
- *"Install numpy pandas scipy statsmodels scikit-learn openpyxl matplotlib seaborn ipykernel pandas-datareader streamlit requests python-dotenv."*

Then select the virtual environment as your interpreter: **View → Command Palette → "Python: Select Interpreter" → choose the venv**.

## 6. Rice Data Portal

1. Visit [data-portal.rice-business.org](https://data-portal.rice-business.org) to get an access token.
2. Tell Claude Code: *"Create a .env file with my Rice access token: abc123..."*

This creates a `.env` file containing `RICE_ACCESS_TOKEN=abc123...`.  Add `.env` to your `.gitignore` so your token is never committed.

## Setup Video

[YouTube walkthrough](https://www.youtube.com/watch?v=hpMrTabldEY) — covers installation end to end.
