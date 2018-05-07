import unittest
from input_parser import pop_single_argument, pop_argument_list, parse_input, parse_file


class TestInputParser(unittest.TestCase):
    def test_pop_single_argument_multiple_arg(self):
        arg, input_str = pop_single_argument('0 1 2 3 4 5')
        self.assertEqual(arg, '0')
        self.assertEqual(input_str, '1 2 3 4 5')

    def test_pop_single_argument_one_arg(self):
        arg, input_str = pop_single_argument('0')
        self.assertEqual(arg, '0')
        self.assertEqual(input_str, '')

    def test_pop_single_argument_no_arg(self):
        arg, input_str = pop_single_argument('')
        self.assertEqual(arg, '')
        self.assertEqual(input_str, '')

    def test_pop_argument_list_multiple_arg(self):
        arg_list, input_str = pop_argument_list('3 florian 1 michael 2 stefan 3', 2)
        self.assertEqual(arg_list, ['florian 1', 'michael 2', 'stefan 3'])
        self.assertEqual(input_str, '')

    def test_pop_argument_list_one_arg(self):
        arg_list, input_str = pop_argument_list('1 florian 1 michael 2 stefan 3', 2)
        self.assertEqual(arg_list, ['florian 1'])
        self.assertEqual(input_str, 'michael 2 stefan 3')

    def test_pop_argument_list_too_less_elems(self):
        with self.assertRaises(ValueError) as context:
            pop_argument_list('10 florian 1 michael 2 stefan 3', 2)

    def test_parse_input(self):
        format = 'N,int [N,ids,1,int]'
        input_str = '10 1 2 3 4 5 6 7 8 9 10'

        expected_result = {'N': 10, 'ids': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

        data = parse_input(input_str, format)

        self.assertEqual(expected_result, data)

    def test_parse_input_2(self):
        format = 'M,int N,str X,int'
        input_str = '1 florian 2'

        expected_result = {'M': 1, 'N': 'florian', 'X': 2}

        data = parse_input(input_str, format)

        self.assertEqual(expected_result, data)

    def test_parse_input_list_with_elem_count_greater_one(self):
        format = 'N,int [N,name_age,2,str]'
        input_str = '2 florian 27 michael 16'

        expected_result = {'N': 2, 'name_age': ['florian 27', 'michael 16']}

        data = parse_input(input_str, format)

        self.assertEqual(expected_result, data)

    def test_parse_input_list_with_floats(self):
        format = 'N,int [N,vals,1,float]'
        input_str = '5 0.1 0.34 1.234 200 0'

        expected_result = {'N':5, 'vals':[0.1, 0.34, 1.234, 200.0, 0.0]}

        data = parse_input(input_str,format)

        self.assertEqual(expected_result,data)

    def test_parse_file(self):
        data = parse_file('resources/input', 'resources/format')

        expected_result = {'N': 10, 'ids': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

        self.assertEqual(expected_result, data)

    def test_parse_file_multi_elem_list(self):
        data = parse_file('resources/input_multi_elem_list', 'resources/format_multi_elem_list')

        expected_result = {'N': 3, 'name_ids': ['flo 1', 'michi 2', 'stefan 3']}
        
        self.assertEqual(expected_result, data)


if __name__ == '__main__':
    unittest.main()
