#SDSS crop worked!
#now time to generate the SQL code

from astropy.io import fits
import numpy as np

f = open("SQLcommand.txt","w")

#open SDSScrop.fits 
hdulist = fits.open("SDSScrop.fits")
locdata = hdulist[1].data
RA = locdata.field(0)
DEC = locdata.field(1)
rad = 1/3600. #1 arcsec in degrees

#SELECT & FROM info
f.write("""
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

#create location component of SQL (8713 long)
for a,d in zip(RA, DEC):
  x_min = str(np.cos((a + rad)*np.pi/180.)*np.cos((d + rad)*np.pi/180.))
  x_max = str(np.cos((a - rad)*np.pi/180.)*np.cos((d - rad)*np.pi/180.))
  y_min = str(np.sin((a - rad)*np.pi/180.)*np.cos((d + rad)*np.pi/180.))
  y_max = str(np.sin((a + rad)*np.pi/180.)*np.cos((d - rad)*np.pi/180.))
  z_min = str(np.sin((d - rad)*np.pi/180.))
  z_max = str(np.sin((d + rad)*np.pi/180.))


  coordstr = "((main.cx BETWEEN " + x_min + " AND " + x_max + ") AND (main.cy BETWEEN " + y_min + " AND " + y_max + ") AND (main.cz BETWEEN " + z_min + " AND " + z_max + ")) OR\n"

	#attach coordstr to SQL
  f.write(coordstr)

  #now I have SQL with location. Let's stitch in rest of the command
f.write("main.imag_psf <= 22\n")
f.write("LIMIT\n")
f.write("8713")

f.close()