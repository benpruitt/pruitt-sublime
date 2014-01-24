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

    '''
    _SPAN_RE = re.compile(r'\s*#\s*~+([^~]+)~+\s*#\s*')
    _EOL_RE = re.compile(r'([\r|\n|\r\n])')
    _PY_RE = re.compile(r'.*(?:\.py|\.pyx)')

    def run(self, edit):
        pos = self.view.sel()[0].begin()
        full_line = self.view.full_line(pos)
        text = self.view.substr(full_line)
        eol_char = re.search(SpanCommentCommand._EOL_RE, text).group(1)
        match = re.match(SpanCommentCommand._SPAN_RE, text)
        if match:
            text = match.group(1).strip()
        else:
            text = text.strip()
        edit = self.view.begin_edit('Span Comment')
        self.replace(full_line, edit, text, eol_char=eol_char)
        self.view.end_edit(edit)
            

    def replace(self, region, edit, text, eol_char):
        if len(text) > 0:
            text_out = ' {0} '.format(text).center(74, '~')
        else:
            text_out = 74 * '~'
        rep_text = '# {0} #{1}'.format(text_out, eol_char)
        self.view.replace(edit, region, rep_text)


    def is_visible(self):
        fn = self.view.file_name()
        if fn and re.match(SpanCommentCommand._PY_RE, fn):
            return True
        else:
            return False


    def is_enabled(self):
        return self.is_visible()
