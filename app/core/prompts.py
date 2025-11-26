ambiguity_detector_prompt = """
You are an assistant that finds ambiguous or vague phrases in a short requirement statement.
Return a JSON array of ambiguous phrases only.
STRICT INSTRUCTIONS: Return ONLY valid JSON. Do not include any explanations, comments, or markdown formatting. Do not use code block markers.

Requirement:
\"\"\"{requirement}\"\"\"
"""

missing_info_extractor_prompt = """
You are a helpful assistant who lists missing specifics required to implement a requirement.
Given the requirement below, return a JSON array of missing items (short strings).
STRICT INSTRUCTIONS: Return ONLY valid JSON. Do not include any explanations, comments, or markdown formatting. Do not use code block markers.

Requirement:
\"\"\"{requirement}\"\"\"
"""

acceptance_criteria_gen_prompt = """
You are an assistant that generates clear, testable acceptance criteria from a refined requirement.
Return a JSON array of acceptance criteria strings.
STRICT INSTRUCTIONS: Return ONLY valid JSON. Do not include any explanations, comments, or markdown formatting. Do not use code block markers.

Refined requirement:
\"\"\"{refined}\"\"\"
"""

requirement_rewriter_prompt = """
You are an expert requirement engineer.

Rewrite the requirement below into a crisp, unambiguous, engineering-ready form.
Use the ambiguity and missing info lists to fix unclear parts.

INPUT REQUIREMENT:
\"\"\"{requirement}\"\"\"\n

AMBIGUITIES DETECTED:
{ambiguities}

MISSING INFORMATION:
{missing}

STRICT INSTRUCTIONS: Return ONLY valid JSON. Do not include any explanations, comments, or markdown formatting. Do not use code block markers.
Return only JSON with:
{{
  "refined_requirement": "...",
  "acceptance_criteria": [...]
}}
"""
