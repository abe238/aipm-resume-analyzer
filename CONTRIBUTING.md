# Contributing to the Applied AI PM Framework

Thanks for helping make AI PM hiring better! We welcome contributions from hiring managers, candidates, and developers.

## 🎯 What We're Looking For

### Framework Improvements
- Evidence-based criteria refinements
- Bias reduction and fairness improvements
- Real-world validation and calibration insights
- New evaluation signals

### Technical Contributions
- Additional AI provider integrations
- Performance optimizations
- Bug fixes and error handling
- Test coverage improvements

### Documentation & Examples
- Usage guides and tutorials
- Case studies and examples
- Best practices for hiring teams
- Candidate success stories

## 🚀 Quick Start

**Found a bug or have an idea?** [Open an issue](https://github.com/abe238/aipm-resume-analyzer/issues/new)

**Want to contribute code?**
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-improvement`
3. Make your changes
4. Test thoroughly
5. Submit a PR with a clear description

**Development Setup:**
```bash
git clone https://github.com/abe238/aipm-resume-analyzer.git
cd aipm-resume-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python -m pytest  # Run tests
```

## 📋 Guidelines

### Before You Start
- Check existing issues/PRs to avoid duplicates
- For significant changes, open an issue first to discuss
- Keep PRs focused on a single improvement

### Framework Changes
Proposed criteria changes should include:
- **Rationale**: Why this improves evaluation quality
- **Evidence**: Research, examples, or industry validation
- **Fairness**: How it avoids bias against non-traditional backgrounds

### Code Quality
- Follow existing code style (PEP 8 for Python)
- Add tests for new features
- Update documentation
- No hardcoded credentials or API keys
- Use type hints for Python functions

### Commit Messages
Use clear, descriptive commit messages:
- `feat: Add new scoring algorithm for technical depth`
- `fix: Correct provider.upper() typo in HTML generation`
- `docs: Update README with installation instructions`
- `refactor: Simplify prompt construction logic`

## 🤝 Community Values

This framework exists to democratize access to AI PM roles. We value:
- **Evidence over opinion**: Data-driven improvements
- **Accessibility**: Welcoming non-traditional backgrounds
- **Transparency**: Open discussion of tradeoffs
- **Rigor**: High standards without gatekeeping

## 🧪 Testing Your Changes

Before submitting a PR, make sure to:
1. Run the test suite: `pytest`
2. Test with sample resumes
3. Verify HTML output renders correctly
4. Check that all API providers work (if applicable)

## 📝 Pull Request Process

1. **Update documentation** if you're adding/changing features
2. **Add tests** for new functionality
3. **Link related issues** in the PR description
4. **Describe your changes** clearly with examples if possible
5. **Request review** from maintainers
6. **Address feedback** promptly and professionally

## 💡 Ideas for Contributions

Not sure where to start? Here are some ideas:

### Easy / Good First Issues
- Fix typos in documentation
- Add more example resumes
- Improve error messages
- Add input validation

### Medium Complexity
- Add new AI provider integration
- Improve scoring algorithms
- Enhance HTML template styling
- Add export formats (JSON, CSV)

### Advanced
- Multi-language support
- Batch processing capabilities
- Web interface for the analyzer
- Integration with ATS systems

## 💬 Questions?

- **General questions**: Open a [GitHub Discussion](https://github.com/abe238/aipm-resume-analyzer/discussions)
- **Bug reports**: [Create an issue](https://github.com/abe238/aipm-resume-analyzer/issues/new)
- **Feature requests**: [Create an issue](https://github.com/abe238/aipm-resume-analyzer/issues/new) with the "enhancement" label

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers and diverse perspectives
- Focus on constructive feedback
- No harassment, discrimination, or gatekeeping

### Enforcement
Violations of the code of conduct should be reported by creating an issue or contacting the maintainers directly. All reports will be reviewed and investigated promptly.

---

**Built with ❤️ by the community, for the community.**

Thank you for contributing to making AI PM hiring more transparent, fair, and rigorous!
