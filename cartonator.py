# Print random cards for Bingo, optionally excluding a 'number' or always
# including it
# Pablo Martin <pablo@odkq.com>, 2014
# This is distributed with the GPL license, see LICENSE file for details
import random
import sys
import argparse

def get_empty_carton():
    ''' Return a 9x3 array with None or 0 where a space is placed '''
    position = []
    for i in range(10):
        position.append([])
        for j in range(3):
            position[i].append(None)
    # Set 9 zeroes
    for i in range(10):
        position[i][random.randint(0, 2)] = 0
    # Set another 3 zeroes
    xbase = range(10)
    for i in range(3):
        x = random.choice(xbase)
        del xbase[xbase.index(x)]
        ybase = range(3)
        # Remove already filled positions before extracting a random one
        for j in range(3):
            if position[x][j] == 0:
                del ybase[j]
        y = random.choice(ybase)
        position[x][y] = 0
    return position

def get_carton(excluded=0, included=0):
    ''' Return a 9x3 array with bingo numbers, 0 means 'space' '''
    position = get_empty_carton()
    for i in range(10):
        ypositions = []
        for j in range(3):
            if position[i][j] is None:
                ypositions.append(j)
        choices = range(10)
        extracted = []
        for turn in range(len(ypositions)):
            if included != 0:
                e = included - (i * 10)
                if ((e >= 0) and (e < 10)):
                    del choices[choices.index(e)]
                    extracted.append(included)
                    included = 0
                    continue
            while True:
                e = random.choice(choices)
                number = e + (i * 10)
                del choices[choices.index(e)]
                if number == excluded:
                    continue
                else:
                    break
            extracted.append(number)
        extracted = sorted(extracted)
        for j in range(len(ypositions)):
            y = ypositions[j]
            e = extracted[j]
            position[i][y] = e
    return position

def draw_line(fd, x0, y0, x1, y1):
    fd.write('{} {} moveto\n'.format(x0, y0))
    fd.write('{} {} lineto\n'.format(x1, y1))

def draw_text(fd, x, y, s):
    fd.write('/Times-Roman findfont\n')
    fd.write('34 scalefont\n')
    fd.write('setfont\n')
    # fd.write('newpath\n')
    fd.write('{} {} moveto\n'.format(x + 9, y + 14))
    fd.write('(' + s + ') show\n')

def draw_number(fd, x0, y0, x, y, n):
    if n != 0:
        px = x * 50 + x0
        py = y * 50 + y0
        draw_text(fd, px, py, str(n))

def draw_carton(fd, x, y, board):
    for dy in range(0, 151, 50):
        draw_line(fd, x, dy + y, x + 500, dy + y)

    for dx in range(0, 501, 50):
        draw_line(fd, dx + x, y, dx + x, y + 150)

    for i in range(3):
        for j in range(10):
            draw_number(fd, x, y, j, i, board[j][i])
    fd.write('1 setlinewidth\n')
    fd.write('stroke\n')
description = 'Print random cards for Bingo using PostScript'
parser = argparse.ArgumentParser(prog='cartonator', description=description)
parser.add_argument('-i', '--include', default=0,
    help='include always the specified number')
parser.add_argument('-e', '--exclude', default=0,
    help='include always the specified number')
parser.add_argument('file', default='stdout',
    help='File to write the Postscript to. If ommited, write to stdout')
args = parser.parse_args()

carton = get_carton(included=args.include, excluded=args.exclude)
if args.file != 'stdout':
    fd = open(args.file, 'w')
else:
    fd = sys.stdout
fd.write('%!PS-Adobe-3.0\n')
draw_carton(fd, 50, 650, carton)
if args.file != 'stdout':
    fd.close()

