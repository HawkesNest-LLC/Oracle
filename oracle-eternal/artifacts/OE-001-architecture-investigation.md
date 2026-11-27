# What actually works: autonomous research engines for a writer on an iPhone

Artifact ID: OE-001
Date: 2026-11-27
Assignment: OE-000
Author: Merlin, at the direction of Noah Alexander Hawkes (Noah.Physical), First Light execution of ORACLE Eternal
Status: Research review. Mechanical review only. Human review required. Not canon. Not a scientific finding.
Evidence classes used in this artifact: VERIFIED means read first-hand in this console. REPORTED means stated by a secondary source that was read, but not checked against a primary document. UNVERIFIED means not checked here at all.

## 1. The requirement, restated

The human requirement is simple to state and hard to build. Noah Hawkes is a writer, researcher, and creator who works primarily through an iPhone. He is not a software engineer. He has years of accumulated work: Rendered Reality, LEGACY.GI, ORACLE, SOV1, Continuity Computing, Star Trek: Avalon, Jupiter Station, and the Noahverse, plus extensive historical conversations, research papers, manuscripts, specifications, and unfinished creative works. He is tired of manually transferring prompts between artificial intelligences to keep that work moving. He wants an ongoing agent that advances the work while he lives his life, and he wants to open his phone in the morning and see what was accomplished.

Four constraints shape every design choice that follows. First, the interface must be natural language from an iPhone, with no terminal and no routine troubleshooting. Second, nothing may be published automatically: public-safe research, private creative work, and personal material need different destinations and different approvals. Third, no financial obligation may be created silently; any paid API or subscription must be identified with its exact requirement and estimated cost before recurring execution is enabled. Fourth, the system must keep receipts: a durable ledger of what was examined, produced, corrected, and published, so that progress survives individual model sessions and failed jobs resume without repeating finished work.

This artifact investigates four existing approaches against that requirement, states what actually works, and records the architecture selected for ORACLE Eternal First Light.

## 2. Method and evidence classes

On 2026-11-27, the public documentation and repository pages listed in Section 11 were read. No account was created, no paid service was run, and no model was executed against a live API for this investigation. Repository facts about the Oracle repository itself were read first-hand through the GitHub connector: the repository root listing, the Research Atlas, the research index, the open problems agenda, and the single existing workflow file. Claims about other systems are labeled REPORTED where they rest on secondary coverage, and the memo says so. Nothing in this artifact claims that a scheduled run has been demonstrated, because none has. That demonstration requires a merged workflow on the default branch and an observed run, and Section 10 states this plainly.

## 3. System 1: JARVIS, the drussell23 ecosystem

JARVIS, described in its repository README as "Just A Rather Very Intelligent System," is a solo-built, three-repository system: JARVIS as the Body, J-Prime as the Mind, and Reactor Core as the Soul [1]. The README describes a unified supervisor that boots and coordinates the stack, macOS integration including screen vision, voice biometric authentication, and interface automation, runtime-resolved model references from a shared policy file, and explicit safety laws named in the README as the Immutable Orange Protocol and an air-gapped sandbox. It also describes a test spine used to keep a self-modifying system honest, and reports very large scale figures that the README says are generated from git by a script rather than transcribed by hand [1].

What is VERIFIED here is narrow: the README exists, is public, and says these things. The scale figures, the soak results, and the autonomy claims are REPORTED, meaning this investigation did not independently verify them by running the system or auditing the code. That distinction matters, because the numbers are extraordinary and the system is presented by its author as a research organism rather than a product.

The verdict for Noah's requirement is: real, instructive, and not directly reusable. JARVIS is a local-machine organism. It assumes an always-on Mac under its author's control, deep operating system integration, and continuous hands-on stewardship by the person who built it. Noah's requirement is the opposite shape: iPhone-first, no machine to tend, no plumbing to operate. Rebuilding JARVIS would put the writer back in the software engineering seat the mission exists to remove him from. What transfers is the pattern, not the machine: a small supervisor with explicit duties, a test spine that keeps the system honest, safety laws stated as enforceable checks rather than aspirations, and receipts for everything the system does. ORACLE Eternal First Light adopts exactly that pattern at a fraction of the scale, and Section 8 records how.

## 4. System 2: GitHub Agentic Workflows

GitHub Agentic Workflows is an open source project from GitHub Next. According to the GitHub Changelog entry dated October 28, 2026, it is generally available on github.com for GitHub Free, Team, and Enterprise plans [2]. The design is: an automation is defined in a natural language Markdown file with a small frontmatter block stating when it runs, what it may touch, and which AI engine powers it. A command line tool, gh-aw, compiles that Markdown file into a standard GitHub Actions workflow file. The supported engines reported in coverage of the release are GitHub Copilot by default, plus Claude, Codex, and Gemini, each with its own credential [3][4].

The safety model is the strongest part of the design, and it is the reason this system is the closest working equivalent to what the mission asks for. Agents run with read-only permissions by default. They execute inside a sandboxed container behind what GitHub calls the Agent Workflow Firewall. Proposed changes are routed through a separate job that holds write access, and that job can be gated behind reviewer requirements. The general availability release added budget forecasting through a forecast command, model routing per task, and deeper isolation options [2][4]. The default spending cap reported for the release is 1,000 AI Credits, stated as 10 dollars, per run, with forecasting available before a run is enabled [4].

The verdict is: this is what actually works for scheduled reasoning work inside a repository, and it is gated on two things Noah has not yet approved. First, a credential: the default Copilot engine requires a Copilot license and consumes AI Credits, while the other engines require their own API keys [4]. Second, a spending decision: the cap exists, but enabling the workflow creates a metered obligation, and the mission forbids silent financial obligations. First Light therefore does not ship an agentic workflow. Compiling one requires the gh-aw tool and a credential, neither of which was verified in this console. Section 9 records the exact activation steps and the cost question that must be answered first. The deterministic engine in First Light is the correct predecessor: it proves selection, retrieval, review, saving, read-back, receipts, and persistence without any metered call, so that when a credentialed engine is approved, it inherits a working ledger and a working queue instead of a blank slate.

## 5. System 3: OpenAI Codex

Codex is OpenAI's coding agent product line. It has three surfaces that matter here: an open source command line interface, an extension inside editors and the ChatGPT desktop application, and Codex Cloud, a cloud task runner that can be started from the web or from a phone with a GitHub repository connected, after which it reads the repository, makes changes, runs checks, and opens pull requests [5][6]. Coverage of the product reports that it is included in ChatGPT plans, with Plus reported at 20 dollars per month and Pro reported from 100 dollars per month, and that a pay-per-token route through an OpenAI API key is also available [5][6]. Those prices are REPORTED, not verified against Noah's own account, and plan limits for Codex change frequently enough that any figure here must be rechecked before money is spent.

The verdict is: Codex Cloud is the best available path for a one-off mission pasted from an iPhone today, because it needs no local machine and no workflow file. Noah's own mission text anticipated exactly this, naming Codex first and ChatGPT Work with GitHub connected as the iPhone route. Three cautions apply. First, subscription and limit status for Noah's own account was not verified in this console, and the mission explicitly warns not to assume a subscription provides unrestricted API access. Second, Codex Cloud operates under its own product limits and review model; it is an engineering agent, not a governed publication pipeline, so its output still needs the SOV1 gates in Section 8 before anything is treated as published or canonical. Third, Codex is a way to execute a mission, not a substitute for the ledger: work done in Codex Cloud must still be recorded in the ORACLE Eternal ledger, or the next run will not know it happened. First Light records this as an operating rule rather than assuming any integration exists.

## 6. System 4: Scheduled GitHub Actions

Scheduled GitHub Actions are the scheduler underneath the other options, and they work on their own for deterministic work. A workflow file on the default branch with a cron trigger runs on GitHub-hosted runners. For public repositories, standard runner minutes are free with no minute cap, as reported across multiple independent write-ups of GitHub's billing behavior [7][8]. The constraints that shape real use are equally well reported: scheduling is best effort, runs can be delayed under load especially at the top of the hour, queued jobs can be dropped, the minimum interval is five minutes, a single job is capped at six hours, the workflow file must exist on the default branch or the schedule never fires, and schedules in public repositories are automatically disabled after sixty days without repository activity [7][8]. Every run gets a fresh virtual machine that is wiped afterward, so no state survives unless it is written back to the repository, to artifacts, or to external storage [7].

The verdict is: the scheduler is real, free for this public repository, and sufficient for one careful daily run, provided the design never assumes precision, persistence, or privacy from the runner itself. Those three properties must come from the repository: the ledger and queue live in git, the briefing is a file, and secrets live only in repository settings, never in code. First Light is built to exactly these constraints. The workflow runs at 13:17 UTC, which is 7:17 a.m. Central time, deliberately off the top of the hour, with a concurrency guard, a ten minute timeout, and tests that must pass before any state is written.

## 7. Comparison: what actually works

JARVIS shows that a governed supervisor with a test spine and explicit safety laws can run for a long time under one author's care. It does not show that such a system can be handed to a writer on a phone. GitHub Agentic Workflows shows that scheduled reasoning work with read-only agents, safe outputs, and budget caps is a shipping product. It does not remove the credential and spending decisions. Codex shows that a mission can be executed from a phone into a pull request today. It does not provide the ledger, the publication gates, or the morning briefing. Scheduled GitHub Actions show that a free, daily, repository-backed run is available. They do not provide reasoning, persistence, or judgment on their own.

The honest synthesis is that no single existing system satisfies the whole requirement, and no system satisfies it for zero setup. What works is a composition: scheduled Actions for timing, a deterministic engine for selection, retrieval, review, and receipts, a repository-backed ledger for memory, draft pull requests for publication, and a credentialed reasoning engine added later, once its cost is approved, to do the manuscript generation the deterministic engine must abstain from. That composition is what First Light builds.

## 8. The selected architecture

ORACLE Eternal First Light implements the composition in the smallest form that can be verified:

Selection. The queue in oracle-eternal/queue.json is seeded from sources located first-hand: the seven candidate problems in OPEN_PROBLEMS.md and the six entries of the Research Atlas index. The engine selects the first queued assignment the ledger does not record as completed.

Retrieval. The engine reads the Atlas index and hashes each located source file, recording the hashes in the receipt. A missing source is recorded as a finding, not hidden.

Related work and duplication. The mechanical review compares artifact titles against ledger and Atlas titles, and requires a Sources section and a Limitations or Evidence section.

Production. The engine produces nothing on its own. When an artifact is supplied, as this memo was, the engine verifies it, classifies it, and records it. When no artifact is supplied and no model is configured, the engine abstains and records the abstention. The model execution path is designed but unbuilt, and the code refuses it explicitly rather than failing silently.

Review. The MERLIN role runs mechanical checks: section presence, citation format, duplication, length, absolute claim language, and secret patterns. The record is stamped mechanical, not an independent model attestation. Independent attestation requires a second model execution, which is unavailable in First Light and is labeled as such wherever it would matter.

Classification and publication. The SOV1 policy module classifies every artifact. Blocked categories, including secrets, private family information, medical or financial records, confidential employment material, private conversations, and unreviewed personal manuscripts, are refused or held for review by code. Fiction is candidate only and branch-labeled, and canon promotion is refused without an approval record. The scheduled workflow writes only to the oracle-eternal/state branch, holding ledger, briefing, receipts, and proposals. It never merges, never publishes to the default branch, and never opens a publication pull request on its own.

Memory. The ledger is append-only JSON with a SHA-256 hash chain. It records sources examined, assignments completed, artifacts produced, corrections, failures, abstentions, costs, and model information. The runtime ledger seeds from the shipped snapshot, so the first scheduled run continues where First Light stopped instead of repeating it.

Briefing. The engine generates oracle-eternal/briefing/latest.md from the ledger and the queue: what was discovered, what was written, why it matters, links, failures, decisions awaiting approval, costs, and the next proposed assignment. After activation, the single iPhone-readable location is that file on the state branch, rendered by GitHub, plus the workflow run artifacts.

Crew roles. REG, MERLIN, ALEXANDRIA, LIGHTHOUSE, ELLIE, and SOV1 are implemented as labeled mechanical functions with stated limits, not as personas. Where a role needs a model, the function records that the capability is unavailable instead of pretending otherwise.

## 9. Costs

Recorded cost of First Light: zero dollars. No API was called, no subscription was used, and the scheduled workflow for a public repository uses free standard runner minutes [7][8]. Future options, with the verification each one still needs:

Agentic Workflows with the Copilot engine: requires a Copilot license and consumes AI Credits, with a reported default cap of 1,000 AI Credits, stated as 10 dollars, per run, and a forecast command to estimate spend before enabling [4]. Verify the current license and credit position before enabling.

Agentic Workflows with Claude, Codex, or Gemini engines: requires that provider's API key, billed per that provider's current rates. Rates were not quoted here because they change; obtain the current rate and set the spending limit before enabling.

Codex Cloud: included in ChatGPT plans under reported pricing, or billed through an API key [5][6]. Verify Noah's own plan, limits, and whether the shared account's terms permit this use before relying on it.

No recurring obligation is created by First Light. The spending limit in the engine configuration is zero dollars per day, and the engine abstains from any step that would spend.

## 10. Limitations and what is not claimed

Scheduled execution has not been demonstrated. The workflow file exists on a review branch, and scheduled workflows only fire from the default branch. The first scheduled run after merge is the demonstration, and until it appears in the Actions tab, autonomous operation is not claimed. The engine's scheduled mode was verified only by local simulation: two consecutive runs against a seeded ledger, in which the second run selected the next assignment and abstained rather than repeating the first. Those simulations are recorded in the First Light receipt.

No live literature discovery was performed by the engine. The LIGHTHOUSE role returns a curated list from this dated investigation. No ChatGPT or Claude conversation archive was accessed, because the export has not been received in this console; the engine claims no such access. Alexandria's Atlas work in the repository is landing concurrently from another system, including commits on the morning of 2026-11-27; the engine reads the Atlas as found and proposes additions without overwriting it, but concurrent writes remain a coordination risk that Noah's review of each pull request must manage. Finally, this artifact was written by one system, Merlin, at Noah's direction. It has had mechanical review only. No independent cross-model attestation was performed, and the memo's verdicts should be treated as a research review, not as established findings about these systems.

## 11. Sources

[1] drussell23, JARVIS repository README. VERIFIED: page read 2026-11-27. Scale and autonomy claims inside it are REPORTED. https://github.com/drussell23/jarvis/blob/HEAD/README.md

[2] GitHub Changelog, "GitHub Agentic Workflows generally available," October 28, 2026. VERIFIED: changelog entry read 2026-11-27. https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available/

[3] KDnuggets, "Getting Started with GitHub Agentic Workflows." REPORTED: secondary coverage read 2026-11-27. https://www.kdnuggets.com/getting-started-with-github-agentic-workflows

[4] DataStudios, "GitHub Agentic Workflows generally available: engines, safe outputs, costs and plans." REPORTED: secondary coverage read 2026-11-27. https://www.datastudios.org/post/github-agentic-workflows-generally-available-markdown-coding-agents-actions

[5] Tailkits, "OpenAI Codex: Pricing, Limits and Alternatives," updated November 2026. REPORTED: secondary coverage read 2026-11-27. https://tailkits.com/tools/openai-codex/

[6] Pandromeda, "OpenAI Codex Explained: Pricing, CLI and Features [2026]." REPORTED: secondary coverage read 2026-11-27. https://pandromeda.com/software/what-is-openai-codex-pricing-features-and-how-it-works

[7] Joor0x, "Free Scheduled VMs: Run Periodic Jobs on GitHub Actions." REPORTED: secondary coverage read 2026-11-27. https://joor0x.github.io/posts/github-actions-free-scheduled-vms/

[8] Dev.to, "How to Stay Within GitHub Actions' Free Minutes." REPORTED: secondary coverage read 2026-11-27. https://dev.to/procwire/how-to-stay-within-github-actions-free-minutes-1g52

Repository sources, VERIFIED first-hand through the GitHub connector at commit db1829ff690c5bbdd693ab93e0b32c4b9dfd2273, 2026-11-27: RESEARCH_ATLAS.md, research-index.json, RESEARCH_DEPENDENCIES.md, RESEARCH_TIMELINE.md, OPEN_PROBLEMS.md, and the repository root listing showing a single existing workflow file, .github/workflows/amplify.yml.

The witness must not become the author. The human keeps the keys. The system keeps the receipts. The ship remembers. The captain decides.
