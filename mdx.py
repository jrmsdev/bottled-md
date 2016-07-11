# https://github.com/Undeterminant/markdown-newtab/blob/master/markdown_newtab/__init__.py

import re
from markdown.extensions import Extension
from markdown.inlinepatterns import LINK_RE, LinkPattern


class LocalLinks(LinkPattern):
    exturl_re = re.compile(r'^[^:]+:')

    def handleMatch(self, match):
        elem = super(LocalLinks, self).handleMatch(match)
        href = elem.get('href')
        if href and href.endswith('.md'):
            if not self.exturl_re.match(href):
                elem.set('href', href.replace('.md', '.html'))
        return elem


class MDX(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = LocalLinks(LINK_RE, md)
