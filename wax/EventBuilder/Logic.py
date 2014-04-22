# -*- coding: utf-8 -*-

"""
    wax.core.EventBuilding
    ~~~~~~~~~~~~~~~~~~~~~~~

    Event building converts time blocks of data (from different digitizer boards) into DAQ events.

    Event building (see jargon) occurs by taking all the data from all the boards recorded during a time window and,
    using some trigger logic, identifying independent events within this time window.  An EventBuilder class is defined
    that performs the following sequential operations:

    * Build sum waveform
    * Using trigger algorithm, identify peaks in time.
    * If there is no pileup (read further for pileup details), an event corresponds to a predefined time range before
      and after each peak.

    More technically about pileup, if two particles interact in the detector within a typical 'event window', then
    these two interactions are saved as one event.  Identifying how to break up the event is thus left for
    postprocessing.  For example, for peak_k > peak_i, if peak_i + t_post > peak_k - t_pre, these are one event.
"""
import logging

import numpy as np

from wax.Trigger import PeakFinder
from wax.core.math import compute_subranges


def find_sum_in_data(data):
    """Find sum waveform in channel data


    :param data: Initial time to query.
    :type data: dict.
    :returns:  dict -- Sum waveform indices and samples.
    :raises: ValueError
    """
    for key, value in data.items():
        start, stop, pmt_num = key
        if pmt_num == 'sum':
            sum0, sum1 = value['indices'][0], value['indices'][-1]
            logging.debug('Sum waveform range: [%d, %d]', sum0, sum1)
            return value

    raise ValueError("Sum waveform not found")


class EventBuilder():

    """From data, construct events

    This is a separate class since it has to keep track of event number"""

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_number = None

    def get_event_number(self):
        if self.event_number is None:
            self.event_number = 0
            return self.event_number
        else:
            self.event_number += 1
            return self.event_number

    def build_event(self, data, t0, t1, padding):
        """Build events out of raw data.

        Using the sum waveform provided as an input, distinct events are identified.
        Subsequently, all of the relevant individual channel PMT information (also
        an input) is saved for that specific event.

        :param data: Data to query, including sum waveform and individual channels
        :type data: dict.
        :param t0: Earliest possible time for sanity checks.  If None, skip check.
        :type t0: int.
        :param t1: Latest possible time for sanity checks.  If None, skip check.
        :type t1: int.
        :returns:  dict -- Sum waveform indices and samples.
        :raises: ValueError
        """
        ##
        # Step 1: Grab sum waveform:  this sum waveform will be used to identify S2 signals
        ##
        # sum0, sum1, time ranges
        sum_data = find_sum_in_data(data)

        ##
        # Step 2: Identify peaks in sum waveform using a Trigger algorithm
        ##
        peak_indices, smooth_waveform = PeakFinder.identify_nonoverlapping_trigger_windows(sum_data['indices'],
                                                                                           sum_data['samples'])
        if len(peak_indices) == 0:  # If no peaks found, return
            self.log.info("No peak found; returning")
            return []
        peaks = sum_data['indices'][peak_indices]
        for peak in peaks:  # Check peak in sum waveform
            assert sum_data['indices'][0] <= peak <= sum_data['indices'][-1]
        self.log.debug('Peak indices: %s', str(peaks))
        self.log.debug('Peak local indices: %s', str(peak_indices))
        self.log.debug("Peaks found: %s" % str(peaks))

        ##
        # Step 3: Flag ranges around peaks to save, then break into events
        ##
        event_ranges = compute_subranges(peaks)
        self.log.debug('%d trigger events from %d peaks',
                       len(event_ranges),
                       len(peak_indices))

        data[(0, 0, 'smooth')] = {'indices': sum_data['indices'],
                                  'samples': smooth_waveform}

        ##
        # Step 4: For each trigger event, associate channel information
        ##
        events = []
        # e0, e1 are the times for this trigger event
        for e0, e1 in event_ranges:
            #  This information will be saved about the trigger event
            to_save = {'data': {}}

            # Logic to deal with overlapping region
            if e1 > t1:
                if e0 < t1 - padding:
                    self.log.error("Event bigger than overlap region.  Flagging 1 second of deadtime.")
                    to_save['peaks'] = [peak for peak in peaks if e0 < peak < e1]
                    to_save['evt_num'] = "deadtime"
                    to_save['error'] = "Event range [%d, %d] greater than overlap window!" % (e0, e1)
                    to_save['range'] = [int(e0 - 5e7), int(e1 + 5e7)]
                    events.append(to_save)
                continue
            if e0 < t0 + padding:
                continue

            evt_num = self.get_event_number()
            self.log.debug('\tEvent %d: [%d, %d]', evt_num, e0, e1)

            # If there data within our search range [e0, e1]?
            for key, value in data.items():
                pmt_num = key[2]

                if e1 < value['indices'][0] or value['indices'][-1] < e0:
                    continue
                elif e0 <= value['indices'][0] and value['indices'][-1] <= e1:
                    indices_to_save = value['indices']
                    samples_to_save = value['samples']
                else:
                    mask = (e0 < value['indices']) & (value['indices'] < e1)

                    if not mask.any():
                        continue

                    indices_to_save = value['indices'].compress(mask)
                    samples_to_save = value['samples'].compress(mask)

                # Existing data that needs to be added?
                if pmt_num in to_save['data']:
                    indices_already_saved = to_save['data'][pmt_num]['indices']
                    samples_already_saved = to_save['data'][pmt_num]['samples']
                    indices_to_save = np.concatenate((indices_to_save,
                                                      indices_already_saved))
                    samples_to_save = np.concatenate((samples_to_save,
                                                      samples_already_saved))

                to_save['data'][pmt_num] = {'indices': indices_to_save,
                                            'samples': samples_to_save}

            to_save['peaks'] = [peak for peak in peaks if e0 < peak < e1]

            to_save['evt_num'] = evt_num
            to_save['range'] = [int(e0), int(e1)]
            events.append(to_save)

        return events


if __name__ == '__main__':
    import sys
    from wax.core.main import CitoApp

    myapp = CitoApp()
    import cProfile

    cProfile.run("""myapp.run(['process', '-q', '--chunks', '2'])""",
                 'profile')

    sys.exit(0)