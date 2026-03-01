# BUSI 722 Setup Guide — macOS

## 1. Claude Pro

1. Visit [claude.ai](https://claude.ai) and create an account.
2. Click **Upgrade to Pro** in the sidebar and complete payment.

## 2. Claude Code

Anthropic now provides a **native installer** (recommended) that requires no dependencies and auto-updates in the background.  The older **npm** method still works but is officially deprecated — it requires Node.js 18+ and you must update manually.

### Option A: Native Installer (Recommended)

Open Terminal and run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

That's it.  The binary installs to `~/.local/bin/claude` and auto-updates silently.

### Option B: Homebrew

```bash
brew install --cask claude-code
```

Homebrew does **not** auto-update.  Run `brew upgrade claude-code` periodically.

### Option C: npm (Deprecated)

If you need npm for compatibility reasons:

1. Install Node.js 18+ from [nodejs.org](https://nodejs.org) or via Homebrew: `brew install node`
2. Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

Do **not** use `sudo`.

### Verify

```bash
claude --version
claude doctor
```

## 3. VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com).
2. Open your course folder: **File → Open Folder**.
3. Install extensions: **Python**, **Jupyter**, **Claude Code**, **Data Wrangler**, **Rainbow CSV**.

## 4. Python

Open the Claude Code panel in VS Code (click the orange Claude icon in the toolbar, or **View → Command Palette → "Claude Code: Open in New Tab"**) and give it these prompts:

- *"Install Python 3.13 and add it to the path."*
- *"Upgrade pip."*
- *"Create a virtual environment using Python 3.13 in my current directory."*
- *"Install numpy pandas scipy statsmodels scikit-learn openpyxl matplotlib seaborn ipykernel pandas-datareader streamlit requests python-dotenv."*

Then select the virtual environment as your interpreter: **View → Command Palette → "Python: Select Interpreter" → choose the venv**.

## 5. Rice Data Portal

1. Visit [data-portal.rice-business.org](https://data-portal.rice-business.org) to get an access token.
2. Tell Claude Code: *"Create a .env file with my Rice access token: abc123..."*

This creates a `.env` file containing `RICE_ACCESS_TOKEN=abc123...`.  Add `.env` to your `.gitignore` so your token is never committed.

## Setup Video

[YouTube walkthrough](https://www.youtube.com/watch?v=hpMrTabldEY) — covers installation end to end.
