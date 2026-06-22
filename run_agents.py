import asyncio
import aiohttp
import os
import sys

# 1. Load keys safely (handles comma-separated and newline-separated keys, ignoring comments)
if not os.path.exists("keys.txt"):
    print("Error: keys.txt file not found.")
    sys.exit(1)

with open("keys.txt", "r", encoding="utf-8") as f:
    raw_content = f.read()

RAW_KEYS = []
for part in raw_content.split(','):
    for line in part.split('\n'):
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("#"):
            RAW_KEYS.append(cleaned)

if not RAW_KEYS:
    print("Error: No valid API keys found in keys.txt. Please add at least one API key.")
    sys.exit(1)

BASE_URL = "https://api.tokenrouter.com/v1"  # Replace with your actual Token Router endpoint if different
MODEL_NAME = "MiniMax-M3"

async def validate_single_key(session, key, idx):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    try:
        async with session.get(f"{BASE_URL}/models", headers=headers, timeout=15) as resp:
            if resp.status == 200:
                return key, True, None
            else:
                err_text = await resp.text()
                return key, False, f"HTTP {resp.status}: {err_text[:120]}"
    except Exception as e:
        return key, False, str(e)

async def filter_active_keys(keys):
    print(f"🔍 Checking {len(keys)} API keys from keys.txt concurrently...")
    connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [validate_single_key(session, key, idx) for idx, key in enumerate(keys)]
        results = await asyncio.gather(*tasks)
        
        valid_keys = []
        for idx, (key, is_valid, err) in enumerate(results):
            if is_valid:
                valid_keys.append(key)
            else:
                masked_key = f"{key[:8]}...{key[-6:]}" if len(key) > 14 else "invalid_key"
                print(f"⚠️ Key #{idx+1} ({masked_key}) is inactive or exhausted: {err}")
        
        print(f"✅ Key validation complete. Active keys: {len(valid_keys)}/{len(keys)}")
        return valid_keys

# ==========================================
# 🏢 THE FLAWLESS 100-AGENT PRODUCTION MATRIX
# ==========================================
AGENT_MATRIX = [
    # --- DEPARTMENT 1: STRATEGIC POSITIONING, MARKET TEARDOWNS, & FRICTION RISK (1-20) ---
    {"role": "Competitor Defeat Architect", "focus": "Search the live web for the top 5 direct competitors to this SaaS. Conduct a brutal matrix teardown of their feature gaps, pricing vulnerabilities, and customer complaints on Reddit/G2 to position us defensively."},
    {"role": "ICP Behavioral Analyst", "focus": "Map the psychographic profile of the primary buyer. Identify their silent objections, institutional buying friction, and exactly what internal metrics they must hit to justify buying this SaaS."},
    {"role": "Churn Mitigation Predictor", "focus": "Analyze the core_idea.md to isolate UX, onboarding, or technical friction points that will cause high user churn within the first 14 days. Draft the structural fixes."},
    {"role": "Pricing & Packaging Financial Model", "focus": "Design a 3-tier value-metric pricing framework (Free-Tier/Pro/Scale) maximizing expansion revenue, explicitly defining limits based on usage indicators instead of flat user seats."},
    {"role": "Value Proposition Refinement Critic", "focus": "Deconstruct the current messaging for ambiguity. Strip away generic SaaS phrases ('streamline workflows', 'empower teams') and replace them with sharp, undeniable quantified value metrics."},
    {"role": "Local Market Adaptation Specialist", "focus": "Evaluate geo-specific distribution friction (e.g., hyper-local ecosystems, regional billing preferences, market-specific user behaviors) to establish an initial dominant wedge."},
    {"role": "Enterprise Readiness Compliance Auditor", "focus": "List every technical compliance hurdle (SOC2, GDPR, data isolation, audit logs) this SaaS will encounter, and formulate the minimal viable security roadmap to close mid-market clients."},
    {"role": "Market Timing & Paradigm Strategist", "focus": "Examine macro market shifts, current developer tool trajectories, and industry tailwinds via web search to ensure the product positioning targets where the market is going, not where it is."},
    {"role": "Feature Bloat Counter-Strategist", "focus": "Audit the technical scope in core_idea.md. Identify the 20% core features that deliver 80% of consumer utility, and mandate a strict MVP reduction plan to speed up launch velocity."},
    {"role": "UX Onboarding Friction Specialist", "focus": "Design the step-by-step 'Time-to-Aha!' user journey map from the very first login screen to the moment the user experiences the core product value, minimizing input steps."},
    {"role": "B2B Land-and-Expand Tactician", "focus": "Build a deployment framework showing how a single team member can champion the tool, naturally creating collaborative loops that force viral peer adoption inside an organization."},
    {"role": "Product-Led Growth (PLG) Loop Engineer", "focus": "Architect an organic growth engine built inside the product mechanics (e.g., watermarks, shared workspace links, public asset sharing) so active usage inherently drives new user acquisition."},
    {"role": "Hook & Angle Ideation Engine", "focus": "Generate 15 distinct, high-impact marketing angles attacking diverse user pain points, classifying each by emotional hook (e.g., fear of losing data, pride of efficiency, cost reduction)."},
    {"role": "Category Creation Strategist", "focus": "Formulate a blueprint to position this SaaS not as an incremental alternative to existing systems, but as an entirely new operational layer or software category."},
    {"role": "Open-Source Community Conversion Advocate", "focus": "If building open-source, design the pipeline that smoothly transitions developer users from free self-hosted instances over to managed cloud tiers without fracturing community trust."},
    {"role": "Alternative Acquisition Wedge Analyst", "focus": "Identify 3 non-obvious entry-point utilities or micro-tools you can deploy for free to capture high-intent leads before upselling them to the main platform."},
    {"role": "Platform Dependency Risk Assessor", "focus": "Evaluate architectural structural risks related to third-party APIs or infrastructure backbones. Design operational isolation layers to safeguard reliability and system performance."},
    {"role": "Frictionless Checkout & Billing Engineer", "focus": "Map out a zero-drop-off upgrade flow, optimizing payment triggers, clear feature-gate modals, and annual discount incentives."},
    {"role": "Customer Success Automation Modeler", "focus": "Design an automated customer success framework utilizing trigger events to send hyper-personalized educational sequences when a user gets stuck on a specific feature."},
    {"role": "SaaS Post-Mortem Forensic Agent", "focus": "Simulate the structural collapse of this SaaS 12 months post-launch. Identify the exact failure modes (e.g., failed acquisition channels, mispriced COGS) so they can be fixed preemptively."},

    # --- DEPARTMENT 2: SEMANTIC CONTENT BLUEPRINTS & SEARCH INTENT ARCHITECTS (21-40) ---
    {"role": "Semantic Topical Authority Cartographer", "focus": "Search the web for top search vectors in this niche. Map a complete 30-node topical authority cluster grid with structural parent/child URL relationships to build immediate domain ranking."},
    {"role": "High-Intent Bottom-of-Funnel (BOFU) Keyword Engineer", "focus": "Isolate the highest-converting transactional keywords (e.g., 'alternative to...', 'best tool for X', 'how to automate Y'). Write detailed content outlines for each."},
    {"role": "Programmatic SEO Directory Architect", "focus": "Design the technical schema, data inputs, and URL routing for an automated programmatic SEO sub-directory that builds thousands of landing pages for long-tail integrations."},
    {"role": "Technical Blog Author (Advanced Engineering)", "focus": "Draft a deeply technical, comprehensive guide showcasing how to solve the target audience's core problem from first principles, writing real code snippets or detailed logic workflows."},
    {"role": "Skyscraper Competitive Content Destroyer", "focus": "Identify the top-ranking piece of content for our main target keyword via search. Outline a piece that is 10x deeper, structured better, and packed with superior assets."},
    {"role": "Developer Experience (DX) Documentation Writer", "focus": "Analyze core_idea.md and write the ultimate 'Quick Start Guide' documentation page that lets an engineering user get their first API request or deployment live within 2 minutes."},
    {"role": "AI Engine Optimization (AEO) Specialist", "focus": "Structure our public-facing text, schema definitions, and markdown matrices so LLM engines, search crawlers, and AI systems consistently cite this SaaS as the primary solution for the niche."},
    {"role": "Case Study Extraction Journalist", "focus": "Synthesize historical user issues or beta feedback to draft a compelling narrative case study documenting an anonymous team going from operational breakdown to 10x metrics using our system."},
    {"role": "Lead Magnet Asset Engineer", "focus": "Design the structure and raw content for an incredibly valuable free utility asset (e.g., a massive Notion workspace template, an open-source automation script) to secure high-intent emails."},
    {"role": "Newsletter Editorial Content Lead", "focus": "Draft a 3-part weekly educational sequence targeting founders and engineers, focusing on high-level strategy and technical insights while subtly integrating the SaaS value proposition."},
    {"role": "Comparison Page Copywriter (Us vs Them)", "focus": "Draft an objective, high-converting 'Alternative to [Major Competitor]' landing page copy framework that acknowledges competitor strengths but makes our core differentiation undeniable."},
    {"role": "Interactive Tool Ideator & Copy Lead", "focus": "Design the functional requirements and copy hooks for an online calculator or micro-UI tool (e.g., 'ROI Saver Calculator') that acts as a top-of-funnel viral customer magnet."},
    {"role": "Video Script Storyboard Engine (Technical/Product)", "focus": "Write a 90-second high-energy product launch video script using an engaging hook, smooth visual transitions, clear feature showcases, and an undeniable call-to-action."},
    {"role": "Ebook Blueprint Author", "focus": "Outline a complete, comprehensive ultimate industry field manual addressing the core structural challenges of our target market segment, ready for distribution."},
    {"role": "Glossary & Knowledge Base Scaler", "focus": "Construct a list of 25 industry terms specific to this product's niche, complete with clean definitions and internal cross-linking instructions to capture informational long-tail keywords."},
    {"role": "Social Proof Strategy Designer", "focus": "Formulate a systematic collection system that naturally prompts active users to leave reviews, submit video testimonials, or showcase their output metrics publicly."},
    {"role": "Micro-Blogging Content Matrix Builder", "focus": "Generate a library of short, highly specific educational tips addressing niche operational challenges, perfectly formatted for distribution channels."},
    {"role": "Repurposing Engine Orchestrator", "focus": "Create the structural rules to convert a single deep technical blog post into 5 LinkedIn snippets, a 10-post social media thread, and a script outline for video platforms."},
    {"role": "Interactive Checklist Developer", "focus": "Build a comprehensive markdown checklist guiding users through fixing their major industry bottlenecks, seamlessly positioning the SaaS as the ultimate tool to accelerate the process."},
    {"role": "Content Operations Guardrail Copywriter", "focus": "Establish a definitive brand voice style guide, setting rules for tone, formatting parameters, and forbidden phrasing to ensure complete consistency across all future agent generation runs."},

    # --- DEPARTMENT 3: HIGH-CONVERSION LANDING PAGE ELEMENTS & MICRO-COPY (41-60) ---
    {"role": "Above-The-Fold Conversion Optimizer", "focus": "Draft 10 distinct, highly optimized variations of the primary Hero Headline, Sub-headline, and CTA button text, focusing purely on clarity and immediate value confirmation."},
    {"role": "Feature-Benefit Matrix Copywriter", "focus": "Translate the technical architecture specs in core_idea.md into a clear visual matrix displaying specific backend features mapped directly to emotional consumer benefits."},
    {"role": "Micro-Interaction Engagement UX Writer", "focus": "Write the exact micro-copy for all secondary site touchpoints: input field placeholders, inline error messaging, success state notifications, and tooltips."},
    {"role": "Exit-Intent Pop-up Conversion Engineer", "focus": "Design an irresistible exit-intent overlay copy framework that converts bouncing site visitors into registered beta users or email list subscribers."},
    {"role": "Bento Grid Layout Asset Copywriter", "focus": "Structure a high-end, premium Bento-grid layout copy flow for the main homepage, focusing on fluid micro-interactions, distinct product feature blocks, and minimal text."},
    {"role": "Pricing Plan Card Conversion Catalyst", "focus": "Write the exact text for the pricing page cards, emphasizing plan subheads, highlighting the most popular package tier, and detailing localized currency checkouts."},
    {"role": "FAQ Objection-Crusher Builder", "focus": "Anticipate the 10 hardest, most skeptical questions a developer or buyer will ask about security, self-hosting, lock-in, and capabilities, and draft definitive answers."},
    {"role": "Interactive Demo Walkthrough Copywriter", "focus": "Write the step-by-step interactive guidance tooltip text that hand-holds a user through a simulated mockup sandbox of our product on the landing page."},
    {"role": "Beta Signup Waitlist Micro-Copy Lead", "focus": "Craft the copy for an elite, high-incentive waitlist landing page that leverages social referrals to help users climb the product access queue faster."},
    {"role": "Header/Footer Navigation & UX Flow Lead", "focus": "Structure the exact information architecture layout of the primary landing page header and footer navigation to optimize conversion pathing and minimize user drop-off."},
    {"role": "Social Proof Placement Matrix Designer", "focus": "Map out the strategic positioning of customer testimonials, logo bars, and rating badges across the page layout to maximize psychological safety at high-friction scroll depths."},
    {"role": "Value Proposition Graphic Concept Designer", "focus": "Detail the explicit visual concepts and exact textual descriptors for 5 infographics or layout illustrations that communicate our tech stack advantage instantly without text walls."},
    {"role": "Urgency & Scarcity Copy Catalyst", "focus": "Draft high-converting notification micro-copy leveraging real, non-fake platform scarcity (e.g., 'Infrastructure slots remaining for batch alpha run') to drive immediate onboarding actions."},
    {"role": "Enterprise Call-To-Action Deep Diver", "focus": "Draft the copy and discovery form layout for the 'Contact Enterprise Sales' path, optimizing fields to collect high-signal firmographic data while maintaining zero conversion friction."},
    {"role": "Customer Churn Reactivation Landing Page Writer", "focus": "Create the interface text for a specialized cancellation flow that gathers clean cancellation data while providing automated subscription options to save the account."},
    {"role": "Product Update Log & Changelog Writer", "focus": "Establish a clean, developer-centric public changelog post template based on the core features, framing every technical update as major progress."},
    {"role": "Mobile-Responsive UX Copy Auditor", "focus": "Audit the landing page layout concept specifically for mobile viewpoints, shortening headlines and ensuring immediate action visibility above mobile screen folds."},
    {"role": "Trust & Security Badge Integration Director", "focus": "Design the technical trust section copy, ensuring details regarding database encryption, secure authentication layers, and uptime guarantees are clearly communicated."},
    {"role": "Localization & Multi-Market Copy Specialist", "focus": "Adapt the standard landing page copy vectors to fit diverse international marketing tones, balancing direct technical phrasing with approachable business language."},
    {"role": "Typography Hierarchy & Visual Weight Architect", "focus": "Define the visual scannability rules for the landing page layout, establishing parameters for bold callouts, list formatting, and clear sectional splits."},

    # --- DEPARTMENT 4: HIGH-SIGNAL GROWTH & VIRAL DISTRIBUTION LOOPS (61-80) ---
    {"role": "Product Hunt Launch Playbook Director", "focus": "Design the complete launch asset timeline for a top Product Hunt release: draft the hunter comment, first maker comment, list of teaser features, and launch day update schedule."},
    {"role": "Hacker News Content Strategy Engineer", "focus": "Analyze what resonates on Hacker News via search. Craft 5 potential 'Show HN' angles and deeply technical title hooks that spark genuine discussion without sounding like spam."},
    {"role": "Subreddit Growth Distribution Hacker", "focus": "Identify 5 target subreddits where our core buyer hangs out. Design a highly tactical, non-promotional educational post framework that solves user issues while organically driving organic brand search."},
    {"role": "GitHub Open-Source Repository Optimizer", "focus": "Provide the complete layout, visual structure, badges, and code block formatting conventions for our GitHub README.md file to convert developers visiting the repo into active stars and contributors."},
    {"role": "Indie Hackers Launch Narrative Lead", "focus": "Draft an authentic, high-transparent founder journey launch write-up detailing the hard technical challenges and initial insights behind building this SaaS platform."},
    {"role": "Developer Discord/Slack Community Community Engine", "focus": "Build a comprehensive blueprint to scale an interactive community space, outlining engagement rituals, open technical channels, and ways to incentivize user support systems."},
    {"role": "X (Twitter) Long-Form Thread Architect", "focus": "Write 3 complete, highly scannable long-form social media threads that break down complex technical insights or business transformations, smoothly positioning our tool as the ultimate framework shortcut."},
    {"role": "LinkedIn Thought Leadership Engineer", "focus": "Draft 5 premium, high-impact text updates for professional networking platforms tailored to engineering executives and founders, addressing major industry changes."},
    {"role": "Co-Marketing Integration Campaign Partner", "focus": "Identify 5 non-competitive software platforms sharing our audience. Design exact integration partner pitch frameworks showing how combining utilities creates value."},
    {"role": "Affiliate & Partner Referral Growth Architect", "focus": "Design the complete mechanics, rewards dashboard parameters, and tracking infrastructure for an affiliate marketing network that incentives developers to recommend the app."},
    {"role": "Developer Relations (DevRel) Advocacy Plan", "focus": "Build a high-impact DevRel outreach plan mapping out technical content tutorials, community workshop formats, and direct developer support initiatives."},
    {"role": "Beta User Feedback Loop Orchestrator", "focus": "Design the automated email outreach systems and interface prompt frameworks used to gather high-quality bug reports and feature feature validation during the initial rollout phase."},
    {"role": "Public Launch Press & Media Pitch Lead", "focus": "Draft a personalized, high-context email outreach template targeting prominent technical journalists and independent newsletter publishers in our specific niche market."},
    {"role": "Micro-Influencer Technical Outreach Specialist", "focus": "Formulate a collaboration outreach script targeting developers and micro-influencers who run niche programming tutorials, offering clear sandbox workspace perks."},
    {"role": "Cold Audience Retargeting Campaign Architect", "focus": "Design the exact layout structure and ad copy blueprints for paid remarketing campaigns targeting visitors who dropped off our main onboarding flow."},
    {"role": "Community Q&A Authority Engine (Quora/StackOverflow)", "focus": "Identify high-volume technical discussion vectors online. Draft authoritative response architectures that position our product as the ultimate solution blueprint."},
    {"role": "Interactive Event/Webinar Launch Director", "focus": "Design the structural roadmap and full promotional timeline for a live developer workshop showcasing how to configure and deploy workflows using our platform."},
    {"role": "Viral Waitlist Gamification Engineer", "focus": "Formulate explicit engagement mechanics (e.g., automated unlock tiers, invite tracking) to transform our initial signup waitlist into a high-growth referral loop."},
    {"role": "Niche Online Platform Aggregator Submitter", "focus": "Map out a submission directory protocol targeting 20 software index directories, optimizing tagging structures to boost immediate search visibility and domain rank build-up."},
    {"role": "Founder 'Build in Public' Content Director", "focus": "Establish a weekly content publishing schedule for the core founders, detailing metrics to share, development obstacles to highlight, and how to build strong authentic audience relationships."},

    # --- DEPARTMENT 5: ACCOUNT-BASED OUTREACH & HIGH-SIGNAL COLD SDR ENGINES (81-100) ---
    {"role": "Cold Email Sequence Architect (3-Step)", "focus": "Write a highly personalized, completely non-spammy 3-stage cold email sequence targeting engineering directors, ensuring a strong focus on actual pain points and zero marketing fluff."},
    {"role": "LinkedIn Warm Social Outreach SDR", "focus": "Draft 5 personalized connection note styles and non-intrusive follow-up message flows that offer value based on recent industry updates before ever pitching our tool."},
    {"role": "Technical Director Sales Deck Presentation Architect", "focus": "Structure a high-converting 10-slide presentation deck layout tailored for technical management, detailing slides for system validation, ROI calculations, and deployment steps."},
    {"role": "Hyper-Personalized Video Outreach Scriptwriter", "focus": "Write a highly flexible 60-second personalized screen-share recording script for sales agents, showing how to highlight a prospect's public performance bottlenecks and present our tool as the fix."},
    {"role": "Enterprise Pilot Program Offer Architect", "focus": "Design a low-risk, high-incentive 'Enterprise Sandbox Pilot' onboarding proposal blueprint that eliminates corporate purchasing friction and accelerates initial trial rollouts."},
    {"role": "Inbound Lead Qualification Scoring Model", "focus": "Establish explicit operational qualification rules (e.g., team size, technological framework match) to automatically filter high-intent prospects for immediate sales outreach focus."},
    {"role": "Cold Calling Insight Trigger Framework", "focus": "Develop an actionable response playbook for sales reps, providing clear handling strategies for common initial calling hurdles like 'No time,' 'No budget,' or 'Happy with current tools.'"},
    {"role": "Account-Based Marketing (ABM) Playbook Director", "focus": "Construct a highly targeted marketing playbook designed to run integrated campaigns against 10 specific high-value dream enterprise accounts simultaneously across multiple channels."},
    {"role": "Free Structural Value Audit Outreach Lead", "focus": "Draft an out-of-the-box outbound email offer inviting prospects to receive a completely automated, free custom engineering architecture audit generated by our team."},
    {"role": "Re-engagement Sequence Engine (Lost Deals)", "focus": "Write a high-converting 2-part email re-engagement sequence targeting historical outbound leads who dropped out of the sales discovery process months prior."},
    {"role": "Niche Event Networking Playbook Director", "focus": "Design a tactical blueprint outlining how team members can connect with target accounts at industry meetups and tech conferences without resorting to pitch scripts."},
    {"role": "Customer Referral Incentive Program Designer", "focus": "Draft a personalized email sequence prompting active internal champions to introduce our platform to adjacent engineering teams in exchange for account upgrades."},
    {"role": "Executive Sponsor Pitch Framework", "focus": "Construct the exact business case documentation that an engineering lead can pass directly to their CFO or technical director to rapidly secure tool procurement budget approval."},
    {"role": "High-Signal Intent Trigger Tracker", "focus": "Define a monitoring framework detailing exactly how to act on real-time organizational shifts (e.g., job changes, new tech stacks) with high-context outbound outreach scripts."},
    {"role": "Technical Proposal Document Template Architect", "focus": "Provide the markdown structural layout for a formal product proposal, optimizing sections for system architecture diagrams, onboarding timelines, and terms."},
    {"role": "Post-Demo High-Velocity Follow-up Director", "focus": "Draft the exact follow-up message sequence sent immediately after a product demo, summarizing custom requirements and outlining clear deployment next steps."},
    {"role": "Cross-Functional Team Procurement Coordinator", "focus": "Create an automated sequence framework that brings both security leads and product directors into the sandbox evaluation space together to minimize checkout friction."},
    {"role": "Annual Contract Upsell Transition Architect", "focus": "Design the automated messaging pipeline that transitions monthly high-volume accounts over into structured annual contracts by offering dedicated account optimizations."},
    {"role": "Niche Vertical Industry Outreach Specialist", "focus": "Tailor our core value proposition copy to perfectly align with 3 highly distinct market verticals, ensuring all industry terminology sounds natural and native."},
    {"role": "Ultimate Sales Operation Playbook Director", "focus": "Write a definitive operational guide for new reps, detailing system setup parameters, voice guidelines, and strict frameworks to ensure all outbound messaging remains premium."}
]

# ==========================================
# ⚡ THE SYSTEM PARAMETERS ENGINE
# ==========================================
SYSTEM_GUARDRAIL = """
You are an elite, hyper-specialized AI agent operating inside a 100-agent decentralized marketing enterprise powered by MiniMax M3.
You have native access to a 1M context window and advanced agentic tools, including web search.

CRITICAL OPERATIONAL REQUIREMENT:
You must perform live web searches implicitly using your tools to gather up-to-date competitive data, real internet trends, current discussions on Reddit/Hacker News/G2, and the exact state of the marketing landscape as of 2026. Do not rely on assumptions. Look up the facts.

STRICT OUTPUT FORMAT MANDATE:
- Your output must be absolutely flawless, highly professional, completely clean, and free of generic AI introductions or conversational fluff. Start directly with the markdown headers.
- Do NOT output raw tool calls, function call blocks, or XML tags (such as `<function_calls>`, `<invoke>`, or `<error>`). If active web search tools are not available or fail in this session, proceed directly to generating the complete strategic analysis using your internal knowledge.

1. ## 📊 EXECUTIVE DIAGNOSIS
- Deliver a sharp, data-backed assessment of how the 'core_idea.md' interacts with current real-world market dynamics discovered via search.
- Note any direct competitive threats or industry shifts.

2. ## 🛠️ ELITE STRATEGY SPECIFICATION
- Provide a step-by-step, granular technical blueprint, deployment sequence, or ready-to-copy markdown marketing copy.
- It must be so detailed that a maker or coder could copy-paste it directly into production code, websites, or repositories.

3. ## ⚠️ CRITICAL CONTEXTUAL FLAW EXTRACTION
- Explicitly dismantle the core idea. Point out exactly where it lacks technical validation, where the positioning will fail, or where marketing budgets will be wasted. 
- Provide the structural correction.

Maintain an analytical, sharp, premium, and direct brand tone. Provide maximum depth.
"""

# Progress counters
started_agents = 0
completed_agents = 0
failed_agents = 0

async def run_agent(session, agent_id, key, matrix_item, core_context):
    global started_agents, completed_agents, failed_agents
    started_agents += 1
    
    # Initial jitter to spread concurrency and prevent rate limiting (0 to 15s)
    jitter = (agent_id % 10) * 1.5 + (agent_id % 3) * 0.5
    if jitter > 0:
        print(f"⏳ [Agent {agent_id:03d}/100] Applying initial jitter of {jitter:.1f}s to spread API requests...")
        await asyncio.sleep(jitter)
        
    print(f"🚀 [Agent {agent_id:03d}/100 | Started: {started_agents}/100] Initializing {matrix_item['role']}. Focus: {matrix_item['focus'][:85]}...")
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    user_prompt = f"""
    ### MASTER BLUEPRINT CONTEXT (core_idea.md):
    {core_context}
    
    ### YOUR ASSIGNED DECENTRALIZED ROLE:
    Agent ID: {agent_id}
    Role Name: {matrix_item['role']}
    Target Task Vector & Search Scope: {matrix_item['focus']}
    
    Execute your assigned task flawlessly based on the Master Blueprint and real-time internet validation.
    """
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_GUARDRAIL},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.25  # Low temperature forces hyper-analytical, precise reasoning patterns
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        print(f"📡 [Agent {agent_id:03d}/100 | Attempt {attempt}/{max_retries}] Sending request to Token Router API ({MODEL_NAME})...")
        start_time = asyncio.get_event_loop().time()
        
        try:
            async with session.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers, timeout=450) as resp:
                elapsed = asyncio.get_event_loop().time() - start_time
                if resp.status == 200:
                    result = await resp.json()
                    if not result:
                        raise ValueError("API returned empty JSON response")
                    
                    if "error" in result:
                        err_detail = result["error"]
                        err_msg = err_detail.get("message", str(err_detail))
                        raise ValueError(f"API returned HTTP 200 but with error: {err_msg}")
                        
                    choices = result.get('choices')
                    if not choices:
                        raise ValueError(f"API response missing 'choices' key. Response: {result}")
                    
                    first_choice = choices[0]
                    if not first_choice:
                        raise ValueError(f"API response 'choices' list is empty. Response: {result}")
                    
                    message = first_choice.get('message')
                    if not message:
                        raise ValueError(f"API response choice missing 'message' key. Choice: {first_choice}")
                    
                    content = message.get('content')
                    if content is None:
                        raise ValueError(f"API response message missing 'content' key. Message: {message}")
                    
                    completed_agents += 1
                    print(f"✅ [Agent {agent_id:03d}/100 | Success: {completed_agents}/100] Completed on Attempt {attempt} in {elapsed:.2f}s (length: {len(content)} chars).")
                    return f"# AGENT SYSTEM {agent_id}: {matrix_item['role'].upper()}\n\n**🎯 Task Focus:** {matrix_item['focus']}\n\n{content}\n\n---\n\n"
                
                # If non-200, log warning and check if we should retry
                err_text = await resp.text()
                print(f"⚠️ [Agent {agent_id:03d}/100 | Attempt {attempt}/{max_retries}] API Error (Status {resp.status}) in {elapsed:.2f}s. Response: {err_text[:200]}")
                
                if attempt < max_retries:
                    backoff = 3 * attempt
                    print(f"⏳ [Agent {agent_id:03d}/100] Waiting {backoff}s before retrying...")
                    await asyncio.sleep(backoff)
                else:
                    failed_agents += 1
                    print(f"❌ [Agent {agent_id:03d}/100 | Failure: {failed_agents}/100] Failed permanently after {max_retries} attempts.")
                    return f"# AGENT SYSTEM {agent_id}: {matrix_item['role'].upper()}\n\n❌ API Connection Refused (Status {resp.status} after {max_retries} attempts): {err_text}\n\n---\n\n"
        except Exception as e:
            elapsed = asyncio.get_event_loop().time() - start_time
            err_desc = f"{type(e).__name__}: {str(e)}" if str(e) else type(e).__name__
            print(f"⚠️ [Agent {agent_id:03d}/100 | Attempt {attempt}/{max_retries}] Exception in {elapsed:.2f}s: {err_desc}")
            
            if attempt < max_retries:
                backoff = 3 * attempt
                print(f"⏳ [Agent {agent_id:03d}/100] Waiting {backoff}s before retrying...")
                await asyncio.sleep(backoff)
            else:
                failed_agents += 1
                print(f"❌ [Agent {agent_id:03d}/100 | Failure: {failed_agents}/100] Failed permanently after {max_retries} exceptions.")
                return f"# AGENT SYSTEM {agent_id}: {matrix_item['role'].upper()}\n\n❌ Runtime Exception Triggered (after {max_retries} attempts): {err_desc}\n\n---\n\n"

async def main():
    # Filter active keys before starting
    API_KEYS = await filter_active_keys(RAW_KEYS)
    if not API_KEYS:
        print("Error: None of the API keys in keys.txt are valid or active. Please check your credentials.")
        sys.exit(1)
        
    if len(API_KEYS) < len(AGENT_MATRIX):
        print(f"Warning: Found {len(API_KEYS)} active keys for {len(AGENT_MATRIX)} agents. Keys will be cycled.")

    # Detect the correct core idea file
    core_idea_file = "core_idea.md"
    if os.path.exists("core_idea_agent.md"):
        core_idea_file = "core_idea_agent.md"
    
    if not os.path.exists(core_idea_file):
        print("Error: Neither core_idea.md nor core_idea_agent.md file was found.")
        sys.exit(1)

    print(f"Loading context from {core_idea_file}...")
    with open(core_idea_file, "r", encoding="utf-8") as f:
        core_context = f.read()

    # Dynamically append the GTM Master Playbook if it exists in the workspace
    gtm_playbook_file = "AgentGrid_GTM_Master.md"
    if os.path.exists(gtm_playbook_file):
        print(f"Loading additional playbook context from {gtm_playbook_file}...")
        with open(gtm_playbook_file, "r", encoding="utf-8") as f:
            playbook_content = f.read()
        core_context += "\n\n### MASTER GO-TO-MARKET PLAYBOOK (AgentGrid_GTM_Master.md):\n" + playbook_content

    print(f"Initializing decentralized swarm: Running {len(AGENT_MATRIX)} parallel agents across {len(API_KEYS)} keys...")
    
    # Custom high-concurrency connection pooling specifically for GitHub Actions environments
    connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i, task_item in enumerate(AGENT_MATRIX):
            # Rotates seamlessly across the valid keys pool
            key = API_KEYS[i % len(API_KEYS)]
            tasks.append(run_agent(session, i + 1, key, task_item, core_context))
        
        # Parallel async launch inside the GitHub Actions Cloud Runner
        results = await asyncio.gather(*tasks)
        
        with open("complete_marketing_blueprint.md", "w", encoding="utf-8") as f:
            f.write("# 🏢 THE 100-AGENT ENTERPRISE: DECENTRALIZED MASTER MARKETING REPORT\n\n")
            f.write("--- \n\n")
            f.writelines(results)
            
    print("✨ Execution successfully finished! The document is generated inside: complete_marketing_blueprint.md")

if __name__ == "__main__":
    asyncio.run(main())
