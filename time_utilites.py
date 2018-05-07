def time_diff(start,end):
    '''
    Calculate the difference between a start and end time, both given in the format 'hh:mm:ss'
    :param start: start time
    :param end: end time
    :return: difference in seconds
    '''

    start_split = start.split(':')
    end_split = end.split(':')

    start_sec = int(start_split[0])*60*60 + int(start_split[1])*60 + int(start_split[2])
    end_sec = int(end_split[0])*60*60 + int(end_split[1])*60 + int(end_split[2])

    diff = end_sec - start_sec

    return abs(diff)