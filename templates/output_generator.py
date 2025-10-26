"""
Output generators for resume analysis reports
Generates beautiful markdown and HTML reports
"""

from datetime import datetime
from pathlib import Path


def generate_markdown(analysis, output_path):
    """Generate markdown report"""

    candidate = analysis.get('candidate_name', 'Candidate')
    now = datetime.now()
    date_formatted = now.strftime('%B %d, %Y at %H:%M:%S')
    total_score = analysis.get('total_score', 0)
    weighted_score = analysis.get('weighted_score', 0)
    decision = analysis.get('decision', 'Unknown')
    pillars = analysis.get('pillars', {})
    strengths = analysis.get('top_strengths', [])
    concerns = analysis.get('top_concerns', [])
    recommendation = analysis.get('recommendation', '')
    suitable_roles = analysis.get('suitable_roles', [])

    # Extract model metadata
    metadata = analysis.get('_metadata', {})
    model_name = metadata.get('model_display_name', 'Unknown Model')

    md_content = f"""# AI PM Resume Analysis: {candidate}

**Analysis Date**: {date_formatted}
**Model**: {model_name}
**Total Score**: {total_score}/60 ({weighted_score}/100 weighted)
**Decision**: **{decision}**

---

## Executive Summary

{recommendation}

### Decision Criteria

| Score Range | Decision | Meaning |
|-------------|----------|---------|
| 8.0 - 10.0 | **Strong Screen** | Top candidate, prioritize for interview |
| 6.5 - 7.9 | **Screen** | Solid candidate, invite to interview |
| 5.0 - 6.4 | **Maybe** | Borderline, use additional criteria |
| Below 5.0 | **No Screen** | Does not meet bar |

**This Candidate**: {decision} ({weighted_score}/100)

---

## Top 3 Strengths

"""

    for i, strength in enumerate(strengths[:3], 1):
        md_content += f"{i}. {strength}\n"

    md_content += f"""
---

## Top 3 Concerns

"""

    for i, concern in enumerate(concerns[:3], 1):
        md_content += f"{i}. {concern}\n"

    md_content += f"""
---

## Pillar-by-Pillar Analysis

"""

    # Add each pillar
    for pillar_key, pillar_data in pillars.items():
        name = pillar_data.get('name', pillar_key)
        score = pillar_data.get('score', 0)
        level = pillar_data.get('level', 0)
        evidence = pillar_data.get('evidence', '')
        pillar_strengths = pillar_data.get('strengths', [])
        pillar_gaps = pillar_data.get('gaps', [])

        level_names = {1: "Developing", 2: "Functional", 3: "Proficient", 4: "Advanced", 5: "Expert"}
        level_name = level_names.get(level, "Unknown")

        # Score bar
        score_bar = "█" * score + "░" * (10 - score)

        md_content += f"""### {name}

**Score**: {score}/10  `{score_bar}`
**Level**: {level_name} (Level {level}/5)

**Evidence from Resume**:
{evidence}

**Strengths**:
"""
        for strength in pillar_strengths:
            md_content += f"- ✅ {strength}\n"

        md_content += f"""
**Gaps/Concerns**:
"""
        for gap in pillar_gaps:
            md_content += f"- ⚠️ {gap}\n"

        md_content += "\n---\n\n"

    # Suitable roles
    if suitable_roles:
        md_content += f"""## Better Fit Roles

Based on this candidate's profile, they may be a better fit for:

"""
        for role in suitable_roles:
            md_content += f"- {role}\n"

        md_content += "\n---\n\n"

    # Footer
    md_content += f"""
## About This Analysis

This resume was analyzed using the **Applied AI PM Evaluation Framework** - an open-source, standardized evaluation system for AI Product Manager candidates.

**Framework**: 6 Pillars (Technical Skills, Product Thinking, AI/ML Knowledge, Communication, Strategic Thinking, Execution)

**Model Used**: {model_name}

**Learn more**: https://github.com/abe238/aipm-resume-analyzer

---

*Analysis generated on {date_formatted}*
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(md_content)


def generate_html(analysis, output_path):
    """Generate HTML report with beautiful CSS"""

    candidate = analysis.get('candidate_name', 'Candidate')
    now = datetime.now()
    date_formatted = now.strftime('%B %d, %Y at %H:%M:%S')
    total_score = analysis.get('total_score', 0)
    weighted_score = analysis.get('weighted_score', 0)
    decision = analysis.get('decision', 'Unknown')
    pillars = analysis.get('pillars', {})
    strengths = analysis.get('top_strengths', [])
    concerns = analysis.get('top_concerns', [])
    recommendation = analysis.get('recommendation', '')
    suitable_roles = analysis.get('suitable_roles', [])

    # Extract model metadata
    metadata = analysis.get('_metadata', {})
    model_name = metadata.get('model_display_name', 'Unknown Model')

    # Decision styling
    decision_class = {
        "Strong Screen": "strong-screen",
        "Screen": "screen",
        "Maybe": "maybe",
        "No Screen": "no-screen"
    }.get(decision, "maybe")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI PM Resume Analysis: {candidate}</title>
    <style>
        /* Design inspiration from Stripe Docs + Tailwind CSS + Material-UI */

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #2D3748;
            background: #F7FAFC;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            overflow: hidden;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
            color: white;
            padding: 40px;
        }}

        .header h1 {{
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .header .meta {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}

        /* Score Badge */
        .score-badge {{
            display: inline-block;
            margin-top: 16px;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
        }}

        /* Decision Badge */
        .decision-badge {{
            display: inline-block;
            margin-top: 8px;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .decision-badge.strong-screen {{
            background: #10B981;
            color: white;
        }}

        .decision-badge.screen {{
            background: #3B82F6;
            color: white;
        }}

        .decision-badge.maybe {{
            background: #F59E0B;
            color: white;
        }}

        .decision-badge.no-screen {{
            background: #EF4444;
            color: white;
        }}

        /* Content */
        .content {{
            padding: 40px;
        }}

        h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1A202C;
            margin: 32px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #E2E8F0;
        }}

        h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #2D3748;
            margin: 24px 0 12px 0;
        }}

        /* Executive Summary */
        .summary-box {{
            background: #F0F9FF;
            border-left: 4px solid #0066CC;
            padding: 20px;
            margin: 20px 0;
            border-radius: 6px;
        }}

        .summary-box p {{
            margin: 0;
            line-height: 1.7;
        }}

        /* Lists */
        .strength-list, .concern-list {{
            list-style: none;
            margin: 16px 0;
        }}

        .strength-list li {{
            padding: 12px;
            margin: 8px 0;
            background: #ECFDF5;
            border-left: 4px solid #10B981;
            border-radius: 4px;
        }}

        .strength-list li::before {{
            content: "✅ ";
            margin-right: 8px;
        }}

        .concern-list li {{
            padding: 12px;
            margin: 8px 0;
            background: #FEF3C7;
            border-left: 4px solid #F59E0B;
            border-radius: 4px;
        }}

        .concern-list li::before {{
            content: "⚠️ ";
            margin-right: 8px;
        }}

        /* Pillar Cards */
        .pillar-card {{
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 24px;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .pillar-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}

        .pillar-name {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #1A202C;
        }}

        .pillar-score {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #0066CC;
        }}

        .level-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: #E0E7FF;
            color: #4C51BF;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 12px;
        }}

        /* Progress Bar */
        .score-bar {{
            width: 100%;
            height: 8px;
            background: #E2E8F0;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0 16px 0;
        }}

        .score-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #0066CC 0%, #6C5CE7 100%);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}

        .evidence-box {{
            background: #F7FAFC;
            padding: 16px;
            border-radius: 6px;
            margin: 12px 0;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        .sub-list {{
            margin: 12px 0;
            padding-left: 0;
            list-style: none;
        }}

        .sub-list li {{
            padding: 8px 12px;
            margin: 6px 0;
            border-left: 3px solid #CBD5E0;
            padding-left: 16px;
        }}

        /* Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #E2E8F0;
        }}

        th {{
            background: #F7FAFC;
            font-weight: 600;
            color: #4A5568;
        }}

        /* Footer */
        .footer {{
            background: #F7FAFC;
            padding: 24px 40px;
            text-align: center;
            color: #718096;
            font-size: 0.9rem;
        }}

        .footer a {{
            color: #0066CC;
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        /* Roles Section */
        .roles-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 12px;
            margin: 16px 0;
        }}

        .role-item {{
            background: #EFF6FF;
            padding: 12px 16px;
            border-radius: 6px;
            border-left: 3px solid #3B82F6;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>AI PM Resume Analysis</h1>
            <div class="meta">Candidate: {candidate}</div>
            <div class="meta">Analysis Date: {date_formatted}</div>
            <div class="meta">Model: {model_name}</div>
            <div class="score-badge">
                Total Score: {total_score}/60 ({weighted_score}/100 weighted)
            </div>
            <div class="decision-badge {decision_class}">
                Decision: {decision}
            </div>
        </div>

        <!-- Content -->
        <div class="content">
            <!-- Executive Summary -->
            <h2>Executive Summary</h2>
            <div class="summary-box">
                <p>{recommendation}</p>
            </div>

            <!-- Decision Criteria Table -->
            <table>
                <thead>
                    <tr>
                        <th>Score Range</th>
                        <th>Decision</th>
                        <th>Meaning</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>8.0 - 10.0</td>
                        <td><strong>Strong Screen</strong></td>
                        <td>Top candidate, prioritize for interview</td>
                    </tr>
                    <tr>
                        <td>6.5 - 7.9</td>
                        <td><strong>Screen</strong></td>
                        <td>Solid candidate, invite to interview</td>
                    </tr>
                    <tr>
                        <td>5.0 - 6.4</td>
                        <td><strong>Maybe</strong></td>
                        <td>Borderline, use additional criteria</td>
                    </tr>
                    <tr>
                        <td>Below 5.0</td>
                        <td><strong>No Screen</strong></td>
                        <td>Does not meet bar</td>
                    </tr>
                </tbody>
            </table>

            <p><strong>This Candidate</strong>: {decision} ({weighted_score}/100)</p>

            <!-- Top Strengths -->
            <h2>Top 3 Strengths</h2>
            <ul class="strength-list">
"""

    for strength in strengths[:3]:
        html_content += f"                <li>{strength}</li>\n"

    html_content += """            </ul>

            <!-- Top Concerns -->
            <h2>Top 3 Concerns</h2>
            <ul class="concern-list">
"""

    for concern in concerns[:3]:
        html_content += f"                <li>{concern}</li>\n"

    html_content += """            </ul>

            <!-- Pillar Analysis -->
            <h2>Pillar-by-Pillar Analysis</h2>
"""

    # Add each pillar
    level_names = {1: "Developing", 2: "Functional", 3: "Proficient", 4: "Advanced", 5: "Expert"}

    for pillar_key, pillar_data in pillars.items():
        name = pillar_data.get('name', pillar_key)
        score = pillar_data.get('score', 0)
        level = pillar_data.get('level', 0)
        evidence = pillar_data.get('evidence', '')
        pillar_strengths = pillar_data.get('strengths', [])
        pillar_gaps = pillar_data.get('gaps', [])

        level_name = level_names.get(level, "Unknown")
        score_percent = (score / 10) * 100

        html_content += f"""
            <div class="pillar-card">
                <div class="pillar-header">
                    <div class="pillar-name">{name}</div>
                    <div class="pillar-score">{score}/10</div>
                </div>
                <div class="level-badge">Level {level}: {level_name}</div>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: {score_percent}%"></div>
                </div>

                <h3>Evidence from Resume</h3>
                <div class="evidence-box">
                    {evidence}
                </div>

                <h3>Strengths</h3>
                <ul class="sub-list">
"""
        for strength in pillar_strengths:
            html_content += f"                    <li>✅ {strength}</li>\n"

        html_content += """                </ul>

                <h3>Gaps/Concerns</h3>
                <ul class="sub-list">
"""
        for gap in pillar_gaps:
            html_content += f"                    <li>⚠️ {gap}</li>\n"

        html_content += """                </ul>
            </div>
"""

    # Suitable roles
    if suitable_roles:
        html_content += """
            <!-- Better Fit Roles -->
            <h2>Better Fit Roles</h2>
            <p>Based on this candidate's profile, they may be a better fit for:</p>
            <div class="roles-list">
"""
        for role in suitable_roles:
            html_content += f"                <div class=\"role-item\">{role}</div>\n"

        html_content += """            </div>
"""

    # Footer
    html_content += f"""
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>This resume was analyzed using the <strong>Applied AI PM Evaluation Framework</strong></p>
            <p>An open-source, standardized evaluation system for AI Product Manager candidates</p>
            <p><strong>Model Used:</strong> {model_name}</p>
            <p><a href="https://github.com/abe238/aipm-resume-analyzer" target="_blank">Learn more about the framework</a></p>
            <p style="margin-top: 16px; font-size: 0.85rem;">Analysis generated on {date_formatted}</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)


def generate_aggregated_report(analyses, output_path):
    """Generate aggregated report from multiple provider analyses"""

    # Get candidate name from first analysis
    candidate = list(analyses.values())[0].get('candidate_name', 'Candidate')
    now = datetime.now()
    date_formatted = now.strftime('%B %d, %Y at %H:%M:%S')

    # Calculate consensus scores
    pillar_keys = ['pillar_1', 'pillar_2', 'pillar_3', 'pillar_4', 'pillar_5', 'pillar_6']
    pillar_names = ['Technical Skills', 'Product Thinking', 'AI/ML Knowledge',
                    'Communication', 'Strategic Thinking', 'Execution']

    consensus_scores = {}
    for i, pillar_key in enumerate(pillar_keys):
        scores = [a.get('pillars', {}).get(pillar_key, {}).get('score', 0) for a in analyses.values()]
        consensus_scores[pillar_names[i]] = {
            'avg': round(sum(scores) / len(scores), 1) if scores else 0,
            'min': min(scores) if scores else 0,
            'max': max(scores) if scores else 0,
            'scores': {provider: score for provider, score in zip(analyses.keys(), scores)}
        }

    # Calculate total scores
    total_scores = {provider: a.get('total_score', 0) for provider, a in analyses.items()}
    avg_total = round(sum(total_scores.values()) / len(total_scores), 1)

    # Get all strengths and concerns
    all_strengths = []
    all_concerns = []
    for provider, analysis in analyses.items():
        provider_display = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        for strength in analysis.get('top_strengths', []):
            all_strengths.append(f"**[{provider_display}]** {strength}")
        for concern in analysis.get('top_concerns', []):
            all_concerns.append(f"**[{provider_display}]** {concern}")

    # Build markdown content
    md_content = f"""# Deep AI PM Resume Analysis: {candidate}

**Analysis Date**: {date_formatted}
**Providers**: {', '.join([a.get('_metadata', {}).get('model_display_name', p.upper()) for p, a in analyses.items()])}
**Consensus Score**: {avg_total}/60

---

## 🔬 Deep Analysis Overview

This is an **aggregated deep analysis** using multiple AI providers to provide maximum feedback and diverse perspectives on the candidate's profile.

**Providers analyzed:**
"""

    for provider, analysis in analyses.items():
        model_name = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        score = analysis.get('total_score', 0)
        decision = analysis.get('decision', 'Unknown')
        md_content += f"- **{model_name}**: {score}/60 - {decision}\n"

    md_content += f"""
**Consensus Total Score**: {avg_total}/60

---

## 📊 Consensus Pillar Scores

| Pillar | Avg | Min | Max | {' | '.join([a.get('_metadata', {}).get('model_display_name', p)[:15] for p, a in analyses.items()])} |
|--------|-----|-----|-----|{'----|' * len(analyses)}
"""

    for pillar_name in pillar_names:
        scores_data = consensus_scores[pillar_name]
        provider_scores = ' | '.join([str(scores_data['scores'].get(p, 0)) for p in analyses.keys()])
        md_content += f"| {pillar_name} | {scores_data['avg']}/10 | {scores_data['min']} | {scores_data['max']} | {provider_scores} |\n"

    md_content += f"""
---

## ✨ All Identified Strengths

"""

    for i, strength in enumerate(all_strengths, 1):
        md_content += f"{i}. {strength}\n"

    md_content += f"""
---

## ⚠️ All Identified Concerns

"""

    for i, concern in enumerate(all_concerns, 1):
        md_content += f"{i}. {concern}\n"

    md_content += """
---

## 📋 Detailed Analysis by Provider

"""

    for provider, analysis in analyses.items():
        model_name = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        score = analysis.get('total_score', 0)
        decision = analysis.get('decision', 'Unknown')
        recommendation = analysis.get('recommendation', '')

        md_content += f"""
### {model_name}

**Score**: {score}/60 | **Decision**: {decision}

**Executive Summary:**
{recommendation}

**Pillar Breakdown:**
"""

        for i, pillar_key in enumerate(pillar_keys):
            pillar_data = analysis.get('pillars', {}).get(pillar_key, {})
            pillar_score = pillar_data.get('score', 0)
            pillar_level = pillar_data.get('level', 'Unknown')
            md_content += f"- **{pillar_names[i]}**: {pillar_score}/10 ({pillar_level})\n"

        md_content += "\n"

    md_content += f"""
---

## 💡 How to Use This Deep Analysis

This report aggregates insights from multiple AI models to provide:
- **Consensus view**: Where all models agree, there's high confidence
- **Diverse perspectives**: Different models may emphasize different strengths/concerns
- **Comprehensive feedback**: More detailed than single-provider analysis

**Action items:**
1. Review consensus scores for overall assessment
2. Note where models disagree - these areas may need human judgment
3. Read all identified strengths and concerns for complete picture
4. Review individual provider analyses for detailed reasoning

---

## About This Analysis

**Aggregated Deep Analysis** using the Applied AI PM Evaluation Framework

**Framework**: 6 Pillars (Technical Skills, Product Thinking, AI/ML Knowledge, Communication, Strategic Thinking, Execution)

**Providers Used**: {', '.join([a.get('_metadata', {}).get('model_display_name', p.upper()) for p, a in analyses.items()])}

**Learn more**: https://github.com/abe238/aipm-resume-analyzer

---

*Deep analysis generated on {date_formatted}*
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(md_content)
