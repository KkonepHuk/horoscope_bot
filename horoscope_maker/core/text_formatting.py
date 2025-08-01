def format(string):
    cnt = 0
    new_strings = []
    tmp_string = ''
    for sym in string:
        cnt += 1
        if cnt > 50 and sym == ' ':
            cnt = 0
            new_strings.append(tmp_string)
            tmp_string = ''
        else:
            tmp_string += sym
            cnt += 1
    new_strings.append(tmp_string)

    return new_strings