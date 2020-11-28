import html
import re


def unquote(text):
    proc = html.unescape(text).replace('\t', ' ').replace('\n', '')  # Remove tabulations, new lines, html entities
    proc = re.sub(r'<.+?>', '', proc)  # Remove HTML tags
    proc = re.sub(r'\s+', ' ', proc)  # Condense multiple spaces
    return proc
