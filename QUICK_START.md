# Quick Start Guide

## Installation (One Time Setup)

**1. Navigate to the folder:**
```bash
cd aipm-resume-analyzer
```

**2. Install dependencies:**
```bash
# macOS/Linux
./scripts/install.sh

# Windows
pip install -r requirements.txt
```

## Usage

### Step 1: ⚠️ REQUIRED - Create your .env file

**IMPORTANT**: The `.env` file is **hidden** by default (starts with a dot).

**Option A: Copy from example (recommended)**
```bash
cp examples/example.env .env
```

**Option B: Let the tool create it**
```bash
./analyze resume.pdf
# It will create .env and show you where it is
```

**📁 Where is the .env file?**
- **Exact location**: `aipm-resume-analyzer/.env` (same folder as `analyze` script)
- **Full path example**: `/Users/yourname/aipm-resume-analyzer/.env` (macOS/Linux)
- **Full path example**: `C:\Users\yourname\aipm-resume-analyzer\.env` (Windows)

**🔍 Can't see the .env file?**

The file starts with a dot (.), making it hidden by default:

- **macOS Finder**: Press `Cmd + Shift + .` to show hidden files
- **macOS Terminal**: Use `ls -la` instead of `ls`
- **Windows Explorer**: View → Show → Hidden items
- **Windows Command Prompt**: Use `dir /a` instead of `dir`
- **Linux Terminal**: Use `ls -la` instead of `ls`

### Step 2: Add your API key

Open `.env` in any text editor and add ONE of these:

```bash
# For OpenAI (GPT-4) - Most popular
OPENAI_API_KEY=sk-your-key-here

# OR for Anthropic (Claude) - Best quality
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OR for Google (Gemini) - Most affordable
GOOGLE_API_KEY=your-key-here

# Default provider
DEFAULT_PROVIDER=openai
```

### Step 3: Analyze resumes!

```bash
# Analyze with default provider
./analyze path/to/resume.pdf

# Use specific provider
./analyze resume.pdf --provider anthropic
./analyze resume.pdf --provider google

# Custom output location
./analyze resume.pdf --output ./my_reports/
```

## Output

Reports will be created in `./output/`:
- `Candidate_Name_TIMESTAMP.md` - Markdown report
- `Candidate_Name_TIMESTAMP.html` - Beautiful HTML report (open in browser)
- `Candidate_Name_TIMESTAMP.json` - Raw JSON data

## Example Usage

```bash
# Analyze a resume with default provider
./analyze path/to/resume.pdf

# Use specific provider
./analyze resume.pdf --provider anthropic

# Save to custom location
./analyze resume.pdf --output ./my_reports/
```

## Getting API Keys

### OpenAI (Recommended for most users)
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "+ Create new secret key"
4. Name it "AI PM Resume Analyzer"
5. Copy key and paste in .env
6. Add $5-10 credits at https://platform.openai.com/account/billing

**Cost**: ~$0.10-0.30 per resume

### Anthropic (Best quality)
1. Go to https://console.anthropic.com/settings/keys
2. Sign in or create account
3. Click "Create Key"
4. Copy key and paste in .env
5. Add credits if needed

**Cost**: ~$0.15-0.40 per resume

### Google Gemini (Most affordable)
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Select or create project
5. Copy key and paste in .env

**Cost**: ~$0.05-0.15 per resume (often has free tier)

## Troubleshooting

**"Module not found" error:**
```bash
# Recreate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**"API key not found":**
- Check `.env` file exists in root directory: `ls -la .env`
- Verify file location (must be same folder as `analyze` script)
- Check no extra spaces: `OPENAI_API_KEY=sk-...` (correct) vs `OPENAI_API_KEY = sk-...` (wrong)
- Check no quotes: `OPENAI_API_KEY=sk-...` (correct) vs `OPENAI_API_KEY="sk-..."` (wrong)
- Make sure filename is exactly `.env` not `.env.txt` or `env`
- Start fresh: `cp examples/example.env .env` then edit

**"Permission denied":**
```bash
chmod +x analyze
chmod +x bin/analyze
```

## Tips

**Find your .env file:**
```bash
# Show hidden files (macOS/Linux)
ls -la

# Should see: -rw-r--r--  1 user  staff  XXX Oct 25 XX:XX .env
```

**Edit your .env file:**
```bash
# macOS/Linux
nano .env

# Or use any text editor like VS Code, Sublime, etc.
```

**Verify your setup:**
```bash
# Check .env exists
cat .env

# You should see your API key (not empty values)
```

---

**Need help?** See README.md for full documentation.
