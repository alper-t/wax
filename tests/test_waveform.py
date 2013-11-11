#!/usr/bin/env python

import unittest

import numpy as np
from cito.helpers import waveform

class Test_split_boolean_array(unittest.TestCase):
    def setUp(self):
        self.answer = {}
        self.answer[(True, True, True)] = [(0, 3)]
        self.answer[(True, True, False)] = [(0, 2)]
        self.answer[(True, False, True)] = [(0, 1), (2, 3)]
        self.answer[(True, False, False)] = [(0, 1)]
        self.answer[(False, True, True)] = [(1, 3)]
        self.answer[(False, True, False)] = [(1, 2)]
        self.answer[(False, False, True)] = [(2, 3)]
        self.answer[(False, False, False)] = []

    def test_length3(self):
        f = waveform.split_boolean_array
        for i in [True, False]:
            for j in [True, False]:
                for k in [True, False]:
                    self.assertEqual(f(np.array((i,j,k), dtype=np.bool)),
                                     self.answer[(i,j,k)])

    def test_length6(self):
        f = waveform.split_boolean_array
        for i in [True, False]:
            for j in [True, False]:
                for k in [True, False]:
                    new_answer = [(2*a, 2*b) for a, b in self.answer[(i,j,k)]]
                    self.assertEqual(f(np.array((i,i,j,j,k,k), dtype=np.bool)),
                                     new_answer)






class Test_save_time_range(unittest.TestCase):
    def setUp(self):
        self.single = [False, False,  True,  True,  True,  True,  True,  True, False, False]
        self.range_around_trigger = (-3, 3)


    def test_single_peak_int(self):
        x = waveform.get_index_mask_for_trigger(10, 5, self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_single_peak_list(self):
        x = waveform.get_index_mask_for_trigger(10, 5, self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_multi_peak_list_no_overlap(self):
        x = waveform.get_index_mask_for_trigger(10, [2, 9], self.range_around_trigger).tolist()
        self.assertEqual([True, True, True, True, True, False, True, True, True, True],
                         x)
    def test_multi_peak_list_overlap(self):
        x = waveform.get_index_mask_for_trigger(10, [5, 15], self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_overrun(self):
        x = waveform.get_index_mask_for_trigger(10, [0], self.range_around_trigger).tolist()
        self.assertEqual([True, True, True, False, False, False, False, False, False, False],
                         x)

    def test_single_peak_float_exception(self):
         with self.assertRaises(ValueError):
            waveform.get_index_mask_for_trigger(10, 5.0, self.range_around_trigger)

    def test_size_not_int(self):
         with self.assertRaises(ValueError):
            waveform.get_index_mask_for_trigger([10], 5, self.range_around_trigger)

class Test_save_time_range(unittest.TestCase):
    def setUp(self):
        self.single = [False, False,  True,  True,  True,  True,  True,  True, False, False]
        self.range_around_trigger = (-3, 3)


    def test_single_peak_int(self):
        x = waveform.get_index_mask_for_trigger(10, 5, self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_single_peak_list(self):
        x = waveform.get_index_mask_for_trigger(10, 5, self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_multi_peak_list_no_overlap(self):
        x = waveform.get_index_mask_for_trigger(10, [2, 9], self.range_around_trigger).tolist()
        self.assertEqual([True, True, True, True, True, False, True, True, True, True],
                         x)
    def test_multi_peak_list_overlap(self):
        x = waveform.get_index_mask_for_trigger(10, [5, 15], self.range_around_trigger).tolist()
        self.assertEqual(self.single,
                         x)

    def test_overrun(self):
        x = waveform.get_index_mask_for_trigger(10, [0], self.range_around_trigger).tolist()
        self.assertEqual([True, True, True, False, False, False, False, False, False, False],
                         x)

    def test_single_peak_float_exception(self):
         with self.assertRaises(ValueError):
            waveform.get_index_mask_for_trigger(10, 5.0, self.range_around_trigger)

    def test_size_not_int(self):
         with self.assertRaises(ValueError):
            waveform.get_index_mask_for_trigger([10], 5, self.range_around_trigger)


class Test_get_sum_waveform(unittest.TestCase):
    def _testGoodDocs(self):
        #  Not nice to include raw data in a file, but this ensures the test and raw data are in sync.
        #  This data is already unzipped
        docs = []

        docs.append({'zipped': True,
                     'data': b'\x90\t\x88$\x01\x00\xa0\xff\x00\x00\x01\x00\x00\x16\x00\xa2\xf0B\xe8$\x00\x00\x00\x7f\x00\x00\x00!\x00\x00\x80\x81>\x81>\x82>\x82\r\x06\x01\n\x0c\x82>\x83>\x01\x16\x01\x04\x08\x80>\x83\x05\x14\x08\x81>\x83\x05\x02(\x80>\x82>\x85>\x81>\x84>\x84\x05\x18\x01\x10\x014\x01D\x01*\x00\x83\x05\x18\x01\x16\x01\x12\x00\x80\x05\n\x88\x82>{:\xd8)g%\xa8$\x87$\x7f$v$t$A5\xe0<L>|>\x81>\x85>\x84>\x83>$\x1d\x90\x18\x80>~>\x81>\x80\r~\x01\x0e\x00\x82\x05\x10\x04\x7f>\x01N\x11\x18\x08\x81>\x7f\x05\x18\x11*\x08\x82>~\x05 \x10\x82>\x80>\x7f\x05<\t\x1a\x014\x01\x14\x01\x1e\x01\xd0\x01\x16h\x7f>\x05:\xc1)\x81%\xcc$\xad$\xa2$\x99$\x9f$\x995\xea<H>y>~\x05f\x00\x7f:\x90\x00\x01R\x01\x88\x00\x7f\x05F\x01\x0e\x01\xa2\x01\x90\x010\x00}\r\n\x01\x0c\x01\x04\x10\x7f>\x7f>|\x05\x14\x01\n\x01&\x01\x04\x01\x80\x01\x04\x10\x80>}>}\x05(\x01\x0e\x01\x1a\x01&XS:\xcb)Z%\x9e$}$q$h$g$G5\xda<K>|\x05\xe2\x01\xf2.\xb0\x01\x00\x82%b!^!p!|!\xae)x\x11\x06\x01\x16\x01\xea)\xb4\x01\x06!f\x01\x04\x014!\xbc\x08\x85>\x85%\xe8\x01\x1c\t\x04\tX)\xd6X\x90:\xe8)n%\xae$\x90$\x84${$t$;5\xdc<K>}\x05>\x01\\.\x90\x00!\x16.\x04\x01\x01\xde!\x08\x01\x14\x00\x7f\x05\x0e\t\x12\x01\x06\x00}%\x1a\x01\x1a!\x06\x01\x04!\x06\x00~\r\x02\t\x10\x00{\r*\x01&!\xe6\x01\x08X|:%){$\xb3#\x91#\x84#{#n#_4\xad<A>x-\x966\xb0\x01\x01\x90\x01R!\\!<\x01\x84!d\x00\x80\x05\x16!\xbeA \x01\x12A\x10\x01\x10\x01\xae\x01.\x01\x08\x01\x90\x19*A>\x01\x04\x08\x81>~\x05\x88\x01&\x01\x10X\x80:\xa6)-%o$N$A$9$.$\xea4\xce<I>z\x05\x1c\x01\x80. \x01\x00\x85%`!n)\\a^!\x86I\xfa\x01\x0e\x00\x84\x05\xa8\x01\x8e!\\\x01\x12\x01 !\x96!\x94!\xae\x01\x0ca\x82\x01\x10\x01\x0c!\xe8\x00\x85m\\\x01\x10XQ:\x04)z$\xbd#\x9c#\x91#\x86#}#\xa54\xc3<H>}e\xac\x01,.\x90\x00(\x87>\x87>\x89>\x86>\x87>\x88\x05\x04\x00\x89\x05\x08\x08\x8a>\x88\x05\x02\x0c\x89>\x89>\x01"\x08\x86>\x88\x05\x0c\x01\x16\t*\x11\x12\x01"\x01\x04\x01&\x01\x1a\x01(\x01J\x01\x14\x9c\x89>\x8a>\x86>\x89>\xbd:\xbf)6%u$S$G$>$3$\xd24\xd0<O>\x82>\x86>\x89>\x88>\x89>',
                     'triggertime': 3896701090, 'module': 770, 'datalength': 727})
        docs.append({'zipped': True,
                     'data': b'\x90\t\x88$\x01\x00\xa0\xff\x00\x00\x01\x00\x00\x16\x00\xa2\xf0B\xe8$\x00\x00\x00\x7f\x00\x00\x00!\x00\x00\x80\x81>\x81>\x82>\x82\r\x06\x01\n\x0c\x82>\x83>\x01\x16\x01\x04\x08\x80>\x83\x05\x14\x08\x81>\x83\x05\x02(\x80>\x82>\x85>\x81>\x84>\x84\x05\x18\x01\x10\x014\x01D\x01*\x00\x83\x05\x18\x01\x16\x01\x12\x00\x80\x05\n\x88\x82>{:\xd8)g%\xa8$\x87$\x7f$v$t$A5\xe0<L>|>\x81>\x85>\x84>\x83>$\x1d\x90\x18\x80>~>\x81>\x80\r~\x01\x0e\x00\x82\x05\x10\x04\x7f>\x01N\x11\x18\x08\x81>\x7f\x05\x18\x11*\x08\x82>~\x05 \x10\x82>\x80>\x7f\x05<\t\x1a\x014\x01\x14\x01\x1e\x01\xd0\x01\x16h\x7f>\x05:\xc1)\x81%\xcc$\xad$\xa2$\x99$\x9f$\x995\xea<H>y>~\x05f\x00\x7f:\x90\x00\x01R\x01\x88\x00\x7f\x05F\x01\x0e\x01\xa2\x01\x90\x010\x00}\r\n\x01\x0c\x01\x04\x10\x7f>\x7f>|\x05\x14\x01\n\x01&\x01\x04\x01\x80\x01\x04\x10\x80>}>}\x05(\x01\x0e\x01\x1a\x01&XS:\xcb)Z%\x9e$}$q$h$g$G5\xda<K>|\x05\xe2\x01\xf2.\xb0\x01\x00\x82%b!^!p!|!\xae)x\x11\x06\x01\x16\x01\xea)\xb4\x01\x06!f\x01\x04\x014!\xbc\x08\x85>\x85%\xe8\x01\x1c\t\x04\tX)\xd6X\x90:\xe8)n%\xae$\x90$\x84${$t$;5\xdc<K>}\x05>\x01\\.\x90\x00!\x16.\x04\x01\x01\xde!\x08\x01\x14\x00\x7f\x05\x0e\t\x12\x01\x06\x00}%\x1a\x01\x1a!\x06\x01\x04!\x06\x00~\r\x02\t\x10\x00{\r*\x01&!\xe6\x01\x08X|:%){$\xb3#\x91#\x84#{#n#_4\xad<A>x-\x966\xb0\x01\x01\x90\x01R!\\!<\x01\x84!d\x00\x80\x05\x16!\xbeA \x01\x12A\x10\x01\x10\x01\xae\x01.\x01\x08\x01\x90\x19*A>\x01\x04\x08\x81>~\x05\x88\x01&\x01\x10X\x80:\xa6)-%o$N$A$9$.$\xea4\xce<I>z\x05\x1c\x01\x80. \x01\x00\x85%`!n)\\a^!\x86I\xfa\x01\x0e\x00\x84\x05\xa8\x01\x8e!\\\x01\x12\x01 !\x96!\x94!\xae\x01\x0ca\x82\x01\x10\x01\x0c!\xe8\x00\x85m\\\x01\x10XQ:\x04)z$\xbd#\x9c#\x91#\x86#}#\xa54\xc3<H>}e\xac\x01,.\x90\x00(\x87>\x87>\x89>\x86>\x87>\x88\x05\x04\x00\x89\x05\x08\x08\x8a>\x88\x05\x02\x0c\x89>\x89>\x01"\x08\x86>\x88\x05\x0c\x01\x16\t*\x11\x12\x01"\x01\x04\x01&\x01\x1a\x01(\x01J\x01\x14\x9c\x89>\x8a>\x86>\x89>\xbd:\xbf)6%u$S$G$>$3$\xd24\xd0<O>\x82>\x86>\x89>\x88>\x89>',
                     'triggertime': 3896701090, 'module': 770, 'datalength': 727})
        docs.append({'zipped': True,
                     'data': b'\x90\t\x88$\x01\x00\xa0\xff\x00\x00\x01\x00\x00\x16\x00\xa2\xf0B\xe8$\x00\x00\x00\x7f\x00\x00\x00!\x00\x00\x80\x81>\x81>\x82>\x82\r\x06\x01\n\x0c\x82>\x83>\x01\x16\x01\x04\x08\x80>\x83\x05\x14\x08\x81>\x83\x05\x02(\x80>\x82>\x85>\x81>\x84>\x84\x05\x18\x01\x10\x014\x01D\x01*\x00\x83\x05\x18\x01\x16\x01\x12\x00\x80\x05\n\x88\x82>{:\xd8)g%\xa8$\x87$\x7f$v$t$A5\xe0<L>|>\x81>\x85>\x84>\x83>$\x1d\x90\x18\x80>~>\x81>\x80\r~\x01\x0e\x00\x82\x05\x10\x04\x7f>\x01N\x11\x18\x08\x81>\x7f\x05\x18\x11*\x08\x82>~\x05 \x10\x82>\x80>\x7f\x05<\t\x1a\x014\x01\x14\x01\x1e\x01\xd0\x01\x16h\x7f>\x05:\xc1)\x81%\xcc$\xad$\xa2$\x99$\x9f$\x995\xea<H>y>~\x05f\x00\x7f:\x90\x00\x01R\x01\x88\x00\x7f\x05F\x01\x0e\x01\xa2\x01\x90\x010\x00}\r\n\x01\x0c\x01\x04\x10\x7f>\x7f>|\x05\x14\x01\n\x01&\x01\x04\x01\x80\x01\x04\x10\x80>}>}\x05(\x01\x0e\x01\x1a\x01&XS:\xcb)Z%\x9e$}$q$h$g$G5\xda<K>|\x05\xe2\x01\xf2.\xb0\x01\x00\x82%b!^!p!|!\xae)x\x11\x06\x01\x16\x01\xea)\xb4\x01\x06!f\x01\x04\x014!\xbc\x08\x85>\x85%\xe8\x01\x1c\t\x04\tX)\xd6X\x90:\xe8)n%\xae$\x90$\x84${$t$;5\xdc<K>}\x05>\x01\\.\x90\x00!\x16.\x04\x01\x01\xde!\x08\x01\x14\x00\x7f\x05\x0e\t\x12\x01\x06\x00}%\x1a\x01\x1a!\x06\x01\x04!\x06\x00~\r\x02\t\x10\x00{\r*\x01&!\xe6\x01\x08X|:%){$\xb3#\x91#\x84#{#n#_4\xad<A>x-\x966\xb0\x01\x01\x90\x01R!\\!<\x01\x84!d\x00\x80\x05\x16!\xbeA \x01\x12A\x10\x01\x10\x01\xae\x01.\x01\x08\x01\x90\x19*A>\x01\x04\x08\x81>~\x05\x88\x01&\x01\x10X\x80:\xa6)-%o$N$A$9$.$\xea4\xce<I>z\x05\x1c\x01\x80. \x01\x00\x85%`!n)\\a^!\x86I\xfa\x01\x0e\x00\x84\x05\xa8\x01\x8e!\\\x01\x12\x01 !\x96!\x94!\xae\x01\x0ca\x82\x01\x10\x01\x0c!\xe8\x00\x85m\\\x01\x10XQ:\x04)z$\xbd#\x9c#\x91#\x86#}#\xa54\xc3<H>}e\xac\x01,.\x90\x00(\x87>\x87>\x89>\x86>\x87>\x88\x05\x04\x00\x89\x05\x08\x08\x8a>\x88\x05\x02\x0c\x89>\x89>\x01"\x08\x86>\x88\x05\x0c\x01\x16\t*\x11\x12\x01"\x01\x04\x01&\x01\x1a\x01(\x01J\x01\x14\x9c\x89>\x8a>\x86>\x89>\xbd:\xbf)6%u$S$G$>$3$\xd24\xd0<O>\x82>\x86>\x89>\x88>\x89>',
                     'triggertime': 3896701090, 'module': 770, 'datalength': 727})
        docs.append({'zipped': True,
                     'data': b'\x90\t\x88$\x01\x00\xa0\xff\x00\x00\x01\x00\x00\x16\x00\xa2\xf0B\xe8$\x00\x00\x00\x7f\x00\x00\x00!\x00\x00\x80\x81>\x81>\x82>\x82\r\x06\x01\n\x0c\x82>\x83>\x01\x16\x01\x04\x08\x80>\x83\x05\x14\x08\x81>\x83\x05\x02(\x80>\x82>\x85>\x81>\x84>\x84\x05\x18\x01\x10\x014\x01D\x01*\x00\x83\x05\x18\x01\x16\x01\x12\x00\x80\x05\n\x88\x82>{:\xd8)g%\xa8$\x87$\x7f$v$t$A5\xe0<L>|>\x81>\x85>\x84>\x83>$\x1d\x90\x18\x80>~>\x81>\x80\r~\x01\x0e\x00\x82\x05\x10\x04\x7f>\x01N\x11\x18\x08\x81>\x7f\x05\x18\x11*\x08\x82>~\x05 \x10\x82>\x80>\x7f\x05<\t\x1a\x014\x01\x14\x01\x1e\x01\xd0\x01\x16h\x7f>\x05:\xc1)\x81%\xcc$\xad$\xa2$\x99$\x9f$\x995\xea<H>y>~\x05f\x00\x7f:\x90\x00\x01R\x01\x88\x00\x7f\x05F\x01\x0e\x01\xa2\x01\x90\x010\x00}\r\n\x01\x0c\x01\x04\x10\x7f>\x7f>|\x05\x14\x01\n\x01&\x01\x04\x01\x80\x01\x04\x10\x80>}>}\x05(\x01\x0e\x01\x1a\x01&XS:\xcb)Z%\x9e$}$q$h$g$G5\xda<K>|\x05\xe2\x01\xf2.\xb0\x01\x00\x82%b!^!p!|!\xae)x\x11\x06\x01\x16\x01\xea)\xb4\x01\x06!f\x01\x04\x014!\xbc\x08\x85>\x85%\xe8\x01\x1c\t\x04\tX)\xd6X\x90:\xe8)n%\xae$\x90$\x84${$t$;5\xdc<K>}\x05>\x01\\.\x90\x00!\x16.\x04\x01\x01\xde!\x08\x01\x14\x00\x7f\x05\x0e\t\x12\x01\x06\x00}%\x1a\x01\x1a!\x06\x01\x04!\x06\x00~\r\x02\t\x10\x00{\r*\x01&!\xe6\x01\x08X|:%){$\xb3#\x91#\x84#{#n#_4\xad<A>x-\x966\xb0\x01\x01\x90\x01R!\\!<\x01\x84!d\x00\x80\x05\x16!\xbeA \x01\x12A\x10\x01\x10\x01\xae\x01.\x01\x08\x01\x90\x19*A>\x01\x04\x08\x81>~\x05\x88\x01&\x01\x10X\x80:\xa6)-%o$N$A$9$.$\xea4\xce<I>z\x05\x1c\x01\x80. \x01\x00\x85%`!n)\\a^!\x86I\xfa\x01\x0e\x00\x84\x05\xa8\x01\x8e!\\\x01\x12\x01 !\x96!\x94!\xae\x01\x0ca\x82\x01\x10\x01\x0c!\xe8\x00\x85m\\\x01\x10XQ:\x04)z$\xbd#\x9c#\x91#\x86#}#\xa54\xc3<H>}e\xac\x01,.\x90\x00(\x87>\x87>\x89>\x86>\x87>\x88\x05\x04\x00\x89\x05\x08\x08\x8a>\x88\x05\x02\x0c\x89>\x89>\x01"\x08\x86>\x88\x05\x0c\x01\x16\t*\x11\x12\x01"\x01\x04\x01&\x01\x1a\x01(\x01J\x01\x14\x9c\x89>\x8a>\x86>\x89>\xbd:\xbf)6%u$S$G$>$3$\xd24\xd0<O>\x82>\x86>\x89>\x88>\x89>',
                     'triggertime': 3896701090, 'module': 770, 'datalength': 727})

        return docs

    def setUp(self):
        self.size = 1400
        self.result = waveform.get_data_and_sum_waveform(self._testGoodDocs(),
                                                 3896701090,
                                                 self.size)

    def test_get_sum_waveform_nonzero(self):
        self.assertNotAlmostEqual(np.sum(self.result['indecies']), # sample
                                  0)
        self.assertNotAlmostEqual(np.sum(self.result['samples']), # indec
                                  0)

    def test_get_sum_waveform_size(self):
        self.assertEqual(self.result['size'], 4672)

    def test_get_sum_waveform_positive_size(self):
        self.assertGreater(self.result['size'], 0)


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
