#!/usr/bin/env python3

from random import randint
from palettegenerator import Palette

DEBUG = True

#------------------

def debug(string, inte=0):
    '''debuging function
    arguments:
            string = message that should be displayed
    '''
    if DEBUG:
        print('[DEBUG]',string, inte)

#-------------------

def get_empty_palette(amount):
    '''get a palette full of empty (black) spaces
    arguments:
            amount = number of colors in the palette
    returns:
            list of color tuples
    '''
    return [(0, 0 ,0) for i in range(0, amount)]

#-------------------

def get_random_colors(amount):
    '''we create a list of random colors
    arguments:
            amount = number of colors we want to create
    returns:
            a list of color tupels
    '''
    if amount <= 0: return []
    
    return [(randint(0, 255), randint(0, 255), randint(0, 255)) for i in range(0, amount)]

#-----------------

# FIXME we need a better rounding function for more accurate conversions
def convert_hls_rgb(hls):
    '''convert a hls color into rgb
    arguments:
            hls = tuple of hue, luminance, saturation
    returns:
            tuple of red, green, blue
    '''
    # no saturation -> grey
    h, l, s = hls
    
    if s == 0:
        r, g, b = round(l * 255)
        return (r,g,b)
        
    t1 = 0
    if l < 0.5:
        t1 = l * (1+s)
    else:
        t1 = l + s - l*s
        
    t2 = 2 * l - t1
    
    h2 = h/360
    
    # get color channels
    tr = h2 + (1/3)
    if tr > 1: tr -= 1
    elif tr < 0: tr += 1
    
    tg = h2
    
    tb = h2 - (1/3)
    if tb > 1: tb -= 1
    elif tb < 0: tb += 1
    
    # select correct forula for each color channel
    # red
    r = 0
    if 6*tr < 1:
        r = t2 + (t1-t2) * 6 * tr
    elif 2 * tr < 1:
        r = t1
    elif 3*tr < 2:
        r = t2 + (t1-t2) * (0.666-tr) * 6
    else:
        r = t2
        
    # green
    g = 0
    if 6 * tg < 1:
        g = t2 + (t1-t2) * 6 * tg
    elif 2 * tg < 1:
        g = t1
    elif 3 * tg < 2:
        g = t2 + (t1-t2) * (0.666-tg) * 6
    else:
        g = t2
        
    # blue
    b = 0
    if 6 * tb < 1:
        b = t2 + (t1-t2) * 6 * tb
    elif 2 * tb < 1:
        b = t1
    elif 3 * tb < 2:
        b = t2 + (t1-t2) * (0.666-tb) * 6
    else:
        b = t2
        
    r = round(r*255)
    g = round(g*255)
    b = round(b*255)
    
    return (r, g, b)
    
#------------------

def convert_rgb_hls(rgb):
    '''a given RGB color gets converted into hls
    arguments:
            rgb = tuple of red, green, blue
    returns:
            a tuple of hue, luminance, saturation
    '''
    # convert rgb to floats 0<v<1
    fr = rgb[0]/255
    fg = rgb[1]/255
    fb = rgb[2]/255
    
    # min and max of those values
    minval = min(fr, min(fg, fb))
    maxval = max(fr, max(fg, fb))
    
    # luminance value
    l = (round(((minval + maxval)/2)*100))/100
    debug('lum:', l)
    
    # saturation
    h = 0
    s = 0
    if minval == maxval:
        return (h,l,s)
    elif l < 0.5:
        s = round(((maxval-minval)/(maxval+minval))*100)/100
    else:
        s = round(((maxval-minval)/(2-maxval-minval))*100)/100
        
    debug('sat:', s)
    # hue
    if fr == maxval:
        h = (fg-fb)/(maxval-minval)
    elif fg == maxval:
        h = 2.0+(fb-fr)/(maxval-minval)
    else:
        h = 4.0+(fr-fg)/(maxval-minval)
        
    h *= 60
    if h < 0:
        h += 360
        
    debug('hue:', h)
    
    return (h,l,s)
        
#-------------------

def get_palette_colors_rgb(amount, initcolor):
    '''create color steps in HLS
    arguments:
            amount = number of colors we want in our list
            initcolor = going from the lightest to the darkest color
    returns:
            list of amount colors
    '''
    col = [initcolor]
    r = initcolor[0]//amount
    g = initcolor[1]//amount
    b = initcolor[2]//amount
    
    for i in range(0, amount-1):
        col.append((col[i][0]-r, col[i][1]-g, col[i][2]-b))
        
    return col
    
#--------------------------
    
'''hue ranges'''
HUERANGE = [356, 11, # red (0)
            11, 21, # red-orange (1)
            21, 41, # orange-brown (2)
            41, 51, # orange-yellow (3)
            51, 61, # yellow (4)
            61, 81, # yellow-green (5)
            81, 141, # green (6)
            141, 170, # green-cyan (7)
            170, 201, # cyan (8)
            201, 221, # cyan-blue (9)
            221, 241, # blue (10)
            241, 281, # blue-magenta (11)
            281, 321, # magenta (12)
            321, 331, # magenta-pink (13)
            331, 346, # pink (14)
            346, 356] # pink-red (15)
# FIXME hue ranges for in-between colors
def get_palette_colors_hls(amount, initcolor):
    '''create color ramps in HLS
    arguments:
            amount = number of colors we want in our list
            initcolor = lightest color in RGB tuple
    returns:
            list of amount colors
    '''
    h, l, s = convert_rgb_hls(initcolor)
    # first color -> transparent, second -> intial
    colors = [(0,0,0)]
    
    # determine the starting color area depending on the hue
    starthue = 0
    loop = True
    if h >= HUERANGE[0] or h <= HUERANGE[1]:
        starthue = 0
        loop = False

    if loop:    
        for i in range(2, len(HUERANGE), 2):
            if h >= HUERANGE[i] and h <= HUERANGE[i+1]:
                starthue = i//2
                break
                
    if starthue == 0 and loop == True:
        debug('starthue could not be retrieved correctly')
        exit(1)
    debug('starthue:', starthue)
        
    # we want darker colors, so determine difference between init hue and blue,
    # while also avoiding yellow, which is the brightest one
    mb = (HUERANGE[20] + HUERANGE[21])//2
    right = 0 # 0 - below yellow, 1 - above yellow
    if starthue < 4 or starthue == 4 and h <= (HUERANGE[8]+HUERANGE[9])//2:
        side = 0
    else:
        side = 1
    debug('side:', side)
        
    debug('mb:', mb)
    
    # which color is our target point?
    nextrange = 0
    if starthue == 0 and not side: # red underflow
        nextrange = len(HUERANGE)//2 - 2
    if starthue == 1 and not side:
        nextrange = len(HUERANGE)//2 - 1
    elif starthue == 10 or starthue == 9 or starthue == 11: # startpoint is blue
        nextrange = starthue
    elif starthue > 11: # we already passed blue, so we want the previous section
        nextrange = starthue - 2
    elif starthue >= 4 and side: # we passed the middle of yellow
        nextrange = starthue + 2
    else:
        nextrange = starthue - 2
        
    debug('nextrange', nextrange)

    nextmidd = 0
    if nextrange == 0:
        nextmidd = ((HUERANGE[0] + HUERANGE[1]+360)//2) - 360
    else:
        nextmidd = (HUERANGE[(nextrange)*2] + HUERANGE[(nextrange)*2 + 1]) // 2

    debug('nextmidd:', nextmidd)

    if nextrange > starthue + 2:
        diff = h + (360-nextmidd)
    else:
        diff = abs(h-nextmidd)
        
    steps = diff/amount
    if h > mb or not side:
        steps *= -1
    debug('steps:', steps)
    
    # we need a number for saturation and luminance
    satdiff = s/25
    lumdiff = l/16
    
    # get new colors
    i = 0
    hh = h + steps
    ll = l + lumdiff
    ss = s + satdiff
    
    hlslist = [(h,l,s)]
    while i < amount:
        # first in hls annotation
        hh, ll, ss = hlslist[len(hlslist)-1][0]+steps, hlslist[len(hlslist)-1][1]-lumdiff, hlslist[len(hlslist)-1][2]+satdiff
        if hh > 360:
            hh -= 360
        elif hh < 0:
            hh += 360
        
        if ss > 1:
            ss = 1
        elif ss < 0:
            ss = 0
        
        if ll > 1:
            ll = 1
        elif ll < 0:
            ll = 0
            
        hlslist.append((hh, ll, ss))
        i += 1
    debug('list:',hlslist)
    
    # lastly convert hls colors back int rgb
    for i in hlslist:
        colors.append(convert_hls_rgb(i))
        
    cols = [colors[0]]
    for i in reversed(colors[1:]):
        cols.append(i)
        
    return cols

#---------------------
