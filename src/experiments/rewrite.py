from debug import *
from presto_instance import *

def rewrite(source, match_template, rewrite_template):
    if DEBUG_ROOIBOS:
        print '[DEBUG ROOIBOS] source: %r' % source
        print '[DEBUG ROOIBOS] match template: %r' % match_template
        print '[DEBUG ROOIBOS] rewrite template: %r' % rewrite_template

    result = p.rewrite(source, match_template, rewrite_template)

    if result.status_code == 200:
        if DEBUG_ROOIBOS:
            print '[DEBUG ROOIBOS] rooibos result:', result
        return result.text
    else:
        if DEBUG_ROOIBOS:
            print '[DEBUG ROOIBOS] Error: could not rewrite!'
        return ''
