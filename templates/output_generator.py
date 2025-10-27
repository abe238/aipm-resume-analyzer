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

    # Extract new framework fields
    min_thresholds = analysis.get('minimum_thresholds_met', {})
    red_flags = analysis.get('red_flags_found', [])
    yellow_flags = analysis.get('yellow_flags_found', [])
    critical_q = analysis.get('critical_questions_analysis', {})
    must_have = analysis.get('must_have_signals', {})
    diff_signals = analysis.get('differentiation_signals', {})
    decision_rationale = analysis.get('decision_rationale', '')
    interview_areas = analysis.get('interview_focus_areas', [])
    design_eval = analysis.get('design_evaluation', {})

    md_content = f"""# AI PM Resume Analysis: {candidate}

**Analysis Date**: {date_formatted}
**Model**: {model_name}
**Total Score**: {total_score}/60
**Decision**: **{decision}**

---

## Executive Summary

{recommendation}

**Decision Rationale**: {decision_rationale}

### 2025 Framework Evaluation

| Criteria | Status |
|----------|--------|
| **Minimum Thresholds** | {"✅ All Met" if min_thresholds.get('all_met') else "❌ Failed"} |
| **Red Flags** | {"❌ " + str(len(red_flags)) + " Found" if red_flags else "✅ None"} |
| **Must-Have Signals** | {"✅ All Present" if must_have.get('all_present') else "⚠️ " + str(len(must_have.get('signals_missing', []))) + " Missing"} |
| **Differentiation Signals** | {diff_signals.get('count', 0)}/8 ({" ✅ Sufficient" if diff_signals.get('sufficient_for_strong_screen') else "⚠️ Needs More"})|

---

## Minimum Thresholds

"""

    if min_thresholds:
        md_content += f"""
- **Personal AI Projects**: {"✅ Met" if min_thresholds.get('personal_ai_projects') else "❌ Not Met"}
- **Building in Public**: {"✅ Met" if min_thresholds.get('building_in_public') else "❌ Not Met"}
- **Resume Creativity**: {"✅ Met" if min_thresholds.get('resume_creativity') else "❌ Not Met"}

"""

    # Red and Yellow Flags
    if red_flags:
        md_content += f"""## 🚩 Red Flags (Critical Issues)

"""
        for flag in red_flags:
            md_content += f"- ❌ {flag}\n"
        md_content += "\n"

    if yellow_flags:
        md_content += f"""## ⚠️ Yellow Flags (Investigate Further)

"""
        for flag in yellow_flags:
            md_content += f"- ⚠️ {flag}\n"
        md_content += "\n"

    # Critical Questions Analysis
    if critical_q:
        md_content += f"""---

## The Three Critical Questions Analysis

### 1. Paradigm Shift (Car vs. Faster Horse)
"""
        for ex in critical_q.get('paradigm_shift_examples', []):
            md_content += f"- {ex}\n"

        md_content += f"""
### 2. Future-Proofing (Gets Better with AI Advances)
"""
        for ex in critical_q.get('future_proofing_examples', []):
            md_content += f"- {ex}\n"

        md_content += f"""
### 3. Magic Wand Test (Designed for Full Automation)
"""
        for ex in critical_q.get('magic_wand_examples', []):
            md_content += f"- {ex}\n"
        md_content += "\n"

    # Design Evaluation
    if design_eval:
        md_content += f"""---

## Resume Design Evaluation

**Design Score**: {design_eval.get('score', 'N/A')}/10

**Comments**: {design_eval.get('comments', 'Visual analysis not available')}

"""

    md_content += f"""---

## Must-Have Signals

**Signals Found** ({len(must_have.get('signals_found', []))}/5):
"""
    for signal in must_have.get('signals_found', []):
        md_content += f"- ✅ {signal}\n"

    if must_have.get('signals_missing'):
        md_content += f"""
**Signals Missing** ({len(must_have.get('signals_missing', []))}/5):
"""
        for signal in must_have.get('signals_missing', []):
            md_content += f"- ❌ {signal}\n"

    md_content += f"""
---

## Differentiation Signals

**Count**: {diff_signals.get('count', 0)}/8 (Need 3+ for Strong Screen)

**Signals Found**:
"""
    for signal in diff_signals.get('signals_found', []):
        md_content += f"- ✅ {signal}\n"

    md_content += f"""
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

    # Interview focus areas
    if interview_areas:
        md_content += f"""## Interview Focus Areas

If moving forward, probe these areas in depth:

"""
        for area in interview_areas:
            md_content += f"- {area}\n"

        md_content += "\n---\n\n"

    # Footer
    md_content += f"""
## About This Analysis

This resume was analyzed using the **Applied AI PM Evaluation Framework** - an open-source, rigorous evaluation system for 2025 AI Product Manager candidates.

**Framework**: 6 Pillars with 2025 standards - Technical Skills & Hands-On Building, Product Thinking & 0-to-1 Leadership, Deep AI Intuition (non-negotiable), Communication & Storytelling, Strategic Thinking & Second-Order Vision, Full-Spectrum Execution & Rapid Shipping

**Key Criteria**: Minimum thresholds (personal AI projects, building in public, resume creativity), The Three Critical Questions (paradigm shift, future-proofing, magic wand test), Must-have signals, Differentiation signals, Red/yellow flags

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

    # Extract new framework fields
    min_thresholds = analysis.get('minimum_thresholds_met', {})
    red_flags = analysis.get('red_flags_found', [])
    yellow_flags = analysis.get('yellow_flags_found', [])
    critical_q = analysis.get('critical_questions_analysis', {})
    must_have = analysis.get('must_have_signals', {})
    diff_signals = analysis.get('differentiation_signals', {})
    decision_rationale = analysis.get('decision_rationale', '')
    interview_areas = analysis.get('interview_focus_areas', [])
    design_eval = analysis.get('design_evaluation', {})

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
        /*
         * ULTRA COMPACT VARIATION #23
         * Aggressive space reduction optimizations for time-constrained users
         * - Hero: 50vh (was 80vh) - saves 30% vertical space
         * - Section padding: 2rem (was 3rem) - 33% reduction
         * - Card padding: 1.5rem (was 2-2.5rem)
         * - Tighter line-heights and margins throughout
         * - Mobile: 60vh hero (was 100vh)
         */

        /* Modern Minimal Typography - Quattrocento (UNCHANGED) */
        @import url('https://fonts.googleapis.com/css2?family=Quattrocento:wght@400;700&display=swap');

        /* Anthropic Color Palette - Warm Tan/Orange Brand Colors */
        :root:not(.dark) {{
            /* Anthropic design system tokens */
            --accent-brand: 15 63.1% 59.6%;  /* Warm tan/orange */
            --accent-main-000: 15 55.6% 52.4%;
            --accent-main-100: 15 55.6% 52.4%;
            --accent-main-200: 15 63.1% 59.6%;
            --bg-000: 0 0% 100%;  /* Pure white */
            --bg-100: 48 33.3% 97.1%;  /* Warm off-white */
            --bg-200: 53 28.6% 94.5%;  /* Warm light gray */
            --bg-300: 48 25% 92.2%;
            --bg-400: 50 20.7% 88.6%;
            --bg-500: 50 20.7% 88.6%;
            --border-300: 30 3.3% 11.8%;
            --border-400: 30 3.3% 11.8%;
            --text-000: 60 2.6% 7.6%;  /* Near black */
            --text-100: 60 2.6% 7.6%;
            --text-200: 60 2.5% 23.3%;  /* Dark gray */
            --text-300: 60 2.5% 23.3%;
            --oncolor-100: 0 0% 100%;
            --primary: #c96442;  /* Warm tan/orange */
            --primary-foreground: #ffffff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Quattrocento', Georgia, serif;
            background: hsl(var(--bg-100));
            color: hsl(var(--text-100));
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
            max-width: 100vw;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1rem;
            color: hsl(var(--text-000));
        }}

        h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); }}
        h2 {{ font-size: clamp(1.75rem, 4vw, 2.5rem); }}
        h3 {{ font-size: clamp(1.5rem, 3vw, 2rem); }}
        h4 {{ font-size: clamp(1.25rem, 2.5vw, 1.5rem); }}

        p {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: 1rem;
            line-height: 1.65rem;
            margin-bottom: 1rem;
            color: hsl(var(--text-200));
        }}

        a {{
            color: var(--primary);
            text-decoration: none;
            transition: opacity 0.2s ease;
        }}

        a:hover {{
            opacity: 0.8;
        }}

        /* Container - wider gutters */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            width: 100%;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            font-size: 0.9375rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }}

        thead {{
            background: var(--primary);
            color: white;
        }}

        th {{
            padding: 1rem 1.25rem;
            text-align: left;
            font-weight: 600;
            color: white;
        }}

        td {{
            padding: 0.875rem 1.25rem;
            border-bottom: 1px solid hsl(var(--border-300));
            color: hsl(var(--text-200));
        }}

        tbody tr:hover {{
            background: hsl(var(--bg-200));
        }}

        /* Header with scroll shadow */
        header {{
            background: hsl(var(--bg-000) / 0.95);
            border-bottom: 0.5px solid hsl(var(--border-400) / 0.25);
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(10px);
            transition: box-shadow 0.3s ease;
        }}

        header.scrolled {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 4rem;
        }}

        .logo {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            font-size: 1.125rem;
            color: var(--primary);
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}

        .nav-links a {{
            color: hsl(var(--text-100));
            font-size: 0.9375rem;
            font-weight: 500;
            transition: color 0.2s ease;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid transparent;
        }}

        .nav-links a:hover,
        .nav-links a.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
            opacity: 1;
        }}

        @media (max-width: 768px) {{
            nav {{
                height: auto;
                padding: 0.75rem 0;
            }}

            .logo {{
                font-size: 1rem;
            }}

            .nav-links {{
                gap: 0.5rem;
                flex-wrap: wrap;
                justify-content: flex-end;
            }}

            .nav-links a {{
                font-size: 0.75rem;
                padding: 0.25rem 0.5rem;
            }}
        }}

        /* Buttons - Updated for deep blue primary */
        .btn {{
            position: relative;
            display: inline-flex;
            gap: 0.5rem;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            min-width: 5rem;
            height: 2.5rem;
            padding: 0.625rem 1.5rem;
            white-space: nowrap;
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            border-radius: 0.5rem;
            font-size: 1rem;
            text-decoration: none;
            transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn:active {{
            transform: scale(0.985);
        }}

        .btn-primary {{
            color: #ffffff;
            background-color: var(--primary);
            border: none;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}

        .btn-primary:hover {{
            background-color: #b5573a;
            opacity: 1;
        }}

        .btn-secondary {{
            color: var(--primary);
            background-color: transparent;
            border: 1px solid var(--primary);
        }}

        .btn-secondary:hover {{
            background-color: rgba(201, 100, 66, 0.1);
            opacity: 1;
        }}

        .cta-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}

        /* Hero Section - ULTRA COMPACT: 50vh Height */
        .hero {{
            position: relative;
            min-height: 50vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #fff;
            padding: 1rem 0;
        }}

        .hero-bg {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, rgba(30,10,5,0.85), rgba(60,30,20,0.9)),
                        radial-gradient(ellipse at top, rgba(201,100,66,0.3), transparent 50%);
            z-index: -1;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
        }}

        .hero h1 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            font-size: clamp(2.5rem, 5vw, 3.5rem);
            margin-bottom: 0.5rem;
            color: #ffffff;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 1.1rem;
            max-width: 650px;
            margin: 0 auto 1rem;
            color: rgba(255,255,255,0.85);
            line-height: 1.4;
        }}

        /* Scroll down indicator */
        .scroll-down {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(255,255,255,0.7);
            font-size: 2rem;
            animation: bounce 2s infinite;
            cursor: pointer;
        }}

        @keyframes bounce {{
            0%, 100% {{ transform: translate(-50%, 0); }}
            50% {{ transform: translate(-50%, 10px); }}
        }}

        /* Sections - ULTRA COMPACT */
        section {{
            padding: 2rem 0;
        }}

        .section-header {{
            text-align: center;
            margin-bottom: 1.5rem;
        }}

        .section-header h2 {{
            margin-bottom: 0.5rem;
        }}

        .section-header p {{
            font-size: 1.125rem;
            color: hsl(var(--text-300));
        }}

        /* Cards - ULTRA COMPACT */
        .card {{
            background: hsl(var(--bg-000));
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        .card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }}

        .card h3 {{
            margin-bottom: 0.75rem;
            font-size: 1.35rem;
            color: var(--primary);
        }}

        /* Reduce font-size for philosophy section to prevent wrapping */
        #philosophy .card h3 {{
            font-size: 1.15rem;
        }}

        .card p {{
            color: hsl(var(--text-300));
            margin-bottom: 0.5rem;
        }}

        /* Grid Layouts - Wider gutters */
        .grid {{
            display: grid;
            gap: 2.5rem;
        }}

        .grid-2 {{
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        }}

        .grid-3 {{
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        }}

        /* Pillar Cards - ULTRA COMPACT */
        .pillar-card {{
            background: linear-gradient(135deg, hsl(var(--bg-000)) 0%, hsl(var(--bg-100)) 100%);
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        .pillar-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }}

        .pillar-number {{
            display: inline-block;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--primary);
            margin-right: 0.5rem;
        }}

        .pillar-card h3 {{
            display: inline;
            color: var(--primary);
            margin-bottom: 0;
            font-size: 1.5rem;
        }}

        .pillar-card p {{
            display: block;
            margin-top: 0.75rem;
        }}

        .pillar-card ul {{
            list-style: none;
            margin-top: 1rem;
        }}

        .pillar-card li {{
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: hsl(var(--text-200));
        }}

        .pillar-card li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
        }}

        /* Decision Framework */
        .decision-flow {{
            background: hsl(var(--bg-200));
            border-radius: 12px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        .decision-step {{
            padding: 1.5rem;
            margin: 1.25rem 0;
            background: hsl(var(--bg-000));
            border-left: 4px solid var(--primary);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}

        .decision-step h4 {{
            color: var(--primary);
            margin-bottom: 0.75rem;
        }}

        .decision-step ol,
        .decision-step ul {{
            margin-left: 2rem;
            margin-top: 0.75rem;
        }}

        .decision-step li {{
            margin: 0.5rem 0;
            color: hsl(var(--text-200));
        }}

        .highlight-box {{
            background: hsl(var(--bg-100));
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin-top: 0.75rem;
            font-weight: 500;
            border-left: 3px solid var(--primary);
        }}

        /* Personal Story - ULTRA COMPACT */
        .story-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem 1.5rem;
            align-items: center;
            background: hsl(var(--bg-000));
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        }}

        .story-section h2 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: clamp(2rem, 4vw, 3rem);
            margin-bottom: 1rem;
            color: var(--primary);
        }}

        .story-section p {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: 1.125rem;
            line-height: 1.8;
            color: hsl(var(--text-200));
            margin-bottom: 1.5rem;
        }}

        .story-visual {{
            text-align: center;
        }}

        .story-visual img {{
            width: 100%;
            max-width: 400px;
            border-radius: 12px;
            object-fit: cover;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }}

        .caption {{
            text-align: center;
            font-size: 0.875rem;
            color: hsl(var(--text-300));
            margin-top: 0.75rem;
        }}

        .btn-link {{
            display: inline-block;
            margin-top: 1rem;
            font-weight: 600;
            color: var(--primary);
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .btn-link:hover {{
            text-decoration: underline;
        }}

        blockquote.highlight {{
            border-left: 4px solid var(--primary);
            padding-left: 1.5rem;
            font-style: italic;
            color: hsl(var(--text-300));
            margin: 1.5rem 0;
            font-size: 1.125rem;
        }}

        /* Video Container */
        .video-container {{
            position: relative;
            width: 100%;
            margin: 2rem 0;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}

        /* Scoring Stats Cards */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}

        .stat-card {{
            background: linear-gradient(135deg, hsl(var(--bg-000)) 0%, hsl(var(--bg-100)) 100%);
            border: none;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
            line-height: 1;
        }}

        .stat-label {{
            font-size: 1rem;
            font-weight: 600;
            color: hsl(var(--text-200));
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Footer - Consolidated CTAs */
        footer {{
            background: hsl(var(--bg-200));
            border-top: 0.5px solid hsl(var(--border-400));
            padding: 3rem 0 2rem;
            margin-top: 4rem;
        }}

        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2.5rem;
            margin-bottom: 2rem;
        }}

        .footer-section h4 {{
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
            color: var(--primary);
        }}

        .footer-section ul {{
            list-style: none;
        }}

        .footer-section li {{
            margin-bottom: 0.5rem;
        }}

        .footer-section a {{
            color: hsl(var(--text-200));
            font-size: 0.9375rem;
        }}

        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: none;
            color: hsl(var(--text-300));
            font-size: 0.875rem;
        }}

        /* Responsive - ULTRA COMPACT */
        @media (max-width: 768px) {{
            .container {{
                padding: 0 1rem;
            }}

            section {{
                padding: 1.5rem 0;
            }}

            .grid {{
                gap: 1.25rem;
            }}

            .hero {{
                min-height: 60vh;
                padding: 1rem 0;
            }}

            .hero h1 {{
                font-size: clamp(1.75rem, 7vw, 2.25rem);
                margin-bottom: 0.5rem;
            }}

            .hero p {{
                font-size: 1rem;
                margin-bottom: 1rem;
            }}

            .cta-buttons {{
                flex-direction: column;
                gap: 0.5rem;
                margin-top: 1rem;
            }}

            .btn {{
                width: 100%;
                max-width: 320px;
            }}

            .story-section {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
                padding: 1.5rem 1rem;
            }}

            .story-visual {{
                order: -1;
            }}

            .video-container {{
                margin: 1.5rem 0;
            }}

            table {{
                font-size: 0.8125rem;
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}

            th, td {{
                padding: 0.5rem 0.75rem;
                white-space: nowrap;
            }}

            .stats {{
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }}

            .stat-card {{
                padding: 1.5rem 1rem;
            }}

            .stat-number {{
                font-size: 2rem;
            }}

            .stat-label {{
                font-size: 0.875rem;
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
                {f'<p style="margin-top: 12px;"><strong>Decision Rationale:</strong> {decision_rationale}</p>' if decision_rationale else ''}
            </div>

            <!-- 2025 Framework Evaluation -->
            <h2>2025 Framework Evaluation</h2>
            <table>
                <thead>
                    <tr>
                        <th>Criteria</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Minimum Thresholds</strong></td>
                        <td>{"✅ All Met" if min_thresholds.get('all_met') else "❌ Failed"}</td>
                    </tr>
                    <tr>
                        <td><strong>Red Flags</strong></td>
                        <td>{"❌ " + str(len(red_flags)) + " Found" if red_flags else "✅ None"}</td>
                    </tr>
                    <tr>
                        <td><strong>Must-Have Signals</strong></td>
                        <td>{"✅ All Present" if must_have.get('all_present') else "⚠️ " + str(len(must_have.get('signals_missing', []))) + " Missing"}</td>
                    </tr>
                    <tr>
                        <td><strong>Differentiation Signals</strong></td>
                        <td>{diff_signals.get('count', 0)}/8 ({" ✅ Sufficient" if diff_signals.get('sufficient_for_strong_screen') else "⚠️ Needs More"})</td>
                    </tr>
                </tbody>
            </table>

            <!-- Minimum Thresholds -->
            <h2>Minimum Thresholds</h2>
            <ul class="sub-list">
                <li>{"✅" if min_thresholds.get('personal_ai_projects') else "❌"} Personal AI Projects</li>
                <li>{"✅" if min_thresholds.get('building_in_public') else "❌"} Building in Public</li>
                <li>{"✅" if min_thresholds.get('resume_creativity') else "❌"} Resume Creativity</li>
            </ul>
"""

    # Add Red Flags section if any
    if red_flags:
        html_content += """
            <!-- Red Flags -->
            <h2>🚩 Red Flags (Critical Issues)</h2>
            <ul class="concern-list">
"""
        for flag in red_flags:
            html_content += f"                <li>{flag}</li>\n"
        html_content += """            </ul>
"""

    # Add Yellow Flags section if any
    if yellow_flags:
        html_content += """
            <!-- Yellow Flags -->
            <h2>⚠️ Yellow Flags (Investigate Further)</h2>
            <ul class="concern-list" style="background: #FEF3C7; border-left-color: #F59E0B;">
"""
        for flag in yellow_flags:
            html_content += f"                <li>{flag}</li>\n"
        html_content += """            </ul>
"""

    # Add Critical Questions Analysis
    if critical_q:
        html_content += """
            <!-- Critical Questions Analysis -->
            <h2>The Three Critical Questions Analysis</h2>

            <h3>1. Paradigm Shift (Car vs. Faster Horse)</h3>
            <ul class="sub-list">
"""
        for ex in critical_q.get('paradigm_shift_examples', []):
            html_content += f"                <li>{ex}</li>\n"
        html_content += """            </ul>

            <h3>2. Future-Proofing (Gets Better with AI Advances)</h3>
            <ul class="sub-list">
"""
        for ex in critical_q.get('future_proofing_examples', []):
            html_content += f"                <li>{ex}</li>\n"
        html_content += """            </ul>

            <h3>3. Magic Wand Test (Designed for Full Automation)</h3>
            <ul class="sub-list">
"""
        for ex in critical_q.get('magic_wand_examples', []):
            html_content += f"                <li>{ex}</li>\n"
        html_content += """            </ul>
"""

    # Add Design Evaluation
    if design_eval:
        html_content += f"""
            <!-- Resume Design Evaluation -->
            <h2>Resume Design Evaluation</h2>
            <div class="summary-box" style="background: #F0FDF4; border-left-color: #10B981;">
                <p><strong>Design Score:</strong> {design_eval.get('score', 'N/A')}/10</p>
                <p style="margin-top: 8px;">{design_eval.get('comments', 'Visual analysis not available')}</p>
            </div>
"""

    # Add Must-Have Signals
    html_content += f"""
            <!-- Must-Have Signals -->
            <h2>Must-Have Signals</h2>
            <p><strong>Signals Found</strong> ({len(must_have.get('signals_found', []))}/5):</p>
            <ul class="strength-list">
"""
    for signal in must_have.get('signals_found', []):
        html_content += f"                <li>{signal}</li>\n"
    html_content += """            </ul>
"""

    if must_have.get('signals_missing'):
        html_content += f"""
            <p><strong>Signals Missing</strong> ({len(must_have.get('signals_missing', []))}/5):</p>
            <ul class="concern-list">
"""
        for signal in must_have.get('signals_missing', []):
            html_content += f"                <li>{signal}</li>\n"
        html_content += """            </ul>
"""

    # Add Differentiation Signals
    html_content += f"""
            <!-- Differentiation Signals -->
            <h2>Differentiation Signals</h2>
            <p><strong>Count:</strong> {diff_signals.get('count', 0)}/8 (Need 3+ for Strong Screen)</p>
            <p><strong>Signals Found:</strong></p>
            <ul class="strength-list">
"""
    for signal in diff_signals.get('signals_found', []):
        html_content += f"                <li>{signal}</li>\n"
    html_content += """            </ul>

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

    # Interview focus areas
    if interview_areas:
        html_content += """
            <!-- Interview Focus Areas -->
            <h2>Interview Focus Areas</h2>
            <p>If moving forward, probe these areas in depth:</p>
            <ul class="sub-list">
"""
        for area in interview_areas:
            html_content += f"                <li>{area}</li>\n"

        html_content += """            </ul>
"""

    # Footer
    html_content += f"""
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>This resume was analyzed using the <strong>Applied AI PM Evaluation Framework</strong></p>
            <p>A rigorous, open-source evaluation system for 2025 AI Product Manager candidates</p>
            <p><strong>Framework:</strong> 6 Pillars with 2025 standards - Technical Skills & Hands-On Building, Product Thinking & 0-to-1 Leadership, Deep AI Intuition (non-negotiable), Communication & Storytelling, Strategic Thinking & Second-Order Vision, Full-Spectrum Execution & Rapid Shipping</p>
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


def group_feedback_by_theme(feedback_items):
    """Group strengths/concerns by theme for better readability"""

    # Define themes with keywords to match
    themes = {
        "AI Experience & Technical Knowledge": ["ai", "ml", "machine learning", "technical", "hands-on", "coding", "engineering"],
        "Building in Public & Portfolio": ["public", "github", "blog", "portfolio", "thought leadership", "linkedin", "speaking"],
        "Product Management Background": ["product management", "pm experience", "product work", "0-to-1", "shipped"],
        "Strategic & Systems Thinking": ["platform", "second-order", "paradigm shift", "strategic", "systems", "future-proof"],
        "Execution Speed & Velocity": ["rapid", "hours", "days", "velocity", "prototyping", "shipping", "speed"],
        "Resume Quality & Creativity": ["resume", "design", "creativity", "plain text", "visual", "product taste"],
        "Career Narrative & Trajectory": ["career", "pivot", "narrative", "journey", "compelling story", "why ai"]
    }

    # Group items by theme
    grouped = {theme: [] for theme in themes.keys()}
    ungrouped = []

    for item in feedback_items:
        item_lower = item.lower()
        matched = False

        # Try to match to a theme
        for theme, keywords in themes.items():
            if any(keyword in item_lower for keyword in keywords):
                grouped[theme].append(item)
                matched = True
                break

        if not matched:
            ungrouped.append(item)

    # Build output with only themes that have items
    result = []
    for theme, items in grouped.items():
        if items:
            result.append((theme, items))

    # Add ungrouped items as "Other"
    if ungrouped:
        result.append(("Other", ungrouped))

    return result


def format_grouped_items_as_paragraph(items):
    """
    Convert list of items with provider tags at start into paragraph format with tags at end.

    Input: ["**[GPT-5]** Cross-functional...", "**[GPT-5]** Training and...", "**[Claude]** Strong operational..."]
    Output: "Cross-functional... Training and... [GPT-5] Strong operational... [Claude]"
    """
    import re

    # Parse items to extract provider and text
    provider_items = {}
    for item in items:
        # Match pattern like "**[Provider]** text" or "[Provider] text" or "<strong>[Provider]</strong> text"
        match = re.match(r'(?:\*\*|\<strong\>)?\[([^\]]+)\](?:\*\*|\<\/strong\>)?\s*(.*)', item)
        if match:
            provider = match.group(1)
            text = match.group(2).strip()
            if provider not in provider_items:
                provider_items[provider] = []
            provider_items[provider].append(text)
        else:
            # No provider tag found, treat as ungrouped
            if 'Other' not in provider_items:
                provider_items['Other'] = []
            provider_items['Other'].append(item.strip())

    # Build paragraph
    parts = []
    for provider, texts in provider_items.items():
        # Combine texts with periods
        combined = '. '.join(t.rstrip('.') for t in texts)
        # Ensure it ends with period before tag
        if not combined.endswith('.'):
            combined += '.'
        # Add provider tag at end (without bold formatting)
        if provider != 'Other':
            parts.append(f"{combined} [{provider}]")
        else:
            parts.append(combined)

    # Join all parts with space
    return ' '.join(parts)


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

    # Get all strengths and concerns with provider labels
    all_strengths = []
    all_concerns = []
    for provider, analysis in analyses.items():
        provider_display = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        for strength in analysis.get('top_strengths', []):
            all_strengths.append(f"**[{provider_display}]** {strength}")
        for concern in analysis.get('top_concerns', []):
            all_concerns.append(f"**[{provider_display}]** {concern}")

    # Group by theme for readability
    grouped_strengths = group_feedback_by_theme(all_strengths)
    grouped_concerns = group_feedback_by_theme(all_concerns)

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

| Pillar | Avg | Min | Max | {' | '.join([a.get('_metadata', {}).get('model_display_name', p) for p, a in analyses.items()])} |
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

    for theme, items in grouped_strengths:
        md_content += f"### {theme}\n\n"
        paragraph = format_grouped_items_as_paragraph(items)
        md_content += f"{paragraph}\n\n"

    md_content += f"""---

## ⚠️ All Identified Concerns

"""

    for theme, items in grouped_concerns:
        md_content += f"### {theme}\n\n"
        paragraph = format_grouped_items_as_paragraph(items)
        md_content += f"{paragraph}\n\n"

    # Aggregate suitable roles and interview focus areas
    all_roles = set()
    all_interview_areas = set()
    for provider, analysis in analyses.items():
        roles = analysis.get('suitable_roles', [])
        if roles:
            all_roles.update(roles)
        areas = analysis.get('interview_focus_areas', [])
        if areas:
            all_interview_areas.update(areas)

    # Add Better Fit Roles section
    if all_roles:
        md_content += """---

## Better Fit Roles

Based on this candidate's profile across all provider analyses, they may be a better fit for:

"""
        for role in sorted(all_roles):
            md_content += f"- {role}\n"
        md_content += "\n"

    # Add Interview Focus Areas section
    if all_interview_areas:
        md_content += """---

## Interview Focus Areas

If moving forward, probe these areas in depth:

"""
        for area in sorted(all_interview_areas):
            md_content += f"- {area}\n"
        md_content += "\n"

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

---

"""

        # Add detailed pillar analysis
        for i, pillar_key in enumerate(pillar_keys):
            pillar_data = analysis.get('pillars', {}).get(pillar_key, {})
            pillar_score = pillar_data.get('score', 0)
            pillar_level = pillar_data.get('level', 'Unknown')
            pillar_evidence = pillar_data.get('evidence', 'No evidence provided')
            pillar_strengths = pillar_data.get('strengths', [])
            pillar_gaps = pillar_data.get('gaps', [])

            md_content += f"""
#### {pillar_names[i]}

**Score**: {pillar_score}/10 | **Level**: {pillar_level}

**Evidence:**
{pillar_evidence}

"""
            if pillar_strengths:
                md_content += "**Strengths:**\n"
                for strength in pillar_strengths:
                    md_content += f"- ✅ {strength}\n"
                md_content += "\n"

            if pillar_gaps:
                md_content += "**Gaps/Concerns:**\n"
                for gap in pillar_gaps:
                    md_content += f"- ⚠️ {gap}\n"
                md_content += "\n"

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

**Framework**: 6 Pillars with 2025 standards - Technical Skills & Hands-On Building, Product Thinking & 0-to-1 Leadership, Deep AI Intuition (non-negotiable), Communication & Storytelling, Strategic Thinking & Second-Order Vision, Full-Spectrum Execution & Rapid Shipping

**Key Criteria**: Minimum thresholds, The Three Critical Questions, Must-have signals, Differentiation signals, Red/yellow flags

**Providers Used**: {', '.join([a.get('_metadata', {}).get('model_display_name', p.upper()) for p, a in analyses.items()])}

**Learn more**: https://github.com/abe238/aipm-resume-analyzer

---

*Deep analysis generated on {date_formatted}*
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(md_content)


def generate_aggregated_html(analyses, output_path):
    """Generate aggregated HTML report from multiple provider analyses"""

    # Get candidate name from first analysis
    candidate = list(analyses.values())[0].get('candidate_name', 'Candidate')
    now = datetime.now()
    date_formatted = now.strftime('%B %d, %Y at %H:%M:%S')

    # Calculate consensus scores (reuse logic from markdown)
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

    # Calculate consensus decision (most common decision)
    decisions = [a.get('decision', 'No Screen') for a in analyses.values()]
    consensus_decision = max(set(decisions), key=decisions.count)
    decision_class = consensus_decision.lower().replace(' ', '-')

    # Aggregate executive summaries from all providers
    executive_summaries = []
    for provider, analysis in analyses.items():
        model_name = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        recommendation = analysis.get('recommendation', '')
        if recommendation:
            executive_summaries.append(f"<p><strong>{model_name}:</strong> {recommendation}</p>")

    executive_summary_html = '\n'.join(executive_summaries) if executive_summaries else '<p>No recommendations available.</p>'

    # Aggregate 2025 framework evaluation data
    all_min_thresholds = []
    all_red_flags = []
    all_must_have_missing = []
    all_diff_signals_count = []

    for analysis in analyses.values():
        min_thresh = analysis.get('minimum_thresholds', {})
        all_min_thresholds.append(min_thresh.get('all_met', False))

        all_red_flags.extend(analysis.get('red_flags', []))

        must_have = analysis.get('must_have_signals', {})
        all_must_have_missing.extend(must_have.get('signals_missing', []))

        diff_sig = analysis.get('differentiation_signals', {})
        all_diff_signals_count.append(diff_sig.get('count', 0))

    # Consensus framework evaluation
    consensus_min_thresholds_met = any(all_min_thresholds)  # At least one passed
    unique_red_flags = list(set(all_red_flags))  # Unique red flags
    consensus_red_flags_count = len(unique_red_flags)
    unique_must_have_missing = list(set(all_must_have_missing))  # Unique missing signals
    consensus_must_have_missing = len(unique_must_have_missing)
    consensus_diff_signals = round(sum(all_diff_signals_count) / len(all_diff_signals_count)) if all_diff_signals_count else 0

    # Aggregate detailed framework data
    all_personal_ai = []
    all_building_public = []
    all_resume_creativity = []
    all_yellow_flags = []
    all_critical_questions = {'paradigm_shift': [], 'future_proofing': [], 'magic_wand': []}
    all_must_have_found = []
    all_diff_signals_found = []
    all_top_strengths = []
    all_top_concerns = []

    for analysis in analyses.values():
        min_thresh = analysis.get('minimum_thresholds', {})
        all_personal_ai.append(min_thresh.get('personal_ai_projects', False))
        all_building_public.append(min_thresh.get('building_in_public', False))
        all_resume_creativity.append(min_thresh.get('resume_creativity', False))

        all_yellow_flags.extend(analysis.get('yellow_flags', []))

        crit_q = analysis.get('critical_questions', {})
        all_critical_questions['paradigm_shift'].extend(crit_q.get('paradigm_shift_examples', []))
        all_critical_questions['future_proofing'].extend(crit_q.get('future_proofing_examples', []))
        all_critical_questions['magic_wand'].extend(crit_q.get('magic_wand_examples', []))

        must_have = analysis.get('must_have_signals', {})
        all_must_have_found.extend(must_have.get('signals_found', []))

        diff_sig = analysis.get('differentiation_signals', {})
        all_diff_signals_found.extend(diff_sig.get('signals', []))

        all_top_strengths.extend(analysis.get('top_strengths', [])[:3])
        all_top_concerns.extend(analysis.get('top_concerns', [])[:3])

    # Deduplicate
    unique_yellow_flags = list(set(all_yellow_flags))
    unique_must_have_found = list(set(all_must_have_found))
    unique_diff_signals_found = list(set(all_diff_signals_found))

    # Consensus on minimum thresholds
    consensus_personal_ai = any(all_personal_ai)
    consensus_building_public = any(all_building_public)
    consensus_resume_creativity = any(all_resume_creativity)

    # Get all strengths and concerns with provider labels
    all_strengths = []
    all_concerns = []
    for provider, analysis in analyses.items():
        provider_display = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        for strength in analysis.get('top_strengths', []):
            all_strengths.append(f"<strong>[{provider_display}]</strong> {strength}")
        for concern in analysis.get('top_concerns', []):
            all_concerns.append(f"<strong>[{provider_display}]</strong> {concern}")

    # Group by theme for readability
    grouped_strengths = group_feedback_by_theme(all_strengths)
    grouped_concerns = group_feedback_by_theme(all_concerns)

    # Build provider summary
    provider_summary = ""
    for provider, analysis in analyses.items():
        model_name = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        score = analysis.get('total_score', 0)
        decision = analysis.get('decision', 'Unknown')
        provider_summary += f"<li><strong>{model_name}</strong>: {score}/60 - {decision}</li>\n"

    # Build consensus table
    consensus_table_headers = ' | '.join([a.get('_metadata', {}).get('model_display_name', p) for p, a in analyses.items()])
    consensus_table_rows = ""
    for pillar_name in pillar_names:
        scores_data = consensus_scores[pillar_name]
        provider_scores = ' | '.join([str(scores_data['scores'].get(p, 0)) for p in analyses.keys()])
        consensus_table_rows += f"""
        <tr>
            <td><strong>{pillar_name}</strong></td>
            <td>{scores_data['avg']}/10</td>
            <td>{scores_data['min']}</td>
            <td>{scores_data['max']}</td>
            <td>{provider_scores.replace(' | ', '</td><td>')}</td>
        </tr>
"""

    # Build grouped strengths HTML
    strengths_html = ""
    for theme, items in grouped_strengths:
        strengths_html += f"<h3>{theme}</h3>\n"
        paragraph = format_grouped_items_as_paragraph(items)
        strengths_html += f"<p class='grouped-paragraph'>{paragraph}</p>\n"

    # Build grouped concerns HTML
    concerns_html = ""
    for theme, items in grouped_concerns:
        concerns_html += f"<h3>{theme}</h3>\n"
        paragraph = format_grouped_items_as_paragraph(items)
        concerns_html += f"<p class='grouped-paragraph'>{paragraph}</p>\n"

    # Aggregate suitable roles and interview focus areas for HTML
    all_roles_html = set()
    all_interview_areas_html = set()
    for provider, analysis in analyses.items():
        roles = analysis.get('suitable_roles', [])
        if roles:
            all_roles_html.update(roles)
        areas = analysis.get('interview_focus_areas', [])
        if areas:
            all_interview_areas_html.update(areas)

    # Build Better Fit Roles HTML
    roles_html = ""
    if all_roles_html:
        roles_html = "<h2>Better Fit Roles</h2>\n"
        roles_html += "<p>Based on this candidate's profile across all provider analyses, they may be a better fit for:</p>\n"
        roles_html += "<div class='roles-list'>\n"
        for role in sorted(all_roles_html):
            roles_html += f"<div class='role-item'>{role}</div>\n"
        roles_html += "</div>\n"

    # Build Interview Focus Areas HTML
    interview_html = ""
    if all_interview_areas_html:
        interview_html = "<h2>Interview Focus Areas</h2>\n"
        interview_html += "<p>If moving forward, probe these areas in depth:</p>\n"
        interview_html += "<ul class='sub-list'>\n"
        for area in sorted(all_interview_areas_html):
            interview_html += f"<li>{area}</li>\n"
        interview_html += "</ul>\n"

    # Build individual provider sections
    provider_details = ""
    for provider, analysis in analyses.items():
        model_name = analysis.get('_metadata', {}).get('model_display_name', provider.upper())
        score = analysis.get('total_score', 0)
        decision = analysis.get('decision', 'Unknown')
        recommendation = analysis.get('recommendation', '').replace('\n', '<br>')

        pillar_breakdown = ""
        for i, pillar_key in enumerate(pillar_keys):
            pillar_data = analysis.get('pillars', {}).get(pillar_key, {})
            pillar_score = pillar_data.get('score', 0)
            pillar_level = pillar_data.get('level', 'Unknown')
            pillar_evidence = pillar_data.get('evidence', 'No evidence provided').replace('\n', '<br>')
            pillar_strengths = pillar_data.get('strengths', [])
            pillar_gaps = pillar_data.get('gaps', [])

            pillar_breakdown += f"""
            <div class="pillar-detail">
                <h5>{pillar_names[i]}</h5>
                <p><strong>Score:</strong> {pillar_score}/10 | <strong>Level:</strong> {pillar_level}</p>
                <p><strong>Evidence:</strong><br>{pillar_evidence}</p>
"""
            if pillar_strengths:
                pillar_breakdown += "<p><strong>Strengths:</strong></p><ul>\n"
                for strength in pillar_strengths:
                    pillar_breakdown += f"<li>✅ {strength}</li>\n"
                pillar_breakdown += "</ul>\n"

            if pillar_gaps:
                pillar_breakdown += "<p><strong>Gaps/Concerns:</strong></p><ul>\n"
                for gap in pillar_gaps:
                    pillar_breakdown += f"<li>⚠️ {gap}</li>\n"
                pillar_breakdown += "</ul>\n"

            pillar_breakdown += "</div>\n"

        provider_details += f"""
        <div class="provider-section">
            <h3>{model_name}</h3>
            <p><strong>Score:</strong> {score}/60 | <strong>Decision:</strong> {decision}</p>
            <h4>Executive Summary:</h4>
            <p>{recommendation}</p>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #E7E5E4;">
            <h4>Detailed Pillar Analysis:</h4>
            {pillar_breakdown}
        </div>
"""

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep AI PM Analysis: {candidate}</title>
    <style>
        /*
         * ULTRA COMPACT VARIATION #23
         * Aggressive space reduction optimizations for time-constrained users
         * - Hero: 50vh (was 80vh) - saves 30% vertical space
         * - Section padding: 2rem (was 3rem) - 33% reduction
         * - Card padding: 1.5rem (was 2-2.5rem)
         * - Tighter line-heights and margins throughout
         * - Mobile: 60vh hero (was 100vh)
         */

        /* Modern Minimal Typography - Quattrocento (UNCHANGED) */
        @import url('https://fonts.googleapis.com/css2?family=Quattrocento:wght@400;700&display=swap');

        /* Anthropic Color Palette - Warm Tan/Orange Brand Colors */
        :root:not(.dark) {{
            /* Anthropic design system tokens */
            --accent-brand: 15 63.1% 59.6%;  /* Warm tan/orange */
            --accent-main-000: 15 55.6% 52.4%;
            --accent-main-100: 15 55.6% 52.4%;
            --accent-main-200: 15 63.1% 59.6%;
            --bg-000: 0 0% 100%;  /* Pure white */
            --bg-100: 48 33.3% 97.1%;  /* Warm off-white */
            --bg-200: 53 28.6% 94.5%;  /* Warm light gray */
            --bg-300: 48 25% 92.2%;
            --bg-400: 50 20.7% 88.6%;
            --bg-500: 50 20.7% 88.6%;
            --border-300: 30 3.3% 11.8%;
            --border-400: 30 3.3% 11.8%;
            --text-000: 60 2.6% 7.6%;  /* Near black */
            --text-100: 60 2.6% 7.6%;
            --text-200: 60 2.5% 23.3%;  /* Dark gray */
            --text-300: 60 2.5% 23.3%;
            --oncolor-100: 0 0% 100%;
            --primary: #c96442;  /* Warm tan/orange */
            --primary-foreground: #ffffff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Quattrocento', Georgia, serif;
            background: hsl(var(--bg-100));
            color: hsl(var(--text-100));
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
            max-width: 100vw;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1rem;
            color: hsl(var(--text-000));
        }}

        h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); }}
        h2 {{ font-size: clamp(1.75rem, 4vw, 2.5rem); }}
        h3 {{ font-size: clamp(1.5rem, 3vw, 2rem); }}
        h4 {{ font-size: clamp(1.25rem, 2.5vw, 1.5rem); }}

        p {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: 1rem;
            line-height: 1.65rem;
            margin-bottom: 1rem;
            color: hsl(var(--text-200));
        }}

        a {{
            color: var(--primary);
            text-decoration: none;
            transition: opacity 0.2s ease;
        }}

        a:hover {{
            opacity: 0.8;
        }}

        /* Container - wider gutters */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            width: 100%;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            font-size: 0.9375rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }}

        thead {{
            background: var(--primary);
            color: white;
        }}

        th {{
            padding: 1rem 1.25rem;
            text-align: left;
            font-weight: 600;
            color: white;
        }}

        td {{
            padding: 0.875rem 1.25rem;
            border-bottom: 1px solid hsl(var(--border-300));
            color: hsl(var(--text-200));
        }}

        tbody tr:hover {{
            background: hsl(var(--bg-200));
        }}

        /* Header with scroll shadow */
        header {{
            background: hsl(var(--bg-000) / 0.95);
            border-bottom: 0.5px solid hsl(var(--border-400) / 0.25);
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(10px);
            transition: box-shadow 0.3s ease;
        }}

        header.scrolled {{
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 4rem;
        }}

        .logo {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            font-size: 1.125rem;
            color: var(--primary);
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}

        .nav-links a {{
            color: hsl(var(--text-100));
            font-size: 0.9375rem;
            font-weight: 500;
            transition: color 0.2s ease;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid transparent;
        }}

        .nav-links a:hover,
        .nav-links a.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
            opacity: 1;
        }}

        @media (max-width: 768px) {{
            nav {{
                height: auto;
                padding: 0.75rem 0;
            }}

            .logo {{
                font-size: 1rem;
            }}

            .nav-links {{
                gap: 0.5rem;
                flex-wrap: wrap;
                justify-content: flex-end;
            }}

            .nav-links a {{
                font-size: 0.75rem;
                padding: 0.25rem 0.5rem;
            }}
        }}

        /* Buttons - Updated for deep blue primary */
        .btn {{
            position: relative;
            display: inline-flex;
            gap: 0.5rem;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            min-width: 5rem;
            height: 2.5rem;
            padding: 0.625rem 1.5rem;
            white-space: nowrap;
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            border-radius: 0.5rem;
            font-size: 1rem;
            text-decoration: none;
            transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn:active {{
            transform: scale(0.985);
        }}

        .btn-primary {{
            color: #ffffff;
            background-color: var(--primary);
            border: none;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}

        .btn-primary:hover {{
            background-color: #b5573a;
            opacity: 1;
        }}

        .btn-secondary {{
            color: var(--primary);
            background-color: transparent;
            border: 1px solid var(--primary);
        }}

        .btn-secondary:hover {{
            background-color: rgba(201, 100, 66, 0.1);
            opacity: 1;
        }}

        .cta-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}

        /* Hero Section - ULTRA COMPACT: 50vh Height */
        .hero {{
            position: relative;
            min-height: 50vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #fff;
            padding: 1rem 0;
        }}

        .hero-bg {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, rgba(30,10,5,0.85), rgba(60,30,20,0.9)),
                        radial-gradient(ellipse at top, rgba(201,100,66,0.3), transparent 50%);
            z-index: -1;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
        }}

        .hero h1 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-weight: 700;
            font-size: clamp(2.5rem, 5vw, 3.5rem);
            margin-bottom: 0.5rem;
            color: #ffffff;
            line-height: 1.1;
        }}

        .hero p {{
            font-size: 1.1rem;
            max-width: 650px;
            margin: 0 auto 1rem;
            color: rgba(255,255,255,0.85);
            line-height: 1.4;
        }}

        /* Scroll down indicator */
        .scroll-down {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(255,255,255,0.7);
            font-size: 2rem;
            animation: bounce 2s infinite;
            cursor: pointer;
        }}

        @keyframes bounce {{
            0%, 100% {{ transform: translate(-50%, 0); }}
            50% {{ transform: translate(-50%, 10px); }}
        }}

        /* Sections - ULTRA COMPACT */
        section {{
            padding: 2rem 0;
        }}

        .section-header {{
            text-align: center;
            margin-bottom: 1.5rem;
        }}

        .section-header h2 {{
            margin-bottom: 0.5rem;
        }}

        .section-header p {{
            font-size: 1.125rem;
            color: hsl(var(--text-300));
        }}

        /* Cards - ULTRA COMPACT */
        .card {{
            background: hsl(var(--bg-000));
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        .card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }}

        .card h3 {{
            margin-bottom: 0.75rem;
            font-size: 1.35rem;
            color: var(--primary);
        }}

        /* Reduce font-size for philosophy section to prevent wrapping */
        #philosophy .card h3 {{
            font-size: 1.15rem;
        }}

        .card p {{
            color: hsl(var(--text-300));
            margin-bottom: 0.5rem;
        }}

        /* Grid Layouts - Wider gutters */
        .grid {{
            display: grid;
            gap: 2.5rem;
        }}

        .grid-2 {{
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        }}

        .grid-3 {{
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        }}

        /* Pillar Cards - ULTRA COMPACT */
        .pillar-card {{
            background: linear-gradient(135deg, hsl(var(--bg-000)) 0%, hsl(var(--bg-100)) 100%);
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        .pillar-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }}

        .pillar-number {{
            display: inline-block;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--primary);
            margin-right: 0.5rem;
        }}

        .pillar-card h3 {{
            display: inline;
            color: var(--primary);
            margin-bottom: 0;
            font-size: 1.5rem;
        }}

        .pillar-card p {{
            display: block;
            margin-top: 0.75rem;
        }}

        .pillar-card ul {{
            list-style: none;
            margin-top: 1rem;
        }}

        .pillar-card li {{
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: hsl(var(--text-200));
        }}

        .pillar-card li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
        }}

        /* Decision Framework */
        .decision-flow {{
            background: hsl(var(--bg-200));
            border-radius: 12px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        .decision-step {{
            padding: 1.5rem;
            margin: 1.25rem 0;
            background: hsl(var(--bg-000));
            border-left: 4px solid var(--primary);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}

        .decision-step h4 {{
            color: var(--primary);
            margin-bottom: 0.75rem;
        }}

        .decision-step ol,
        .decision-step ul {{
            margin-left: 2rem;
            margin-top: 0.75rem;
        }}

        .decision-step li {{
            margin: 0.5rem 0;
            color: hsl(var(--text-200));
        }}

        .highlight-box {{
            background: hsl(var(--bg-100));
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin-top: 0.75rem;
            font-weight: 500;
            border-left: 3px solid var(--primary);
        }}

        /* Personal Story - ULTRA COMPACT */
        .story-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem 1.5rem;
            align-items: center;
            background: hsl(var(--bg-000));
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        }}

        .story-section h2 {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: clamp(2rem, 4vw, 3rem);
            margin-bottom: 1rem;
            color: var(--primary);
        }}

        .story-section p {{
            font-family: 'Quattrocento', Georgia, serif;
            font-size: 1.125rem;
            line-height: 1.8;
            color: hsl(var(--text-200));
            margin-bottom: 1.5rem;
        }}

        .story-visual {{
            text-align: center;
        }}

        .story-visual img {{
            width: 100%;
            max-width: 400px;
            border-radius: 12px;
            object-fit: cover;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }}

        .caption {{
            text-align: center;
            font-size: 0.875rem;
            color: hsl(var(--text-300));
            margin-top: 0.75rem;
        }}

        .btn-link {{
            display: inline-block;
            margin-top: 1rem;
            font-weight: 600;
            color: var(--primary);
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .btn-link:hover {{
            text-decoration: underline;
        }}

        blockquote.highlight {{
            border-left: 4px solid var(--primary);
            padding-left: 1.5rem;
            font-style: italic;
            color: hsl(var(--text-300));
            margin: 1.5rem 0;
            font-size: 1.125rem;
        }}

        /* Video Container */
        .video-container {{
            position: relative;
            width: 100%;
            margin: 2rem 0;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}

        /* Scoring Stats Cards */
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}

        .stat-card {{
            background: linear-gradient(135deg, hsl(var(--bg-000)) 0%, hsl(var(--bg-100)) 100%);
            border: none;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
            line-height: 1;
        }}

        .stat-label {{
            font-size: 1rem;
            font-weight: 600;
            color: hsl(var(--text-200));
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Footer - Consolidated CTAs */
        footer {{
            background: hsl(var(--bg-200));
            border-top: 0.5px solid hsl(var(--border-400));
            padding: 3rem 0 2rem;
            margin-top: 4rem;
        }}

        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2.5rem;
            margin-bottom: 2rem;
        }}

        .footer-section h4 {{
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
            color: var(--primary);
        }}

        .footer-section ul {{
            list-style: none;
        }}

        .footer-section li {{
            margin-bottom: 0.5rem;
        }}

        .footer-section a {{
            color: hsl(var(--text-200));
            font-size: 0.9375rem;
        }}

        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: none;
            color: hsl(var(--text-300));
            font-size: 0.875rem;
        }}

        /* Responsive - ULTRA COMPACT */
        @media (max-width: 768px) {{
            .container {{
                padding: 0 1rem;
            }}

            section {{
                padding: 1.5rem 0;
            }}

            .grid {{
                gap: 1.25rem;
            }}

            .hero {{
                min-height: 60vh;
                padding: 1rem 0;
            }}

            .hero h1 {{
                font-size: clamp(1.75rem, 7vw, 2.25rem);
                margin-bottom: 0.5rem;
            }}

            .hero p {{
                font-size: 1rem;
                margin-bottom: 1rem;
            }}

            .cta-buttons {{
                flex-direction: column;
                gap: 0.5rem;
                margin-top: 1rem;
            }}

            .btn {{
                width: 100%;
                max-width: 320px;
            }}

            .story-section {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
                padding: 1.5rem 1rem;
            }}

            .story-visual {{
                order: -1;
            }}

            .video-container {{
                margin: 1.5rem 0;
            }}

            table {{
                font-size: 0.8125rem;
                display: block;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }}

            th, td {{
                padding: 0.5rem 0.75rem;
                white-space: nowrap;
            }}

            .stats {{
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }}

            .stat-card {{
                padding: 1.5rem 1rem;
            }}

            .stat-number {{
                font-size: 2rem;
            }}

            .stat-label {{
                font-size: 0.875rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔬 Deep AI PM Resume Analysis: {candidate}</h1>
            <div class="meta">Analysis Date: {date_formatted}</div>
            <div class="score-badge">
                Total Score: {avg_total}/60 (0/100 weighted)
            </div>
            <div class="decision-badge {decision_class}">
                Decision: {consensus_decision}
            </div>
        </div>

        <!-- Executive Summary -->
        <h2>Executive Summary</h2>
        <div class="summary-box">
            {executive_summary_html}
            <p style="margin-top: 12px;"><strong>Decision Rationale:</strong> Consensus across {len(analyses)} provider(s): {consensus_decision} with average score of {avg_total}/60.</p>
        </div>

        <!-- 2025 Framework Evaluation -->
        <h2>2025 Framework Evaluation</h2>
        <table>
            <thead>
                <tr>
                    <th>Criteria</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Minimum Thresholds</strong></td>
                    <td>{"✅ Some Met" if consensus_min_thresholds_met else "❌ Failed"}</td>
                </tr>
                <tr>
                    <td><strong>Red Flags</strong></td>
                    <td>{"❌ " + str(consensus_red_flags_count) + " Found" if consensus_red_flags_count > 0 else "✅ None"}</td>
                </tr>
                <tr>
                    <td><strong>Must-Have Signals</strong></td>
                    <td>{"✅ All Present" if consensus_must_have_missing == 0 else "⚠️ " + str(consensus_must_have_missing) + " Missing"}</td>
                </tr>
                <tr>
                    <td><strong>Differentiation Signals</strong></td>
                    <td>{consensus_diff_signals}/8 ({"✅ Sufficient" if consensus_diff_signals >= 4 else "⚠️ Needs More"})</td>
                </tr>
            </tbody>
        </table>

        <!-- Minimum Thresholds Detail -->
        <h2>Minimum Thresholds</h2>
        <ul class="sub-list">
            <li>{"✅" if consensus_personal_ai else "❌"} Personal AI Projects</li>
            <li>{"✅" if consensus_building_public else "❌"} Building in Public</li>
            <li>{"✅" if consensus_resume_creativity else "❌"} Resume Creativity</li>
        </ul>

        <!-- Red Flags -->
        {f'''<h2>🚩 Red Flags (Critical Issues)</h2>
        <ul class="sub-list">
            {''.join([f"<li>{flag}</li>" for flag in unique_red_flags])}
        </ul>''' if unique_red_flags else ''}

        <!-- Yellow Flags -->
        {f'''<h2>⚠️ Yellow Flags (Investigate Further)</h2>
        <ul class="sub-list">
            {''.join([f"<li>{flag}</li>" for flag in unique_yellow_flags])}
        </ul>''' if unique_yellow_flags else ''}

        <!-- Three Critical Questions -->
        {f'''<h2>The Three Critical Questions Analysis</h2>

        <h3>1. Paradigm Shift (Car vs. Faster Horse)</h3>
        <ul class="sub-list">
            {''.join([f"<li>{ex}</li>" for ex in all_critical_questions['paradigm_shift']]) if all_critical_questions['paradigm_shift'] else '<li>No examples found across providers</li>'}
        </ul>

        <h3>2. Future-Proofing (Gets Better with AI Advances)</h3>
        <ul class="sub-list">
            {''.join([f"<li>{ex}</li>" for ex in all_critical_questions['future_proofing']]) if all_critical_questions['future_proofing'] else '<li>No examples found across providers</li>'}
        </ul>

        <h3>3. Magic Wand Test (Designed for Full Automation)</h3>
        <ul class="sub-list">
            {''.join([f"<li>{ex}</li>" for ex in all_critical_questions['magic_wand']]) if all_critical_questions['magic_wand'] else '<li>No examples found across providers</li>'}
        </ul>''' if any([all_critical_questions['paradigm_shift'], all_critical_questions['future_proofing'], all_critical_questions['magic_wand']]) else ''}

        <!-- Must-Have Signals -->
        <h2>Must-Have Signals</h2>
        {f'''<h3>Signals Found ({len(unique_must_have_found)}/5):</h3>
        <ul class="sub-list">
            {''.join([f"<li>{signal}</li>" for signal in unique_must_have_found])}
        </ul>''' if unique_must_have_found else ''}
        {f'''<h3>Signals Missing ({len(unique_must_have_missing)}/5):</h3>
        <ul class="sub-list">
            {''.join([f"<li>{signal}</li>" for signal in unique_must_have_missing])}
        </ul>''' if unique_must_have_missing else ''}

        <!-- Differentiation Signals -->
        <h2>Differentiation Signals</h2>
        <p><strong>Count:</strong> {len(unique_diff_signals_found)}/8 (Need 3+ for Strong Screen)</p>
        {f'''<h3>Signals Found:</h3>
        <ul class="sub-list">
            {''.join([f"<li>{signal}</li>" for signal in unique_diff_signals_found])}
        </ul>''' if unique_diff_signals_found else '<p>No differentiation signals found across any provider.</p>'}

        <div class="overview">
            <h2>🔬 Deep Analysis Overview</h2>
            <p>This is an <strong>aggregated deep analysis</strong> using multiple AI providers to provide maximum feedback and diverse perspectives on the candidate's profile.</p>

            <h3>Providers Analyzed:</h3>
            <ul>
                {provider_summary}
            </ul>
            <p><strong>Consensus Total Score:</strong> {avg_total}/60</p>
        </div>

        <h2>📊 Consensus Pillar Scores</h2>
        <table>
            <thead>
                <tr>
                    <th>Pillar</th>
                    <th>Average</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>{consensus_table_headers.replace(' | ', '</th><th>')}</th>
                </tr>
            </thead>
            <tbody>
                {consensus_table_rows}
            </tbody>
        </table>

        <h2>✨ All Identified Strengths</h2>
        {strengths_html}

        <h2>⚠️ All Identified Concerns</h2>
        {concerns_html}

        {roles_html}

        {interview_html}

        <h2>📋 Detailed Analysis by Provider</h2>
        {provider_details}

        <h2>💡 How to Use This Deep Analysis</h2>
        <p>This report aggregates insights from multiple AI models to provide:</p>
        <ul>
            <li><strong>Consensus view:</strong> Where all models agree, there's high confidence</li>
            <li><strong>Diverse perspectives:</strong> Different models may emphasize different strengths/concerns</li>
            <li><strong>Comprehensive feedback:</strong> More detailed than single-provider analysis</li>
        </ul>

        <h3>Action Items:</h3>
        <ol>
            <li>Review consensus scores for overall assessment</li>
            <li>Note where models disagree - these areas may need human judgment</li>
            <li>Read all identified strengths and concerns for complete picture</li>
            <li>Review individual provider analyses for detailed reasoning</li>
        </ol>

        <div class="footer">
            <h3>About This Analysis</h3>
            <p><strong>Aggregated Deep Analysis</strong> using the Applied AI PM Evaluation Framework</p>
            <p>A rigorous, open-source evaluation system for 2025 AI Product Manager candidates</p>
            <p><strong>Framework:</strong> 6 Pillars with 2025 standards - Technical Skills & Hands-On Building, Product Thinking & 0-to-1 Leadership, Deep AI Intuition (non-negotiable), Communication & Storytelling, Strategic Thinking & Second-Order Vision, Full-Spectrum Execution & Rapid Shipping</p>
            <p><strong>Providers Used:</strong> {', '.join([a.get('_metadata', {}).get('model_display_name', p.upper()) for p, a in analyses.items()])}</p>
            <p><a href="https://github.com/abe238/aipm-resume-analyzer" target="_blank">Learn more about the framework</a></p>
            <p style="margin-top: 16px;">Analysis generated on {date_formatted}</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)
