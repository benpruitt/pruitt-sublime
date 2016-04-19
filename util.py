import re
import sublime
import sublime_plugin
try:
    from string import maketrans
except:
    try:
        from str import maketrans
    except:
        maketrans = str.maketrans


__all__ = ['_DNA_COMP', '_RNA_COMP', '_NA_RE', '_DNA_RE', '_RNA_RE',
           '_RNA_TO_DNA', 'seqQC', 'complement', 'reverse_complement',
           'reverse', 'NaBase']


_DNA_COMP = maketrans('ATGCatgcKMRYSWBVHDXN.- ',
                      'TACGtacgMKYRSWVBDHXN.- ')

_RNA_COMP = maketrans('AUGCaugcKMRYSWBVHDXN.- ',
                      'UACGuacgMKYRSWVBDHXN.- ')

_RNA_TO_DNA = maketrans('Uu','Tt')

_NA_RE = re.compile('[ATGCUatgcuKMRYSWBVHDXN\.\- ]+')
_DNA_RE = re.compile('[ATGCatgcKMRYSWBVHDXN\.\- ]+')
_RNA_RE = re.compile('[AUGCaugcKMRYSWBVHDXN\.\- ]+')


def seqQC(seq):
    if re.match(_DNA_RE, seq):
        return 'DNA'
    if re.match(_RNA_RE, seq):
        return 'RNA'
    else:
        return None


def complement(seq, na_type):
    trans = _DNA_COMP if na_type == 'DNA' else _RNA_COMP
    return seq.translate(trans)


def reverse_complement(seq, na_type):
    return complement(seq, na_type)[::-1]


def reverse(seq, na_type):
    return seq[::-1]


class NaBase(sublime_plugin.TextCommand):
    ''' Base class for Na commands. Override process_seq and handle_output
        for individual subclasses.
    '''

    def run(self, edit):
        region = self.view.sel()[0]
        seq = str(self.view.substr(region).strip())
        na_type = seqQC(seq)
        if not na_type:
            sublime.error_message('Selected text contains invalid DNA/RNA ' +
                                  'bases. Valid bases include: \n\n' +
                                  'DNA: ATGCatgcKMRYSWBVHDXN.- \n' +
                                  'RNA: AUGCaugcKMRYSWBVHDXN.-')
        else:
            seq_out = self.process_seq(seq, na_type)
            self.handle_output(edit, region, seq_out)


    def handle_output(self, region, seq_out):
        pass

    def process_seq(self, seq, na_type):
        return seq

    def is_enabled(self):
        region = self.view.sel()[0]
        seq = self.view.substr(region).strip()
        if re.match(_NA_RE, seq):
            return True
        else:
            return False
