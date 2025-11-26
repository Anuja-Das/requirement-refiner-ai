# Requirement Refiner AI

Requirement Refiner AI is an **agentic system** that converts raw, messy stakeholder statements into clear, unambiguous, engineering-ready requirements with acceptance criteria.

It strengthens requirement quality at the earliest SDLC stage, **preventing costly rework** later and ensuring every engineering, QA, and product deliverable starts on a **solid foundation**.

---

## Features

- Detects ambiguous terms and unclear language
- Identifies missing details or incomplete logic
- Rewrites the requirement into final engineering format
- Generates testable acceptance criteria
- Produces two JSON outputs:
    - `analysis_output.json`
    - `final_requirement_output.json`

---

## System components

![System components](assets/system%20blueprint.png)

---

## Functional overview

1. **Input Requirement**: Raw stakeholder requirement text.
2. **Agent 1 - Requirement Analyzer**:
    - Uses NLP to analyze the input requirement.
    - Detects ambiguities and missing information.
    - Outputs an analysis report in JSON format.
    - Saves to `analysis_output.json`.
3. **Agent 2 - Requirement Refiner**:
    - Takes the analysis report and original requirement.
    - Rewrites the requirement into a clear, unambiguous format.
    - Generates acceptance criteria.
    - Outputs the final refined requirement in JSON format.
    - Saves to `final_requirement_output.json`.

---

## Data flow process

![Data flow process](assets/data%20flow%20process.png)

---

## Project Structure

<pre>
requirement-refiner-ai/
│
├── main.py                             # Run this
├── requirements.txt
│
├── data/
│ ├── requirement_input.txt             # INPUT
│ ├── analysis_output.json              # Agent 1 output
│ └── final_requirement_output.json     # Agent 2 output
│
├── app/
│ │
│ ├── agents/
│ │ ├── analyzer_agent.py
│ │ ├── refiner_agent.py
│ │
│ ├── config/
│ │ ├── llm_config.py
│ │
│ ├── core/
│ │ ├── llm_adapter.py
│ │ ├── prompts.py
│ │ ├── schemas.py
│ │
│ ├── tools/
│ │ ├── acceptance_criteria_gen_tool.py
│ │ ├── ambiguity_detector_tool.py
│ │ ├── missing_info_extractor_tool.py
│ │ └── requirement_rewriter_tool.py

</pre>

---

## Execution steps

(tested for Python 3.13.9)

1. Place raw requirement text inside:
   data/requirement_input.txt
2. Run:  
   pip install -r requirements.txt
3. Run:  
   python main.py
4. Output files
   - data/analysis_output.json
   - data/final_requirement_output.json

---

## Next-step features

### 1. Domain-Aware Refinement Profiles

Let the user choose a domain preset, for example:
- Supply Chain
- E-commerce
- Healthcare
- Finance
- Manufacturing

Each profile injects domain rules + vocabulary into the refinement process.

### 2. Duplicate Requirement Detection

Useful for large requirement docs.
- Detect overlapping or redundant requirements
- Suggest merging

### 3. Auto-Generate Test Cases

From the refined requirement + AC:
- Positive test cases
- Negative test cases
- Edge cases

Very powerful for QA teams.

### 4. Requirement Change Impact Analyzer

If an input requirement changes, compare:
- What changed?
- Which ACs need updating?
- What tests break?

### 5. Document Upload Support

Instead of typing text:
- Upload PDF, Word, Notion export
- System extracts text
- Runs analysis

---

## RAG Integration Ideas

### 1. Use Domain Documents

RAG can look up industry-related docs (finance, logistics, healthcare, etc.) to better understand the requirement and generate more accurate results.

### 2. Use Company Policies

Store your internal standards (security rules, UX guidelines, SLAs).
RAG will fetch them automatically so every requirement follows your company’s rules.

### 3. Use Past Requirements

Save previously refined requirements.
RAG will retrieve similar ones to keep new requirements consistent and complete.

---