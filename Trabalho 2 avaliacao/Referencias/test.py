#!/usr/bin/env python3
#coding=utf8
from pygnuplot import gnuplot
print("aaaaa")


# Gnuplot lines:
#set terminal pngcairo font "arial,10" fontscale 1.0 size 600, 400
#set output "simple.1.png"
#set key fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid
#set style increment default
#set samples 50, 50
#set title "Simple Plots" font ",20" norotate

g = gnuplot.Gnuplot()
g.set(terminal = 'pngcairo font "arial,10" fontscale 1.0 size 600, 400',
        output = '"simple.1.png"',
        key = 'fixed left top vertical Right noreverse enhanced autotitle box lt black linewidth 1.000 dashtype solid',
        style = 'increment default',
        samples = '50, 50',
        title = '"Simple Plots" font ",20" norotate')
g.plot('[-10:10] sin(x),atan(x),cos(atan(x))')
