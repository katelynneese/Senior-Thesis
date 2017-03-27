# found quasars that fall in range: 3101

from astropy.io import fits
import numpy as np

qfile = open("SQLtext.txt", "w") # the file to write the SQL code to


# fits file containing quasars that fall in range
quasarlist = fits.open("SDSS_lowZ_quasar.fits")
data = quasarlist[1].data

# RA and DEC of each quasar
RA = data['RA']
DEC = data['DEC']
Z = data['Z']

# JS specified a range here (1 arcsec) to look
rad = 1/3600.  #1 arcsec in degrees





#SELECT & FROM info
# SELECTS the specified information FROM the table name
# WHERE filters the records (where detect inner is true)
# I'm assuming everthing here is still named the same and that I need the same info

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

# now need the 'location component' (I only have 3101 quasars)
# for every single quasar, write:



# x, y, z min and max (from polar coords to cartesian coords)
# part of the WHERE string specifies the location of the quasar


for alpha, delta in zip(RA, DEC):
  x_min = str(np.cos((alpha + rad)*np.pi/180.)*np.cos((delta + rad)*np.pi/180.))
  x_max = str(np.cos((alpha - rad)*np.pi/180.)*np.cos((delta - rad)*np.pi/180.))
  y_min = str(np.sin((alpha - rad)*np.pi/180.)*np.cos((delta + rad)*np.pi/180.))
  y_max = str(np.sin((alpha + rad)*np.pi/180.)*np.cos((delta - rad)*np.pi/180.))
  z_min = str(np.sin((delta - rad)*np.pi/180.))
  z_max = str(np.sin((delta + rad)*np.pi/180.))


  coordstr = "((main.cx BETWEEN " + x_min + " AND " + x_max + ") AND (main.cy BETWEEN " + y_min + " AND " + y_max + ") AND (main.cz BETWEEN " + z_min + " AND " + z_max + ")) OR\n"

	#attach coordstr to SQL
  qfile.write(coordstr)






# defines minimum magnitude
qfile.write("main.imag_psf <= 25\n")
# 3101 quasars looking for 
qfile.write("LIMIT\n")
qfile.write("3101")

qfile.close()
