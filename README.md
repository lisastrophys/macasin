# MACASIN
If you wish to simulate radiointefermeter observations on a telescope that is not in CASA but you really wish to use CASA, it is actually very simple and requires only three components: configuration, voltage pattern/primary beam and receiver temperatures (for noise). Let's go over each of them.
## Configuration
Configuration file is a simple ASCII file with .cfg extension. CASA has a few of those ready, especially for ALMA, they can be found here: https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html#Array-Configuration. If your desired configuration is not among those, you have to make your own. You can also find an example for two NOEMA configurations in this repository (made by Anna Punanova). The configuration file contains the observatory name, its coordinates (COFA, may not be necessary if CASA knows the location already like for NOEMA), coordinate system for antenna locations (the usual is local, LOC) and a list of antennas with their names, diameters in meters and location in xyz in meters. To use them for your simulations, it is enough to give `simalma` or `simobserve` file location in `antennalist` argument.
## Voltage pattern/primary beam
Those files are a bit more complicated so it will require a CASA routine to make them. The package `casatools` has `vpmanager` module that makes those files. There is a number of parametric shapes you can set your voltage pattern with, a full list with argument descriptions can be found here: https://casa.nrao.edu/aips2_docs/user/SynthesisRef/node201.html. For NOEMA we used a standard Airy disk pattern. It has 4 main arguments: `dishdiam`, `blockagediam`, `maxrad` and `reffreq`. `dishdiam` and `blockagediam` are dish and secondary mirror (that blocks the dish) diameter, respectively. According to NOEMA webpage, they are 15m and 1.5m respectively. `maxrad` can be evaluated as $1.2\lambda/D$, where $\lambda$ is reference wavelength (so `reffreq` is $c/\lambda$) and $D$ is dish diameter. Full code to make NOEMA primary beam files can be found below or in `make_noema_vp.py` in the repository.
```python
from casatools import vpmanager

vpman = vpmanager()
vpman.setpbairy(telescope='OTHER', othertelescope='NOEMA',
           dishdiam='15m', blockagediam='1.5m',
                maxrad='55arcsec', reffreq='90GHz')
vpman.saveastable('noema.pb')
```
The output is a folder of your chosen name, in this example it is `noema.pb` (also available in repository). To use it in your simulation routine you need to add the following code before `simalma/simobserve`
```python
from casatools import vpmanager

vpman = vpmanager()
vpman.loadfromtable(tablename='noema.pb')
```
Now your CASA simulator will recognise the primary beam for the telescope. Be careful to have the same telescope name in the .cfg and .pb files!
## Receiver temperature
Unfortunately, there is no easy way to add it just as primary beam. There is a path to set your whole simulation manually with `casatools.simulator`, it has a `setnoise` routine and receiver temperature is `trx` argument. If you wish to keep using `simalma/simobserve`, the only way seems to modify `noisetemp` routine in `casatasks/private/simutil.py`. In this routine, CASA stores receiver temperatures for given frequency ranges for a small selection of telescopes (ALMA, ACA, VLA, SMA). Thankfully, it is easy to expand this list by a well placed `elif`. Below is a code that we suggest to insert for NOEMA, based on the values from documentation: https://www.iram.fr/IRAMFR/GILDAS/doc/pdf/noema-intro.pdf
```python
elif telescope=='NOEMA':
    f0=[82, 108.256, 138.616, 171.256, 207.744, 264.384]
    t0=[(25+45)/2, (25+45+35+55)/4, (35+55)/2, (35+55+40+70)/4, (40+70)/2]
    # taken from NOEMA Documentation, Table 2 https://www.iram.fr/IRAMFR/GILDAS/doc/pdf/noema-intro.pdf
    flim = [82, 264.384]
```
A copy of the code is also available inside `make_noema_vp.py`.

And that's it, you have everything to simulate observations on the telescope array of your choice!
