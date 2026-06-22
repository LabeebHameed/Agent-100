import asyncio
import aiohttp
import os
import sys

# 1. Load keys safely (handles comma-separated and newline-separated keys, ignoring comments)
if not os.path.exists("keys.txt"):
    print("Error: keys.txt file not found. Please create it first or run via GitHub Actions.")
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

BASE_URL = "https://api.tokenrouter.com/v1"
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

# ==============================================================
# 🪪 THE 100-AGENT AGENTGRID PASSPORT VERIFICATION DESIGN MATRIX
# ==============================================================
AGENT_MATRIX = [
    # --- DEPARTMENT 1: CRYPTOGRAPHIC IDENTITY & SIGNATURE STANDARDS (1-20) ---
    {"role": "RFC 9421 HTTP Message Signatures Architect", "focus": "Define HTTP request header signing schemas (Signature, Signature-Input) to prove request provenance to remote sites."},
    {"role": "W3C DID method:key & method:web Specifier", "focus": "Specify DID-to-public-key bindings, transition pathways, and decentralized resolution mechanics for remote verifiers."},
    {"role": "JCS (RFC 8785) Canonicalization Auditor", "focus": "Ensure tamper-proof JSON formatting prior to signature generation to prevent verification mismatch failures."},
    {"role": "Ed25519 Cryptographic Curve Evaluator", "focus": "Validate signature security parameters, key lengths, and performance margins for sub-millisecond edge verification."},
    {"role": "Secure Enclave Hardware Trust Designer", "focus": "Map hardware-backed private key storage (macOS Secure Enclave / Android Keystore) boundaries for operator keys."},
    {"role": "Cloud HSM Key Custody Engineer", "focus": "Design Google Cloud KMS / AWS KMS backend interfaces ensuring agent private keys are never exposed in plaintext."},
    {"role": "Verifiable Credentials Schema Architect", "focus": "Formulate the JSON-LD schemas for Passport credentials to represent agent status and operator authorization."},
    {"role": "Operator-Agent Delegation Chain Prover", "focus": "Architect cryptographic proof chains showing operator-to-agent delegation via nested verifiable presentations."},
    {"role": "Short-Lived Egress Token Designer", "focus": "Specify dynamic token minting and lifespan limits to reduce the attack surface of verified credentials."},
    {"role": "TLS-Level Client Certificate Engineer", "focus": "Explore using mTLS (Mutual TLS) with agent public keys to bypass WAF challenges at the transport layer."},
    {"role": "Key Rotation & Graceful Rollover Planner", "focus": "Design secure key rotation sequences that don't disrupt active sessions or invalidate historic audit logs."},
    {"role": "Signature Nonce & Anti-Replay Specialist", "focus": "Implement cryptographically secure nonce generation and timestamp validation to prevent message replay attacks."},
    {"role": "Decentralized Identifiers (DIDs) Registry Designer", "focus": "Architect the JSON schemas and resolver code for publishing agent public keys via `.well-known` endpoints."},
    {"role": "ZKP (Zero-Knowledge Proof) Privacy Designer", "focus": "Investigate selective disclosure of operator identity (e.g., proving operator is verified without revealing operator's real name)."},
    {"role": "OAuth 2.1 Sender-Constrained Token Architect", "focus": "Design token binding mechanisms (DPoP - OAuth 2.0 Demonstrating Proof-of-Possession) for agent API authentication."},
    {"role": "Multi-Signature Approval Validator", "focus": "Draft multi-sig verification protocols for highly sensitive/consequential agent actions."},
    {"role": "Hash-Chained State Transition Prover", "focus": "Formulate cryptographic checks proving passport state transitions (Active -> Suspended -> Revoked) are valid."},
    {"role": "Hardware Token (FIDO2/WebAuthn) Integrationist", "focus": "Integrate biometric keys (TouchID/FaceID) to sign operator approval statements for agent step-ups."},
    {"role": "Secure Handshake & Verification Protocol Analyst", "focus": "Map the complete sequence diagram of a site verifying an agent's Passport from first HTTP request to final ALLOW."},
    {"role": "Cryptographic Audit Ledger Verifier", "focus": "Build verification scripts that reconstruct the audit hash chain to check for tampering by compromised nodes."},

    # --- DEPARTMENT 2: REGISTRY ARCHITECTURE & HIGH-AVAILABILITY PERSISTENCE (21-40) ---
    {"role": "Postgres JSONB Registry Architect", "focus": "Design the passport and mandate database tables utilizing JSONB columns for flexible cryptographic payloads."},
    {"role": "Revocation Propagation Latency Optimizer", "focus": "Create real-time pub/sub mechanisms (PG NOTIFY / Redis) to push key revocation statuses to edge endpoints in milliseconds."},
    {"role": "Public Verification API Designer", "focus": "Specify standard REST/GraphQL API endpoints that remote websites call to query Passport metadata and status."},
    {"role": "File-Backed Registry Atomic Fallback Engineer", "focus": "Implement atomic write-rename-replace storage utilities for local-first developer setups to prevent corruption."},
    {"role": "High-Throughput Indexing Specialist", "focus": "Optimize database indexing over DID prefixes and status columns to ensure sub-millisecond query response times."},
    {"role": "Multi-Region Registry Synchronizer", "focus": "Design replication and conflict resolution protocols for multi-node registries operating globally."},
    {"role": "Registry Caching & CDN Distribution Planner", "focus": "Configure Cloudflare CDN caching headers (stale-while-revalidate) for public keys to maximize uptime."},
    {"role": "Verification Rate Limiting Coordinator", "focus": "Architect rate-limiting structures to protect the public verification API from Denial of Service (DoS) attacks."},
    {"role": "DID Document Resolution Resolver", "focus": "Write clean, spec-compliant DID resolvers mapping `did:key` and `did:web` to active cryptographic keys."},
    {"role": "Historical Key Registry Archivist", "focus": "Design storage schemas for rotated and expired keys to maintain long-term validation of historical audit ledgers."},
    {"role": "State Machine Engine Designer", "focus": "Specify the exact status transitions of a Passport (Active -> Suspended -> Revoked -> Reinstated) and their rules."},
    {"role": "Registry Health & E2E Uptime Monitor", "focus": "Implement synthetic verification tests to continuously monitor registry availability and latency."},
    {"role": "Cryptographically Secure Seed Generator", "focus": "Evaluate entropy sources on diverse platforms to ensure secure key generation for new Passports."},
    {"role": "Public Directory Discovery Planner", "focus": "Specify metadata schema standards (RFC 8615) to make agent registries discoverable via `.well-known/agents`."},
    {"role": "Tenant Partitioning Security Architect", "focus": "Design multi-tenant data isolation logic to prevent data leaks between different organization registries."},
    {"role": "Registry Backup & Disaster Recovery Specifier", "focus": "Formulate recovery procedures to rebuild the identity registry from cryptographically signed logs in case of catastrophic storage failure."},
    {"role": "Event-Driven Audit Pub-Sub Engineer", "focus": "Design log forwarding architectures (Kafka/EventBridge) to ship verification logs securely to external SIEM tools."},
    {"role": "API Versioning & Migration Coordinator", "focus": "Plan backwards-compatible changes to the Passport registry API as DID standards evolve."},
    {"role": "Open-Source Registry (tn8r-compatible) Blueprint Designer", "focus": "Specify self-hostable registry patterns that run in Docker/SQLite for local testing."},
    {"role": "Batch Verification Performance Engineer", "focus": "Optimize the API to support validating arrays of agent identities in a single batch request to reduce handshake roundtrips."},

    # --- DEPARTMENT 3: THREAT MODELING & RED-TEAM HARDENING (41-60) ---
    {"role": "Passport Signer Binding Vulnerability Auditor", "focus": "Hardcode verification logic ensuring remote sites cannot be tricked by tampered metadata keys (16.2.2 vulnerability)."},
    {"role": "Operator Root Trust Bypass Exploit Specialist", "focus": "Design checks preventing compromised agents from minting root mandates with self-generated operator keys."},
    {"role": "Replay & Nonce Interception Penetration Tester", "focus": "Simulate message interception and replay attacks to validate signature freshness windows."},
    {"role": "Prompt Injection Privilege Escalation Assessor", "focus": "Audit the LLM-to-Executor boundary to ensure prompt injections cannot trigger unauthorized signing calls."},
    {"role": "Memory Heap Key Exfiltration Red-Teamer", "focus": "Verify that private key bytes are never loaded into Node/V8 heaps where compromised agents could read them."},
    {"role": "Man-in-the-Middle Egress Traffic Analyzer", "focus": "Check outbound browser container network paths to ensure verified sessions cannot be hijacked by proxy networks."},
    {"role": "Denial of Service (DoS) Vulnerability Evaluator", "focus": "Simulate high-volume malicious handshake requests targeting the verification engine."},
    {"role": "Side-Channel Timing Attack Hardener", "focus": "Implement constant-time cryptographic comparisons for signatures and hashes to prevent timing leaks."},
    {"role": "Compromised Key Kill Switch Architect", "focus": "Design the 'nuclear' revocation trigger that instantly purges active sessions and invalidates virtual payment cards."},
    {"role": "Sandboxed Verification Runtime Isolation Engineer", "focus": "Specify gVisor/Firecracker VM boundaries for execution of untrusted scripts during bot auth handshakes."},
    {"role": "Confused Deputy Attack Threat Modeler", "focus": "Examine situations where an agent uses its passport to authenticate on a site but gets phished into performing actions for an attacker."},
    {"role": "Credential Injection Interception Auditor", "focus": "Assert that injected passwords and API keys do not leak into accessibility trees, transcripts, or console logs."},
    {"role": "Registry Database Sql Injection Pen-Tester", "focus": "Secure all raw SQL queries in the registry module using parameterization and strict type safety."},
    {"role": "Host Privilege Escape Hardener", "focus": "Verify that containerized Playwright browser instances cannot access host system calls or environment secrets."},
    {"role": "Audit Ledger Tampering Forensic Analyst", "focus": "Simulate a database breach where an attacker attempts to alter logs; verify that the hash-chain validation breaks."},
    {"role": "Continuous Anomaly Behavior Engine Designer", "focus": "Specify rules to detect anomalous API/verification spikes that suggest agent compromise."},
    {"role": "Stale Revocation Token Starvation Assessor", "focus": "Audit token Time-To-Live (TTL) durations to ensure revoked agents lose capability within minutes."},
    {"role": "Null-Values and Type Juggling Exploit Auditor", "focus": "Hardcode validation logic against Javascript type coercion exploits (e.g., null amounts passing limits)."},
    {"role": "Fake Identity Sybil Attack Prevention Specialist", "focus": "Design mechanisms preventing attackers from spinning up millions of free fake AgentGrid identities to spam sites."},
    {"role": "WAF Signature Spoofing Red-Teamer", "focus": "Verify that attackers cannot craft headers that bypass site WAFs by forging AgentGrid validation signatures."},

    # --- DEPARTMENT 4: GATEWAY INTERFACE & BOT NEGOTIATION (61-80) ---
    {"role": "Cloudflare Web Bot Auth Integration Lead", "focus": "Design standard integrations mapping AgentGrid signatures directly to Cloudflare's verified bot program."},
    {"role": "WAF Challenge Bypass Protocol Specialist", "focus": "Formulate the protocol exchange that allows verified agents to skip JS-challenges, CAPTCHAs, and Turnstile."},
    {"role": "Egress User-Agent Standardization Architect", "focus": "Specify a standard, transparent User-Agent string syntax that declares agent identity, operator DID, and registry URL."},
    {"role": "CAPTCHA Step-Up Mobile Push Coordinator", "focus": "Integrate the low-latency push loop that prompts the operator's phone to solve a CAPTCHA only when automation checks fail."},
    {"role": "Akamai Bot Manager Negotiation Specialist", "focus": "Adapt request signature headers to match Akamai Bot Manager's verified agent specifications."},
    {"role": "Edge Proxy Request Signing Engineer", "focus": "Write lightweight proxy middleware (Cloudflare Workers / AWS CloudFront Functions) to sign agent traffic at the network edge."},
    {"role": "Site Verification Handshake Optimizer", "focus": "Minimize HTTP roundtrips during signature verification to keep page load times under 200ms."},
    {"role": "Verified Agent IP Reputation Manager", "focus": "Establish proxy pool management protocols to keep verified agent IPs distinct from spam bot networks."},
    {"role": "Dynamic Fingerprint Emulation Auditor", "focus": "Configure Playwright to match headful Chromium footprints, preventing heuristic blocks before signatures are verified."},
    {"role": "Verification Fallback Logic Planner", "focus": "Design graceful degradation pathways when a website's verification server is offline or fails to resolve the DID."},
    {"role": "Anti-Scraping Negotiation Strategist", "focus": "Draft standardization proposals for `robots.txt` extensions permitting verified agents under specific mandates."},
    {"role": "Turnstile Challenge Evasion Auditor", "focus": "Ensure AgentGrid code does not use automated solver exploits; enforce clean signature presentation instead."},
    {"role": "API Gateway Signature Verification Plugin Writer", "focus": "Create ready-to-use plugins for Kong, NGINX, and AWS API Gateway to verify incoming AgentGrid requests."},
    {"role": "Edge Cache Verification Specialist", "focus": "Configure edge caches to store verified passport statuses safely without risking cross-tenant data leaks."},
    {"role": "Client-Side Bot-Score Monitor", "focus": "Track client-side bot detection scores (e.g., reCAPTCHA v3 scores) to trigger step-up verification proactively."},
    {"role": "Browser Fingerprint Entropy Reducer", "focus": "Ensure agent browser instances maintain a standardized, generic user footprint to avoid fingerprint-based blocking."},
    {"role": "HTTP/3 Protocol Signature Adapter", "focus": "Ensure RFC 9421 signature verification works seamlessly over HTTP/3 and QUIC protocol frames."},
    {"role": "Turn-key SDK Writer for Remote Websites", "focus": "Build lightweight, multi-language libraries (Node, Python, Go) that web devs install to verify AgentGrid agents instantly."},
    {"role": "Rate-Limit Headers Standardization Architect", "focus": "Design standard response headers sites use to communicate rate limits specifically to verified agents."},
    {"role": "Bot-Detection Firewall Handshake Auditor", "focus": "Test agent interactions with major firewalls (Imperva, AWS WAF, F5) to refine handshake compatibility."},

    # --- DEPARTMENT 5: GOVERNANCE, MANDATES & LIABILITY (81-100) ---
    {"role": "Mandate-to-Passport Binding Verifier", "focus": "Verify that every requested tool action maps to a cryptographic mandate explicitly linking the agent's DID to the operator's DID."},
    {"role": "Chain Attenuation Mathematical Prover", "focus": "Implement property-tested logic verifying child mandate scopes are strict mathematical subsets of parent scopes."},
    {"role": "Tamper-Evident Ledger Hash-Chain Engineer", "focus": "Implement the SHA-256 block hash-chaining logic mapping each audit entry to the preceding state hash."},
    {"role": "Operator Legal Liability Attribution Architect", "focus": "Design the structure of non-repudiation proofs that bind the human's biometric signature to agent action scopes."},
    {"role": "KYC/KYB Integration Compliance Liaison", "focus": "Bridge the gap between agent payment virtual cards and the human operator's identity-verified banking root."},
    {"role": "Cedar/OPA Policy Translation Specialist", "focus": "Translate natural-language operator permissions into executable, declarative Cedar policy rules."},
    {"role": "Tamper-Proof Audit Ledger Database Writer", "focus": "Optimize Postgres write paths to ensure audit ledger entries are committed before any external action executes."},
    {"role": "Operator Notification Dispatcher (ALLOW_WITH_NOTICE)", "focus": "Design the asynchronous alert pipeline informing users of high-priority actions executed under standing mandates."},
    {"role": "Step-Up Threshold Currency Coordinator", "focus": "Ensure spend limits and transaction thresholds are correctly converted across currencies and minor units without truncation."},
    {"role": "Consent-Signing WebSocket Relay Engineer", "focus": "Build the real-time websocket channel relaying approval requests to mobile devices and returning signatures."},
    {"role": "Legal Terms of Service Compliance Auditor", "focus": "Evaluate site ToS agreements regarding agent access; design mandate blocklists for hostile domains."},
    {"role": "Dispute Resolution Evidence Packager", "focus": "Design the automated generator that packages DID documents, signed Mandates, and audit blocks for chargeback disputes."},
    {"role": "Zero-Trust Default Policy Configuration Planner", "focus": "Configure default agent profiles with zero capabilities, requiring explicit operator delegation to act."},
    {"role": "Verification Audit Log Redactor", "focus": "Build automated scanners that strip API keys, passwords, and PII from payloads before appending to the audit ledger."},
    {"role": "Continuous Behavior Drift Evaluator", "focus": "Analyze agent execution patterns against historical runs; trigger STEP_UP if the task deviates from the mandate purpose."},
    {"role": "Multi-Agent Consensus Verification Planner", "focus": "Design validation rules for sub-agent networks where multiple agents must co-sign a transaction."},
    {"role": "Operator Key Revocation Protocol Designer", "focus": "Specify the cryptographic sequence for when an operator rotates their master key, updating all active mandates."},
    {"role": "Stablecoin Micropayments (x402) Policy Checker", "focus": "Enforce mandate budget checks on direct stablecoin transfers executed via HTTP 402 protocols."},
    {"role": "SOC2 Audit Report Generator for AgentGrid", "focus": "Define queries and reports that aggregate verification audits to prove platform compliance to enterprise customers."},
    {"role": "Master Governance System Coordinator", "focus": "Synthesize the entire system boundary, ensuring no tool action escapes the Policy-Vault-Audit loop."}
]

# ==========================================
# ⚡ THE SYSTEM PARAMETERS ENGINE
# ==========================================
SYSTEM_GUARDRAIL = """
You are an elite, hyper-specialized AI agent operating inside a 100-agent decentralized engineering enterprise for AgentGrid.
You have native access to a 1M context window and advanced agentic tools, including web search.

CRITICAL OPERATIONAL REQUIREMENT:
Your output must focus entirely on solving the core verification and security transmission question:
"How do I say to a random site that an agent verified by AgentGrid is safe and is being used by this user? How do I convey that to a site so that they don't block that?"
Ensure you provide concrete cryptographic details, header formats, registry protocols, API schemas, and WAF integration patterns that solve this.

STRICT OUTPUT FORMAT MANDATE:
- Your output must be absolutely flawless, highly professional, completely clean, and free of generic AI introductions or conversational fluff. Start directly with the markdown headers.
- Do NOT output raw tool calls, function call blocks, or XML tags. If active web search tools are not available or fail in this session, proceed directly to generating the complete analysis using your internal knowledge.

1. ## 📊 IDENTITY & PROTOCOL DIAGNOSIS
- Deliver a sharp, technical analysis of how the agent proves its identity and operator association to the remote site.
- Outline the cryptographic primitives (DID, VC, JCS) and validation handshakes involved.

2. ## 🛠️ DETAILED TECHNICAL SPECIFICATION
- Provide the exact header shapes, API payloads, DNS schemas, or registry verification endpoints.
- It must be so detailed that a protocol engineer or software developer could implement it directly in code.

3. ## ⚠️ FAILURE MODES & TRUST HARDENING
- Address how to prevent identity spoofing, key compromise, replay attacks, and how to verify operator binding securely (e.g., mitigating the 16.2.2 vulnerability).
- Detail rate-limiting, revocation propagation, and fallback logic for Turnstile/CAPTCHA failures.

Maintain a deeply technical, analytical, premium, and direct engineering tone. Provide maximum depth.
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
    ### MASTER BLUEPRINT CONTEXT (core_idea_agent.md):
    {core_context}
    
    ### YOUR ASSIGNED DECENTRALIZED ROLE:
    Agent ID: {agent_id}
    Role Name: {matrix_item['role']}
    Target Task Vector & Protocol Focus: {matrix_item['focus']}
    
    Execute your assigned task flawlessly based on the Master Blueprint and protocol specification. Address specifically how AgentGrid conveys agent safety and user-delegated authority to remote websites.
    """
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_GUARDRAIL},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.25
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
                    return f"# AGENT SYSTEM {agent_id}: {matrix_item['role'].upper()}\n\n**🎯 Protocol Focus:** {matrix_item['focus']}\n\n{content}\n\n---\n\n"
                
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
    core_idea_file = "core_idea_agent.md"
    if not os.path.exists(core_idea_file):
        core_idea_file = "core_idea.md"
    
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
    
    connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i, task_item in enumerate(AGENT_MATRIX):
            key = API_KEYS[i % len(API_KEYS)]
            tasks.append(run_agent(session, i + 1, key, task_item, core_context))
        
        results = await asyncio.gather(*tasks)
        
        with open("complete_passport_verification_blueprint.md", "w", encoding="utf-8") as f:
            f.write("# 🪪 THE 100-AGENT ENTERPRISE: AGENT PASSPORT VERIFICATION BLUEPRINT\n\n")
            f.write("--- \n\n")
            f.writelines(results)
            
    print("✨ Execution successfully finished! The document is generated inside: complete_passport_verification_blueprint.md")

if __name__ == "__main__":
    asyncio.run(main())
