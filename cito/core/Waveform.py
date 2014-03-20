"""Perform operations on sets of blocks
"""

import logging
from scipy.sparse import dok_matrix, bsr_matrix, csr_matrix
from cito.core.math import sizeof_fmt
import numpy as np

# Samples are actually 14 bit unsigned, so 16 bit signed fine
SAMPLE_TYPE = np.int16
MAX_ADC_VALUE = 2 ** 14  # 14 bit ADC samples


def get_samples(data):
    # Parse data
    if len(data) > 32000:
        raise ValueError('Data from board larger than memory on board')

    samples = np.frombuffer(data, dtype=SAMPLE_TYPE)

    # Invert pulse so larger energy deposit is larger ADC values
    samples *= -1
    samples += MAX_ADC_VALUE

    return samples


def get_data_and_sum_waveform(cursor, inputdb, t0, t1):
    """Get inverted sum waveform from mongo

    Args:
        cursor (iterable):  An iterable object of documents containing Caen
                           blocks.  This can be a pymongo Cursor.
        inputdb - class


    Returns:
       csr matrix - not dok so can slice
    """
    log = logging.getLogger(__name__)

    size = 0

    shape = (t1 - t0, 256) # 256 pmts

    all_waveforms = csr_matrix(shape, dtype=np.int16)

    for doc in cursor:
        data = inputdb.get_data_from_doc(doc)
        num_channel = doc['channel']
        if doc['module'] != -1:
            num_channel = doc['module'] * 10 + doc['channel']

        size += len(data)

        time_index = doc['time'] - t0

        try:
            samples = get_samples(data)
        except ValueError as e:
            logging.error('Failed to parse document: %s' % str(doc['_id']))
            logging.exception(e)
            continue

        # Compute baseline with first 3 - numpy function slow
        baseline = (samples[0] + samples[1] + samples[2])/3
        samples -= baseline

        y = num_channel * np.ones(samples.size)
        x = np.arange(time_index, time_index + samples.size)
        z = csr_matrix( (samples,(x,y)), shape=shape, dtype=np.int16)

        all_waveforms = all_waveforms + z

    log.debug("Size of data process in bytes: %s", sizeof_fmt(size))

    return all_waveforms, size
