# -*- coding: cp1252 -*-
import math as m

def j_(d, tw, tfs, tfi, bfs, bfi):
    h = (d - tfs * 0.5 - tfi * 0.5)
    j_ = 1 / 3.0 * (bfs * tfs ** 3 + bfi * tfi ** 3 + h * tw ** 3) / 1.0
    return j_


def i_x(d, tw, bfs, tfs, bfi, tfi):
    i_x = (bfs * tfs * ((d / 2.0 - tfs / 2.0) ** 2) + bfi * tfi * (d / 2.0 - tfi / 2.0) ** 2 + tw * ((d - tfs - tfi) ** 3) / 12.0) / 1
    return i_x


def i_y(d, tfs, bfs, bfi, tfi, tw):
    i_y = (tfs * bfs ** 3.0 / 12.0 + tfi * bfi ** 3 / 12.0 + (d - tfs - tfi) * tw ** 3 / 12.0) / 1
    return i_y


def i_t(tfs, bfs, tw, d):
    i_t = (((2 * bfs * (tfs ** 3))) + ((d - tfs) * (tw ** 3))) / 3.0
    return i_t    

def area(d, tw, bfs, tfs, bfi, tfi):
    area = (((d) * tw) + (bfs * tfs) + (bfi * tfi))
    return area

def r_x(ix, area):
    r_x = (ix / area) ** (0.5)
    return r_x


def r_y(iy, area):
    r_y = ((iy / area) ** (0.5))
    return r_y


## Planilha fernando

def r_t(it, area):
    r_t = ((it / area) ** (0.5))
    return r_t


def wx(ix, d):
    wx = (2 * ix) / d
    return wx

def wy(iy, d):
    wy = (2 * iy) / d
    return wy

def cgx (d):
    cgx = d / 2.0
    return cgx

def cgy(bfs):
    cgy = bfs / 2.0
    return cgy


def zx(bf, tf, d, tw):
    hw = d - 2 * tf
    zx1 = bf * (d * d - hw * hw)
    zx2 = tw * hw * hw
    zx = (zx1 + zx2) / 4.0     
    return zx

def zy(bf, tf, d, tw):
    hw = d - 2 * tf
    zy = ((bf ** 2) * tf * 0.5) + (0.25 * hw * tw ** 2)
    return zy


def tensaor(fy):
    tr = 0.3 * fy
    return tr

def cw(d, tf, bf):    
    h = (d - tf * 0.5 - tf * 0.5)
    cw = ((bf ** 3)* tf / 12.0) * (((d - tf) ** 2) / 2.0)
    return cw

def kc(tf, d, tw):
    hw = d - 2 * tf
    kc = 4 / ((hw / tw)**0.5)
    return kc

def lambda_y(ly, ry):
    lambda_y = ly / ry
    return lambda_y

def lambda_x(lx, rx):
    lambda_x = lx / rx
    return lambda_x


          

    



