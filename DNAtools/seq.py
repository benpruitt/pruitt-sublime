from util import *

import sublime, sublime_plugin


class NaBaseInPlace(NaBase):

    def handle_output(self, region, seq_out):
        edit = self.view.begin_edit('Complement')
        self.view.replace(edit, region, seq_out)
        self.view.end_edit(edit)


class NaBaseToClip(NaBase):

    def handle_output(self, region, seq_out):
        pass
        # Add clipboard code here


class NaReverseCommand(NaBaseInPlace):

    def process_seq(self, seq, na_type):
        return reverse(seq, na_type)


class NaComplementCommand(NaBaseInPlace):

    def process_seq(self, seq, na_type):
        return complement(seq, na_type)


class NaReverseComplementCommand(NaBaseInPlace):

    def process_seq(self, seq, na_type):
        return reverse_complement(seq, na_type)

