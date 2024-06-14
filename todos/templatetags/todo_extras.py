from django import template
from re import sub, IGNORECASE, compile

register = template.Library()

def repl_func(matchObj) -> str:
    href_tag, url = matchObj.groups()
    if href_tag:
        return matchObj.group(0)
    else:
        return '<a target="_blank" href="%s">%s</a>' % (url, url)

@register.filter(name='rich_text')
def rich_text(value:str) -> str:
    pattern = compile(
        r'((?:<a href[^>]+>)|(?:<a href="))?'
        r'((?:https?):(?:(?://)|(?:\\\\))+'
        r"(?:[\w\d:#@%/;$()~_?\+\-=\\\.&](?:#!)?)*)",
        flags=IGNORECASE)
    result:str = sub(pattern, repl_func, value)
    return result.replace('\n', '<br />')
