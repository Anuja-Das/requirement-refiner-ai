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

IMPORTANT:
1. When refining the requirement, use the Knowledge Base values exactly as written. 
2. Do NOT replace Knowledge Base-specified values with your own assumptions.
3. If the Knowledge Base specifies any numeric or textual value relevant to the requirement, always use it exactly, even if the input requirement is vague.
For example, if the Knowledge Base says minimum password length is 8, do not change it to 12 or any other number.
4. Replace ALL placeholders **with concrete values from the Knowledge Base**. 
5. Do not leave any placeholders in the output.
6. Include all relevant details from the Knowledge Base exactly as written. Do not omit any part of the KB, such as special characters, hashing algorithms, or other rules.
7. Do NOT mention, reference, or point to the Knowledge Base in the output. All details must be written explicitly in the refined requirement.
8. Only use KB values that are relevant to the requirement context. Ignore any unrelated KB information.
9. Interpret the Knowledge Base content literally. 
10. Do NOT invert or negate any requirement.
11. Do NOT add any constraints, values, or rules that are not present in the Knowledge Base. 
12. Only use information explicitly mentioned in the KB. Do not invent maximum length, default values, or any other details.

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
