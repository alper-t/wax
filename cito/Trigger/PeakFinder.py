"""Find a peak in sum waveform

Given a list of ADC sample values, the peaks are found.   There are two
functions defined in this class.  The first is:

 identify_nonoverlapping_trigger_windows

which is allows the peak finder to run on multiple spacially seperate trigger
 windows at once.  The actual logic of the peak finder is in:

 find_peaks

where, for example, filtering and identification of ridge lines is performed.
"""

__author__ = 'tunnell'

import logging
import time

import numpy as np
from cito.core.math import find_subranges

MAX_DRIFT = 18000  # units of 10 ns


def find_peaks(values, threshold=1000, ):
    """Find peaks within list of values.


    Args:
        values (sparse matrix):  The 'y' values to find a peak in.
        threshold (int): Threshold in ADC counts required for peaks.

    Returns:
       np.array: Array of peak indices

    """

    # 20 is the wavelet width
    logging.debug('Peak finding with n=%d' % values.size)
    t0 = time.time()
    values_above_threshold = np.where(values > threshold)[0].tolist()
    #values_above_threshold.todense()[0]
    logging.error(values_above_threshold)
    logging.error(type(values_above_threshold))
    # Center of the range above threshold.
    peaks = []
    for a, b in find_subranges(values_above_threshold):
        logging.error(values_above_threshold[b])
        peaks.append(np.round(float(a + b) / 2))

    t1 = time.time()

    logging.debug('Filtering duration: %f s' % (t1 - t0))
    return np.array(peaks, dtype=np.int32)
