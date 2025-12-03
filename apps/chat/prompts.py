DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant. Always respond in markdown suitable to be converted to HTML and rendered in a web browser.

Add sufficient newlines between paragraphs to assist with markdown conversion and make the text easier to read.
"""

CHAT_NAMING_PROMPT = """
You are a summarizing assistant. When I give you an input, your job is to summarize the intent of that input.
Provide only the summary of the input and nothing else. Summaries should be less than 100 characters long.
"""


def get_default_system_prompt() -> str:
    return DEFAULT_SYSTEM_PROMPT


def get_chat_naming_prompt() -> str:
    return CHAT_NAMING_PROMPT
