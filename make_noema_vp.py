from casatools import vpmanager

vpman = vpmanager()
vpman.setpbairy(telescope='OTHER', othertelescope='NOEMA',
           dishdiam='15m', blockagediam='1.5m',
                maxrad='55arcsec', reffreq='90GHz' #1.2*lambda/D
                )
vpman.saveastable('noema.pb')

##code to paste into casatasks/private/simutil.py noisetemp function
# elif telescope == 'NOEMA':
# f0 = [82, 108.256, 138.616, 171.256, 207.744, 264.384]
# t0 = [(25 + 45) / 2, (25 + 45 + 35 + 55) / 4, (35 + 55) / 2, (35 + 55 + 40 + 70) / 4, (40 + 70) / 2]
# # taken from NOEMA Documentation, Table 2 https://www.iram.fr/IRAMFR/GILDAS/doc/pdf/noema-intro.pdf
# flim = [82, 264.384]

