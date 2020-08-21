import html


def unquote(text):
    return html.unescape(text).replace('\t', ' ')
