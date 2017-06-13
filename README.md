# Senior-Thesis
Senior thesis exploring the morphologies of the host galaxies of quasars.

For working with/opening/writing to FITs files, I used this guide: http://docs.astropy.org/en/stable/io/fits/


**FILE NAMING CONVENTIONS**: Q indicates a quasar, PSF indicates the point spread function. These are usually followed by the RA and DEC of the object, and finally the color band of the image (G R I Z Y). 

**hscSspCrossMatch.py**: Code provided by Sogo Mineo for cross-matching the positions of quasars. Effective and fast for a large number of quasars. For an example on how to run it, see Running hscSsp server-side cross match.ipynb.

**HSC Aperture.ipynb**: Code used to find the flux aperature, flux, and magnitudes of each object vs the radius of the object. This was just a stepping stone for me, I didn't end up using it all that much. 

**LoopOverQPSF.ipynb**: The first time I tried to model the quasars, I zipped together 10 quasars and their corresponding PSFs and modeled all ten of them at once in a loop. n and b_n values were provided by Matsuoka. Function calcAB calculates the possible A and B values (magnitudes of PSF and quasar) for each re, b_n and n. Function calcChi2 then calculates the square sum for these values, and chiMin finds the *least* square, as well as the A, B, re, b_n, and n values that minimize it. This is then the model for that quasar. Function psf_profile averages the flux at each point. 

**Image Processing.ipynb**: Modeling quasars individually, using the same functions and methods as above.

**Fast Image Processing.ipynb**: My attempt at making the modelling process faster. It ended up not working and I ran out of time to try and improve it. 

**Combined HSC SDSS data.ipynb**: After matching the SDSS data to the HSC data, I did some basic analysis (such as magnitude vs redshift) and et cetera. 

**median quasar color plots.ipynb**: My preliminary work, I found an approximate magnitude for the host galaxies by subtracting the PSFmodel and Cmodel flux and converting back to magnitudes. I then plotted the medians of the resulting colors (ex. g - r, r - i...) versus redshift.
