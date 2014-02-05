import re

import sublime, sublime_plugin


class SpanCommentCommand(sublime_plugin.TextCommand):
    '''
    Creates or balances a span comment at the current text cursor position.

    Turns:

    #~~~~~~~~~~~ Foo ~~~~~~~~~~~~~~~~~~~#
    Bar

    Into:

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Foo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bar ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    Currently supports: C, Java, JavaScript, Python

    '''

    _LANGS = {
        'C': {
            'F_DELIM': '/*',
            'R_DELIM': '*/',
            'SPACER': '~'
        },
        'JAVA': {
            'F_DELIM': '/*',
            'R_DELIM': '*/',
            'SPACER': '~'
        },
        'JAVASCRIPT': {
            'F_DELIM': '//',
            'R_DELIM': '//',
            'SPACER': '~'
        },
        'PYTHON': {
            'F_DELIM': '#',
            'R_DELIM': '#',
            'SPACER': '~'
        }
    }

    _spacers = set([v['SPACER'] for v in _LANGS.values()])
    _fdelims = set([v['F_DELIM'] for v in _LANGS.values()])
    _rdelims = set([v['R_DELIM'] for v in _LANGS.values()])
    _spacers_re = r'[{0}]*'.format('|'.join(_spacers)) 
    _fdelims_re = r'[{0}]'.format('|'.join(_fdelims)) 
    _rdelims_re = r'[{0}]?'.format('|'.join(_fdelims)) 
    _SPAN_RE = re.compile(r'\s*' + _fdelims_re + r'\s*' + _spacers_re + \
                          r'([^~]+)' + _spacers_re + r'\s*' + _rdelims_re + \
                          r'\s*')
    _PRE_WS_RE = re.compile('^([ |\t]+)')
    _EOL_RE = re.compile(r'([\r|\n|\r\n])')


    def run(self, edit):
        pos = self.view.sel()[0].begin()
        full_line = self.view.full_line(pos)
        text = self.view.substr(full_line)
        find_eol_char = re.search(SpanCommentCommand._EOL_RE, text)
        eol_char = find_eol_char.group(1) if find_eol_char else ''
        find_pre_ws = re.search(SpanCommentCommand._PRE_WS_RE, text)
        pre_ws = find_pre_ws.group(1) if find_pre_ws else ''
        match = re.match(SpanCommentCommand._SPAN_RE, text)
        if match:
            text = match.group(1).strip()
        else:
            text = text.strip()
        edit = self.view.begin_edit('Span Comment')
        self.replace(full_line, edit, text, eol_char=eol_char, pre_ws=pre_ws)
        self.view.end_edit(edit)


    def replace(self, region, edit, text, eol_char, pre_ws):
        ld = self.get_lang_dict()
        fdelim, rdelim, spacer = ld['F_DELIM'], ld['R_DELIM'], ld['SPACER']
        padding = 77 - len(fdelim) - len(rdelim) - len(pre_ws)
        if len(text) > 0:
            text_out = ' {0} '.format(text).center(padding, spacer)
        else:
            text_out = 75 * spacer
        rep_text = '{0}{1} {2} {3}{4}'.format(pre_ws, fdelim, text_out, 
                                              rdelim, eol_char)
        self.view.replace(edit, region, rep_text)


    def get_lang_dict(self):
        cur_syntax = self.view.settings().get('syntax')
        for lang, lang_dict in SpanCommentCommand._LANGS.items():
            if lang in cur_syntax.upper():
                return lang_dict
        return None       


    def is_visible(self):
        if self.get_lang_dict():
            return True
        else:
            return False


    def is_enabled(self):
        return self.is_visible()
