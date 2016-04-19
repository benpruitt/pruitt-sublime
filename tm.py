import math

import sublime

from .util import *


R = 1.9872e-3  # Gas constant (1 / kcal * mol)
KELVIN = 273.15


def divalent_to_monovalent(divalent, dntp):
    if divalent == 0:
        dntp = 0
    if divalent < dntp:
        divalent = dntp
    return 120 * math.sqrt(divalent-dntp)


def calc_thermo(seq, conc_nm=50, monovalent=50, divalent=0.01, dntp=0.0):
    ''' Return the thermo parameters for DNA under specified salt cond.

    '''

    enthalpies = {
        'AA': 79, 'AT': 72, 'AG': 78, 'AC': 84,
        'TA': 72, 'TT': 79, 'TG': 85, 'TC': 82,
        'GA': 82, 'GT': 84, 'GG': 80, 'GC': 98,
        'CA': 85, 'CT': 78, 'CG': 106, 'CC': 80
    }
    entropies = {
        'AA': 222, 'AT': 204, 'AG': 210, 'AC': 224,
        'TA': 213, 'TT': 222, 'TG': 227, 'TC': 222,
        'GA': 222, 'GT': 224, 'GG': 199, 'GC': 244,
        'CA': 227, 'CT': 210, 'CG': 272, 'CC': 199
    }
    dH = dS = 0
    # Calculate oligo symmetry
    sym = seq == reverse_complement(seq, 'DNA')
    # Calculate NN uncorrected dS and dH for oligo
    for idx in range(len(seq)-1):
        dH += enthalpies[seq[idx:idx+2]]
        dS += entropies[seq[idx:idx+2]]
    # Terminal AT penalty and initiation parameters (combined)
    if seq[0] in 'AT':
        dH += -23
        dS += -41
    else:
        dH += -1
        dS += 28
    if seq[-1] in 'AT':
        dH += -23
        dS += -41
    else:
        dH += -1
        dS += 28
    if sym:
        dS += 14
    dH *= -100.0
    dS *= -0.1
    # Convert divalent salt and dntp conc. to monovalent equivalencies
    monovalent += divalent_to_monovalent(divalent, dntp)
    dS = dS + 0.368 * (len(seq) - 1) * math.log(monovalent / 1000.0)
    # Account for oligo symmetry and calculate tm
    if sym:
        tm = dH / (dS + 1.987 * math.log(conc_nm/1.0e9)) - KELVIN
    else:
        tm = dH / (dS + 1.987 * math.log(conc_nm/4.0e9)) - KELVIN
    return dH, dS, tm


def calc_tm(seq, conc_nm=50, monovalent=50, divalent=0.01, dntp=0.0):
    _, _, tm = calc_thermo(seq, conc_nm=50, monovalent=50, divalent=0.01,
                           dntp=0.0)
    return tm


class NaTmDefaultsCommand(NaBase):

    def process_seq(self, seq, na_type):
        if na_type == 'RNA':
            seq = seq.translate(_RNA_TO_DNA)
        return calc_tm(seq)


    def handle_output(self, region, tm):
        sublime.message_dialog('Tm = {0}\n'.format(tm)        +
                               '-' * 30 + '\n'                +
                               'DNA []: \t\t\t50 nM\n'        +
                               'Monovalent []: \t50 mM\n'     +
                               'Divalent []: \t\t0.01 mM\n'   +
                               'dNTP []: \t\t0 mM')



