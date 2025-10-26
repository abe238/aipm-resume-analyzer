# AI PM Resume Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-green.svg)](#installation)

**Analyze AI PM resumes against the 6-pillar framework** - Get instant, consistent evaluations using OpenAI GPT-4, Anthropic Claude, or Google Gemini.

Perfect for hiring managers screening AI PM candidates, recruiters standardizing evaluations, or candidates self-assessing their readiness.

## ✨ Features

- 🎯 **6-Pillar Framework** - Evaluates Technical Skills, Product Thinking, AI/ML Knowledge, Communication, Strategic Thinking, and Execution
- 🤖 **3 AI Providers** - Choose OpenAI (GPT-4), Anthropic (Claude Sonnet), or Google (Gemini)
- 📊 **Detailed Scoring** - 0-10 scores per pillar with evidence and level assessment
- 📝 **Beautiful Reports** - Generates markdown and HTML outputs with clean design
- ⚡ **Fast Analysis** - Get results in 30 seconds vs 10+ minutes manual review
- 🔒 **Privacy-First** - Runs locally, your data stays on your machine
- 💰 **Cost-Effective** - ~$0.10-0.50 per resume analysis
- 🎨 **Professional Design** - HTML reports styled with Stripe/Tailwind-inspired CSS

## 📦 Quick Start

### Prerequisites

- **Python 3.7+** installed on your computer
- **API key** from ONE of these providers (see Step 1 below):
  - [OpenAI](https://platform.openai.com/api-keys) (GPT-4)
  - [Anthropic](https://console.anthropic.com/settings/keys) (Claude)
  - [Google](https://aistudio.google.com/app/apikey) (Gemini)

### Installation & Setup

**1. Download or clone this repository:**
```bash
git clone https://github.com/abediaz/aipm-resume-analyzer.git
cd aipm-resume-analyzer
```

**2. Install dependencies:**

**macOS/Linux:**
```bash
./scripts/install.sh
```

**Windows:**
```cmd
pip install -r requirements.txt
```

**3. ⚠️ REQUIRED: Create your .env file with API key**

**IMPORTANT**: The `.env` file is **hidden** by default. Follow these steps carefully:

**Option A: Copy from example (recommended)**
```bash
# Copy the example file to create your .env
cp examples/example.env .env

# Then edit .env and add your API key
nano .env  # or use any text editor
```

**Option B: Let the tool create it**
```bash
# Run the analyzer once - it will create .env automatically
./analyze resume.pdf

# You'll see instructions showing where the .env file was created
# Then edit .env and add your API key
```

**📁 Where is the .env file?**
- **Exact location**: `aipm-resume-analyzer/.env` (in the same folder as the `analyze` script)
- **Full path example**: `/Users/yourname/aipm-resume-analyzer/.env`

**🔍 Can't see the .env file?**

The `.env` file starts with a dot (.), making it hidden by default:

- **macOS Finder**: Press `Cmd + Shift + .` to show hidden files
- **macOS Terminal**: Use `ls -la` instead of `ls`
- **Windows Explorer**: Go to View → Show → Hidden items
- **Windows Command Prompt**: Use `dir /a` instead of `dir`
- **Linux Terminal**: Use `ls -la` instead of `ls`

**✏️ Editing the .env file:**

Open `.env` in any text editor and add your API key:

```bash
# For OpenAI (example)
OPENAI_API_KEY=sk-proj-your-actual-key-here

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# OR for Google
GOOGLE_API_KEY=your-actual-key-here

# Default provider
DEFAULT_PROVIDER=openai
```

**See `examples/example.env` for a complete template with all options.**

**4. You're ready!** Run your first analysis:

---

## 🔑 API Setup (First Time Only)

### Step 1: Get an API Key

Choose **ONE** provider and get your API key:

#### Option A: OpenAI (GPT-4) - Most Popular
1. Go to https://platform.openai.com/api-keys
2. Click "+ Create new secret key"
3. Name it "AI PM Resume Analyzer"
4. Copy the key (starts with `sk-...`)
5. **Cost**: ~$0.10-0.30 per resume

#### Option B: Anthropic (Claude Sonnet) - Best Quality
1. Go to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Name it "Resume Analyzer"
4. Copy the key (starts with `sk-ant-...`)
5. **Cost**: ~$0.15-0.40 per resume

#### Option C: Google (Gemini) - Most Affordable
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Select or create a project
4. Copy the key
5. **Cost**: ~$0.05-0.15 per resume (often free tier available)

### Step 2: Run the Analyzer (It Will Create .env File)

```bash
./bin/analyze resume.pdf
```

The tool will create a `.env` file and show you where to add your API key.

### Step 3: Add Your API Key

Open the `.env` file (created automatically) and add your key:

```bash
# For OpenAI
OPENAI_API_KEY=sk-your-key-here

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OR for Google
GOOGLE_API_KEY=your-key-here

# Default provider (optional)
DEFAULT_PROVIDER=openai
```

Save the file. **Done!** You're ready to analyze resumes.

---

## 🚀 Usage

### Basic Analysis

```bash
# Analyze resume (uses default provider from .env)
./bin/analyze resume.pdf
```

Output files will be created in `./output/`:
- `Candidate_Name_20241025_143022.md` (Markdown report)
- `Candidate_Name_20241025_143022.html` (HTML report)
- `Candidate_Name_20241025_143022.json` (Raw JSON data)

### Choose Specific Provider

```bash
# Use Claude
./bin/analyze resume.pdf --provider anthropic

# Use Gemini
./bin/analyze resume.pdf --provider google

# Use GPT-4 (default)
./bin/analyze resume.pdf --provider openai
```

### Custom Output Location

```bash
# Save to custom directory
./bin/analyze resume.pdf --output ./reports/

# Different formats
./bin/analyze resume.pdf --format markdown  # MD only
./bin/analyze resume.pdf --format html      # HTML only
./bin/analyze resume.pdf --format both      # Both (default)
```

---

## 📊 Understanding the Output

### Scoring System

Each resume gets scored across **6 pillars**:

| Pillar | Weight | What It Measures |
|--------|--------|------------------|
| **Technical Skills** | 20% | Engineering background, coding, technical decision-making |
| **Product Thinking** | 25% | User empathy, prioritization, product strategy, metrics |
| **AI/ML Knowledge** | 20% | ML fundamentals, AI projects, responsible AI awareness |
| **Communication** | 10% | Writing quality, stakeholder management, presentations |
| **Strategic Thinking** | 15% | Vision setting, market analysis, long-term planning |
| **Execution** | 10% | Shipping track record, project management, results |

### Score Ranges

| Total Score | Decision | Action |
|-------------|----------|--------|
| **8.0 - 10.0** | **Strong Screen** | Top candidate - prioritize interview |
| **6.5 - 7.9** | **Screen** | Solid candidate - invite to interview |
| **5.0 - 6.4** | **Maybe** | Borderline - use additional criteria |
| **Below 5.0** | **No Screen** | Does not meet bar |

### Sample Output

**Markdown Report** (`.md` file):
```markdown
# AI PM Resume Analysis: John Smith

**Total Score**: 42/60 (70/100 weighted)
**Decision**: **Screen**

## Top 3 Strengths
1. Strong product management background with 5 years experience
2. Excellent communication skills - resume is clear and well-organized
3. Proven execution track record with quantified outcomes

## Top 3 Concerns
1. Limited technical background - no engineering experience
2. No AI/ML projects or education
3. Strategic thinking appears tactical (short-term focused)

[... detailed pillar-by-pillar analysis ...]
```

**HTML Report** (`.html` file):
- Beautiful, print-friendly design
- Color-coded scores and decision badges
- Progress bars for each pillar
- Professional styling inspired by Stripe Docs + Tailwind CSS

---

## 🛠️ Troubleshooting

### "Module not found" Errors

```bash
# Reinstall dependencies
pip3 install -r requirements.txt
```

### "API key not found"

**Problem**: The tool can't find your API key.

**Solutions**:

1. **Check `.env` file exists**:
   ```bash
   # Show all files including hidden ones
   ls -la .env

   # Should show: -rw-r--r--  1 yourname  staff  XXX Oct 25 XX:XX .env
   ```

2. **Verify `.env` file location**:
   - Must be in the **root directory** of the project
   - Same folder as the `analyze` script
   - NOT in `examples/`, `bin/`, or any subfolder

3. **Check file contents**:
   ```bash
   # View the .env file
   cat .env

   # Make sure you see your actual API key, not just empty values
   ```

4. **Common mistakes**:
   - ❌ Extra spaces: `OPENAI_API_KEY = sk-...` (wrong)
   - ✅ No spaces: `OPENAI_API_KEY=sk-...` (correct)
   - ❌ Quotes around key: `OPENAI_API_KEY="sk-..."` (wrong)
   - ✅ No quotes: `OPENAI_API_KEY=sk-...` (correct)
   - ❌ Wrong filename: `.env.txt` or `env` (wrong)
   - ✅ Exact name: `.env` (correct)

5. **Start fresh**:
   ```bash
   # Delete old .env and copy from example
   rm .env
   cp examples/example.env .env
   nano .env  # Add your key
   ```

### "Resume file not found"

```bash
# Use full path to resume
./bin/analyze /full/path/to/resume.pdf

# Or move resume to current directory
cp ~/Downloads/resume.pdf ./
./bin/analyze resume.pdf
```

### "Invalid PDF" Error

- Ensure file is actually a PDF (not a screenshot renamed to .pdf)
- Try re-exporting as PDF from original document
- Some encrypted PDFs may not work - remove password protection first

### Python Version Issues

```bash
# Check Python version (need 3.7+)
python3 --version

# If too old, install newer Python:
# macOS: brew install python3
# Linux: sudo apt install python3.9
```

### API Errors

**"Insufficient credits"**: Add credits to your AI provider account
- OpenAI: https://platform.openai.com/account/billing
- Anthropic: https://console.anthropic.com/settings/billing
- Google: Usually has generous free tier

**"Rate limit exceeded"**: Wait 60 seconds and try again (or upgrade API plan)

---

## 💡 Pro Tips

### Cost Optimization

- **Google Gemini**: Usually free tier, cheapest option (~$0.05-0.15/resume)
- **OpenAI**: Mid-range cost (~$0.10-0.30/resume), reliable
- **Anthropic**: Highest cost (~$0.15-0.40/resume), best quality

**Recommendation**: Start with Google Gemini for high-volume screening, use Claude for final rounds.

### Batch Processing

```bash
# Analyze multiple resumes
for resume in resumes/*.pdf; do
  ./bin/analyze "$resume" --output ./batch_reports/
done
```

### Integration with ATS

```bash
# Generate JSON output for ATS integration
./bin/analyze resume.pdf --format markdown
# Then parse the .json file programmatically
```

### Compare Candidates

Open multiple HTML reports in browser tabs for side-by-side comparison.

---

## 📖 Examples

See the `examples/` folder for:
- **`example.env`** - Complete template for configuring your API keys (copy this to create your `.env` file)

---

## 🏗️ Project Structure

```
aipm-resume-analyzer/
├── bin/
│   └── analyze                    # Main analyzer script
├── scripts/
│   └── install.sh                 # Installation script
├── templates/
│   └── output_generator.py        # Report generation
├── examples/
│   └── example.env                # ⭐ Template for your .env file (copy this!)
├── output/                        # Generated reports (created on first run)
├── requirements.txt               # Python dependencies
├── analyze                        # Convenience wrapper script
├── .env                          # ⚠️ YOUR API KEYS (create from example.env)
├── .gitignore
├── LICENSE
└── README.md
```

**Key files:**
- **`examples/example.env`** - Template showing all API configuration options
- **`.env`** - Your actual API keys (you must create this from the example)

---

## 🔒 Privacy & Security

**Your data stays private:**
- ✅ Runs locally on your computer
- ✅ Resumes sent only to YOUR chosen AI provider
- ✅ No data stored on our servers (we don't have any!)
- ✅ API keys stored in local `.env` file

**Best practices:**
- Never commit `.env` file to git (it's in `.gitignore`)
- Don't share your API keys
- Rotate keys if accidentally exposed
- Keep this tool updated for security patches

---

## ❓ FAQ

**Q: Can I use this for non-AI PM roles?**
A: The framework is AI PM-specific, but you can fork and customize the prompts for other roles.

**Q: How accurate is the AI scoring?**
A: Treat it as a screening tool, not a final decision. Always validate with human review.

**Q: Can I customize the evaluation criteria?**
A: Yes! Edit `bin/analyze` to modify the scoring prompts and framework.

**Q: Which AI provider is most accurate?**
A: Claude Sonnet typically gives the most nuanced analysis. GPT-4 is solid. Gemini is fastest/cheapest.

**Q: Does this work with non-PDF resumes?**
A: Currently PDF only. Convert Word docs to PDF first.

**Q: Can I analyze my own resume?**
A: Absolutely! Great for self-assessment before applying to AI PM roles.

---

## 🤝 Contributing

Contributions welcome! This tool helps standardize AI PM hiring.

### To Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test with sample resumes
5. Submit a pull request

### Ideas for Contributions

- [ ] Support for Word documents (.docx)
- [ ] Additional output formats (PDF export)
- [ ] Batch processing UI
- [ ] Integration with popular ATS systems
- [ ] Customizable scoring frameworks

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

**Built with:**
- [OpenAI GPT-4](https://openai.com/) - Powerful language model
- [Anthropic Claude](https://anthropic.com/) - Best-in-class AI assistant
- [Google Gemini](https://ai.google.dev/) - Fast and affordable AI
- [PyPDF2](https://github.com/py-pdf/pypdf2) - PDF text extraction
- Applied AI PM Framework - Open-source evaluation system

**Design inspired by:**
- [Stripe Docs](https://stripe.com/docs) - Clean documentation design
- [Tailwind CSS](https://tailwindcss.com/) - Modern utility-first CSS
- [Material-UI](https://mui.com/) - Component design patterns

---

## 📚 Related Resources

- **Framework Website**: https://aipmframework.com (coming soon)
- **Full Evaluation Rubrics**: [GitHub Repo](https://github.com/abediaz/aipm-framework)
- **Resume Review Template**: [Manual template](https://github.com/abediaz/aipm-framework/tree/main/templates)
- **Interview Scorecards**: [Full interview process](https://github.com/abediaz/aipm-framework)

---

## 🚨 Important Note

**This tool is a screening aid, not a replacement for human judgment.**

- ✅ Use it to: Standardize initial screening, identify promising candidates, save time
- ❌ Don't use it to: Make final hiring decisions, replace interviews, avoid talking to candidates

The best hiring process combines AI-assisted screening with thoughtful human evaluation.

---

**Made for hiring managers, recruiters, and candidates who want standardized, data-driven AI PM evaluations.**

⭐ Star this repo if you find it useful!

---

## Need Help?

- **Issues**: https://github.com/abediaz/aipm-resume-analyzer/issues
- **Discussions**: https://github.com/abediaz/aipm-resume-analyzer/discussions
- **Email**: abe@aipmframework.com
