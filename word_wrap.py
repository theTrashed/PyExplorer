def wrap(text, maxLineLen, maxLineNum=2):
    wrappingChars = ['.', '/', ' ', '_', '-', '&', '\\']
    returnTxt = []

    # Get maxLineNum lines of maxLineLen size from the string. If the substring
    # is empty break out of the loop, as the original string has ended.
    for i in range(maxLineNum):
        returnTxt.append(text[i*maxLineLen:(i+1)*maxLineLen])

    # Extra line appended to avoid indexing errors
    returnTxt.append('')

    if (len(returnTxt) == 2):
        return returnTxt[0]

    for line in returnTxt:
        i = returnTxt.index(line)
        lineLen = len(line)
        if (not (lineLen >= maxLineLen)):
            continue
        for j, c in enumerate(reversed(line)):
            if (c not in wrappingChars):
                continue

            try:
                returnTxt[i+1] = returnTxt[i][lineLen-j:] + returnTxt[i+1]
                returnTxt[i] = returnTxt[i][:lineLen-j]
            except IndexError:
                returnTxt[i] = returnTxt[i][:lineLen-j]
            finally:
                break

        line = returnTxt[i]
        if (len(line) >= maxLineLen):
            for j, c in enumerate(reversed(line)):
                try:
                    if(line[lineLen-(j+1)].isupper() and
                       line[lineLen-(j+2)].islower()):
                        returnTxt[i+1] = returnTxt[i][lineLen-(j+1):] + \
                                        returnTxt[i+1]
                        returnTxt[i] = returnTxt[i][:lineLen-(j+1)]
                        break
                except IndexError:
                    pass

    if (returnTxt[-1] != ''):
        returnTxt[-2] = returnTxt[-2][:maxLineLen-3] + '...'

    return '\n'.join(returnTxt[:maxLineNum])
