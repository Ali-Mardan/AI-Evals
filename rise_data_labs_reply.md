# 📧 Email Draft — Rise Data Labs Reply

> **To**: Ayoub Tabout <ayoub@risedatalabs.com>  
> **Subject**: Re: Internship Invitation: Building LLM-as-a-Judge Architecture

---

Hi Ayoub,

Thanks for reaching out — the project sounds like exactly the kind of work I've been actively exploring.

I've spent time working on both sides of the eval problem. In a recent competition, I built and evaluated a factuality detection system for AI-generated educational content — classifying LLM responses as factual, contradictory, or irrelevant using a combination of NLI-based faithfulness scoring (AlignScore) and semantic similarity. That work gave me a concrete feel for where automated metrics fall short, particularly with detecting irrelevance versus contradiction.

More recently, I built an LLM-as-a-Judge pipeline from scratch: a multi-dimensional rubric system that evaluates frontier model responses across dimensions like accuracy, reasoning quality, completeness, and conciseness. A few design choices I found important: chain-of-thought before scoring reduces anchoring bias, temperature=0 improves reproducibility, and separating the judge model from the evaluated models avoids self-enhancement bias.

The direction you're describing — automating evaluation against complex, multi-layered rubrics to solve the bottleneck of manual alignment — maps directly to the problems I've been working through. I'd love to learn more about the specific models you're benchmarking and how you're structuring the rubric design process.

Very interested — happy to share more details or the pipeline itself whenever convenient.

Best,
[Your Name]

---

## Notes on This Draft

**Why this works:**
- Opens with specific, relevant experience (not generic enthusiasm)
- Drops exact terminology they used: *multi-layered rubrics*, *automated evals*, *model alignment*
- Shows you know the *hard problems* (bias, calibration) — signals you're technical, not surface-level
- Asks a smart question at the end → shows genuine curiosity + keeps the conversation going
- Unpaid acknowledgment is absent (not worth flagging; reply first, negotiate later)

**Things to personalize before sending:**
- [ ] Add your actual name
- [ ] Optionally: mention UChicago explicitly if you want to signal affiliation
- [ ] Optionally: mention the hackathon more specifically ("a university hackathon on LLM eval")
- [ ] Tone-check: this is confident but professional — adjust if it feels too formal/informal for you
