DTYPES = {'int': int, 'str': str, 'float': float}


def pop_single_argument(input_str, dtype=str, delimiter=' '):
    '''
    Cut off the first value of an input string and convert it to a given type.

    :param input_str: string of input values, separated by a delimiter character
    :param dtype: type of return value
    :param delimiter: delimiter character that separates the input values
    :return:
    '''
    separator_pos = input_str.find(delimiter)
    if separator_pos == -1:
        return dtype(input_str), ''
    return dtype(input_str[:separator_pos]), input_str[separator_pos + 1:]


def pop_argument_list(input_str, size_of_elem, dtype=str, count=-1, delimiter=''):
    '''
    Cut off several values from an input string and return it as a list of a given type.
    If the parameter count is not defined, it is assumed, that the first value defines the
    number of elements in the list.

    :param input_str: string of input values, separated by a delimiter character
    :param size_of_elem: number of values per element
    :param dtype: type of return values
    :param count: number of list elements
    :param delimiter: delimiter character that separates the input values
    :return: A list of values
    '''
    if count == -1:
        elem_count, input_str = pop_single_argument(input_str)
        elem_count = int(elem_count)
    else:
        elem_count = count

    arg_list = []

    for elem_index in range(0, elem_count):
        elem = ''
        for attr_index in range(0, size_of_elem):
            if input_str is '':
                raise ValueError(
                    "The input string does not provide enough elements to read a list of {0} elements".format(
                        elem_count))
            attr, input_str = pop_single_argument(input_str)
            elem += attr
            if attr_index != size_of_elem - 1:
                elem += ' '

        arg_list.append(dtype(elem))

    return arg_list, input_str


def parse_input(input_str, format):
    '''
    This method extracts data out of a input string. The Format of the input string is defined via the format string.
    Single Values are just defined as [name],[datatype] (e.g. N,int). Lists can be defined with brackets in following format:
    [elem_count,list_name,elem_size,dtype] (e.g. [N,ids,1,int] -> A List with N elements, that is saved in the data dict
    with key 'list_name'. Every element of the list consists of 'elem_size' elements and every element is going to be converted
    to the defined dtype.

    :param input_str: input string, containing the data to extract
    :param format:  description of the input string format
    :return: data dictionary, containing all data of the input string
    '''
    data = dict()

    while input_str != '':
        format_instruction, format = pop_single_argument(format)

        if format_instruction.startswith('[') and format_instruction.endswith(']'):
            list_params = format_instruction[1:-1].split(',')
            list_count = data[list_params[0]]
            list_name = list_params[1]
            list_elem_size = int(list_params[2])
            dtype = DTYPES[list_params[3]]

            list, input_str = pop_argument_list(input_str, list_elem_size, dtype=dtype, count=list_count)
            data[list_name] = list
        else:
            val_params = format_instruction.split(',')
            dtype = DTYPES[val_params[1]]
            data[val_params[0]], input_str = pop_single_argument(input_str, dtype=dtype)

    return data


def parse_file(input_file, format_file):
    '''
    This method extracts data out of a input_file. The format of the input_file is described in the format_file.
    Format Syntax is similar to the parse_input method. Additionally it is possible to define lists, where all elements
    are separated by \n. The syntax is: {list_count,list_name,list_elem_size,dtype}
    :param input_file: file, containing the data to extract
    :param format_file: file, that defines the format of the input file
    :return: data dictionary, containing the data of the input file
    '''
    with open(input_file, 'r') as i_file:
        with open(format_file, 'r') as f_file:
            data = dict()
            format_line = f_file.readline()
            while format_line != '':
                if format_line.startswith('{') and format_line.endswith('}'):
                    list_params = format_line[1:-1].split(',')
                    list_count = data[list_params[0]]
                    list_name = list_params[1]
                    list_elem_size = int(list_params[2])

                    if list_params[3].endswith('\n'):
                        list_params[3] = list_params[3][:-1]

                    dtype = DTYPES[list_params[3]]

                    list = []
                    for i in range(0, list_count):
                        input_line = i_file.readline()

                        if input_line.endswith('\n'):
                            input_line = input_line[:-1]
                        val = dtype(input_line)
                        list.append(val)

                    data[list_name] = list
                else:
                    input_line = i_file.readline()
                    if input_line.endswith('\n'):
                        input_line = input_line[:-1]
                    if format_line.endswith('\n'):
                        format_line = format_line[:-1]
                    result = parse_input(input_line, format_line)
                    data = {**data, **result}

                format_line = f_file.readline()

            return data
