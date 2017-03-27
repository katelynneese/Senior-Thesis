from astropy.io import fits
import numpy as np


qfile = open("SQLtextv2.txt", "w") # the file to write the SQL code to


# fits file containing quasars that fall in range
quasarlist = fits.open("SDSS_lowZ_quasar.fits")
data = quasarlist[1].data

# RA and DEC of each quasar
RA = data['RA']
DEC = data['DEC']
Z = data['Z']
rad = 1/3600.  #1 arcsec in degrees
# maybe try reducing this ^ distance later?



#SELECT & FROM info
qfile.write("""
SELECT
  main.id, main.ra2000, main.decl2000, main.gmag_psf, main.rmag_psf, 
  main.imag_psf, main.zmag_psf, main.ymag_psf, main.gmag_psf_err, 
  main.rmag_psf_err, main.imag_psf_err, main.zmag_psf_err, main.ymag_psf_err, 
  main.gmag_cmodel, main.rmag_cmodel, main.imag_cmodel, main.zmag_cmodel, 
  main.ymag_cmodel, main.gmag_cmodel_err, main.rmag_cmodel_err, 
  main.imag_cmodel_err, main.zmag_cmodel_err, main.ymag_cmodel_err
FROM
  s15b_wide.photoobj_mosaic__deepcoadd__merged AS main
  LEFT JOIN s15b_wide.mosaic_refflag__deepcoadd AS refflag ON main.id = refflag.id
WHERE
  (refflag.detect_is_tract_inner = 't' AND refflag.detect_is_patch_inner = 't') AND\n""")

#create location component of SQL (3101 search queries)
for a,d in zip(RA, DEC):
	ra_min = str(a - rad)
	ra_max = str(a + rad)
	dec_min = str(d - rad)
	dec_max = str(d + rad)

	coordstr = "(ra2000 BETWEEN " + ra_min + " AND " + ra_max + " AND decl2000 BETWEEN " + dec_min + " AND " + dec_max + ") OR\n"

	qfile.write(coordstr)

qfile.write("main.imag_psf <= 25\n")
qfile.write("LIMIT\n")
qfile.write("20000")

qfile.close()