# Quick Start Guide

## Installation (One Time Setup)

**1. Navigate to the folder:**
```bash
cd /Users/abediaz/Documents/SecondBrain/10\ -\ Projects/Applied_AI_PM/tools/aipm-resume-analyzer
```

**2. The dependencies are already installed in the virtual environment!**

## Usage

### Step 1: Run the analyzer (it will create .env file)

```bash
./analyze resume.pdf
```

You'll see:
```
⚠️  No .env file found!

Creating .env template...
✅ Created .env file at: /path/to/.env

📝 SETUP INSTRUCTIONS:

1. Get an API key from ONE of these providers:
   • OpenAI (GPT-4): https://platform.openai.com/api-keys
   • Anthropic (Claude): https://console.anthropic.com/settings/keys
   • Google (Gemini): https://aistudio.google.com/app/apikey

2. Open the .env file and paste your API key
3. Save the file and run the analyzer again
```

### Step 2: Add your API key

Open `.env` and add ONE of these:

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

## Example: Analyze Cheryl's Resume

```bash
# Copy Cheryl's resume to test
./analyze "/Users/abediaz/Downloads/Cheryl Stubrud 06.2025.pdf" --provider anthropic
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
- Make sure you saved the .env file
- Check there are no extra spaces in the key
- Make sure key is on correct line (OPENAI_API_KEY=... not just API_KEY=...)

**"Permission denied":**
```bash
chmod +x analyze
chmod +x bin/analyze
```

## Ready to Ship to GitHub

This folder is ready to be uploaded as a GitHub repository!

Just copy this entire folder to your GitHub directory:
```bash
cp -r /Users/abediaz/Documents/SecondBrain/10\ -\ Projects/Applied_AI_PM/tools/aipm-resume-analyzer ~/Documents/GitHub/aipm-resume-analyzer
cd ~/Documents/GitHub/aipm-resume-analyzer
git init
git add .
git commit -m "Initial commit: AI PM Resume Analyzer"
```

Then create repo on GitHub and push!

---

**Need help?** See README.md for full documentation.
