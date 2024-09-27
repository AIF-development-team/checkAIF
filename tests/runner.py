# -*- coding: utf-8 -*-
# pylint: disable-msg=invalid-name   #because I use snake_case
# pylint: disable-msg=wrong-import-position
"""Unit Tests for checkAIF"""
import sys
import os
import unittest

# Update path / fix when checkAIF is packaged for distribution
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))
import checkAIF  #pylint: disable-msg=import-error

# Use local AIF definitions
AIF_definition = 'aifdictionary.json'


class Test_checkAIF(unittest.TestCase):
    """
    Describe Test; what AIF errors this file is intended to  create.
    """

    # def test_sample_AIF0(self):
    #     input_file = "./input0.aif"
    #     expected_output = open("./output0","r").read()
    #     output = run(input_file, AIF_definition)

    #     #print('actual output:')
    #     #print(output)
    #     #print()
    #     #print('expected output:')
    #     #print(expected_output)
    #     #print()

    #     self.assertEqual(
    #         expected_output,
    #         output,
    #         "Output does not match expected"
    #     )

    def test_AIF0(self):
        """
        Test should create all following errors
        """
        input_file = './examples/NK_DUT-6_LP_N2_114PKT.aif'
        with open('./outputs/output0.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())

        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF1(self):
        """
        Test should create an error if a keyvalue has an incorrect datatype
        when compared to the json dictionary
        """
        input_file = './examples/NK_DUT_Error1.aif'
        with open('./outputs/output1.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF2(self):
        """
        Wrong date format
        """
        input_file = './examples/NK_DUT_Error2.aif'
        with open('./outputs/output2.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF3(self):
        """
        Test should create an error if loop has non-float data
        """
        input_file = './examples/NK_DUT_Error3.aif'
        with open('./outputs/output3.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF4(self):
        """
        Fake keyname/keyvalue pair, no units
        """
        input_file = './examples/NK_DUT_Error4.aif'
        with open('./outputs/output4.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF5(self):
        """
        Fake keyname/keyvalue pair, connected units
        """
        input_file = './examples/NK_DUT_Error5.aif'
        with open('./outputs/output5.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF6(self):
        """
        Missing dependent unit
        """
        input_file = './examples/NK_DUT_Error6.aif'
        with open('./outputs/output6.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF7(self):
        """
        Missing required keyname
        """
        input_file = './examples/NK_DUT_Error7.aif'
        with open('./outputs/output7.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')

    def test_AIF8(self):
        """
        Grouped loop names dont match
        """
        input_file = './examples/NK_DUT_Error8.aif'
        with open('./outputs/output8.txt', 'r', encoding='utf-8') as handle:
            expected_output = sorted(handle.read().splitlines())
        output = checkAIF.inspect_AIF(input_file, AIF_definition)
        output = sorted(output.splitlines())

        self.assertEqual(expected_output, output,
                         'Output does not match expected')
        print('Success')


if __name__ == '__main__':
    unittest.main(verbosity=2)
