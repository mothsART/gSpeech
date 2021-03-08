def concat_list(_list):
    value = ''
    for indice, speed in enumerate(_list):
        if indice == 0:
            value += ' %s' % str(speed)
            continue
        value += ', %s' % str(speed)
    return value
