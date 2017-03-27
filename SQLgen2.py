#another approach to getting HSC data
#first try error
#unknown duplicate objects

from astropy.io import fits
import numpy as np

f = open("SQLcommand.txt","w")

#open SDSScrop.fits 
hdulist = fits.open("SDSS_BOSS_COMBINED.fits")
locdata = hdulist[1].data
RA = locdata.field(2)
DEC = locdata.field(4)
rad = 1/3600. #1 arcsec in degrees

#SELECT & FROM info
f.write("""
SELECT
main.object_id, main.ra, main.dec, main.gflux_aperture10, main.rflux_aperture10, 
main.iflux_aperture10, main.zflux_aperture10, main.yflux_aperture10, main.n921flux_aperture10, 
main.n816flux_aperture10, main.gflux_aperture15, main.rflux_aperture15, main.iflux_aperture15, 
main.zflux_aperture15, main.yflux_aperture15, main.n921flux_aperture15, main.n816flux_aperture15, 
main.gflux_aperture20, main.rflux_aperture20, main.iflux_aperture20, main.zflux_aperture20, 
main.yflux_aperture20, main.n921flux_aperture20, main.n816flux_aperture20, main.gflux_aperture30, 
main.rflux_aperture30, main.iflux_aperture30, main.zflux_aperture30, main.yflux_aperture30, 
main.n921flux_aperture30, main.n816flux_aperture30, main.gflux_aperture40, main.rflux_aperture40, 
main.iflux_aperture40, main.zflux_aperture40, main.yflux_aperture40, main.n921flux_aperture40, 
main.n816flux_aperture40, main.gflux_aperture57, main.rflux_aperture57, main.iflux_aperture57,
main.zflux_aperture57, main.yflux_aperture57, main.n921flux_aperture57, main.n816flux_aperture57, 
main.gflux_aperture84, main.rflux_aperture84, main.iflux_aperture84, main.zflux_aperture84, 
main.yflux_aperture84, main.n921flux_aperture84, main.n816flux_aperture84, main.gflux_aperture118, 
main.rflux_aperture118, main.iflux_aperture118, main.zflux_aperture118, main.yflux_aperture118, 
main.n921flux_aperture118, main.n816flux_aperture118, main.gflux_aperture168, main.rflux_aperture168, 
main.iflux_aperture168, main.zflux_aperture168, main.yflux_aperture168, main.n921flux_aperture168, 
main.n816flux_aperture168, main.gflux_aperture235, main.rflux_aperture235, main.iflux_aperture235, 
main.zflux_aperture235, main.yflux_aperture235, main.n921flux_aperture235, main.n816flux_aperture235, 
main.gflux_aperture10_err, main.rflux_aperture10_err, main.iflux_aperture10_err, main.zflux_aperture10_err, 
main.yflux_aperture10_err, main.n921flux_aperture10_err, main.n816flux_aperture10_err, main.gflux_aperture15_err, 
main.rflux_aperture15_err, main.iflux_aperture15_err, main.zflux_aperture15_err, main.yflux_aperture15_err, 
main.n921flux_aperture15_err, main.n816flux_aperture15_err, main.gflux_aperture20_err, main.rflux_aperture20_err, 
main.iflux_aperture20_err, main.zflux_aperture20_err, main.yflux_aperture20_err, main.n921flux_aperture20_err, 
main.n816flux_aperture20_err, main.gflux_aperture30_err, main.rflux_aperture30_err, main.iflux_aperture30_err, 
main.zflux_aperture30_err, main.yflux_aperture30_err, main.n921flux_aperture30_err, main.n816flux_aperture30_err, 
main.gflux_aperture40_err, main.rflux_aperture40_err, main.iflux_aperture40_err, main.zflux_aperture40_err, 
main.yflux_aperture40_err, main.n921flux_aperture40_err, main.n816flux_aperture40_err, main.gflux_aperture57_err, 
main.rflux_aperture57_err, main.iflux_aperture57_err, main.zflux_aperture57_err, main.yflux_aperture57_err, 
main.n921flux_aperture57_err, main.n816flux_aperture57_err, main.gflux_aperture84_err, main.rflux_aperture84_err, 
main.iflux_aperture84_err, main.zflux_aperture84_err, main.yflux_aperture84_err, main.n921flux_aperture84_err, 
main.n816flux_aperture84_err, main.gflux_aperture118_err, main.rflux_aperture118_err, main.iflux_aperture118_err, 
main.zflux_aperture118_err, main.yflux_aperture118_err, main.n921flux_aperture118_err, main.n816flux_aperture118_err, 
main.gflux_aperture168_err, main.rflux_aperture168_err, main.iflux_aperture168_err, main.zflux_aperture168_err, 
main.yflux_aperture168_err, main.n921flux_aperture168_err, main.n816flux_aperture168_err, main.gflux_aperture235_err, 
main.rflux_aperture235_err, main.iflux_aperture235_err, main.zflux_aperture235_err, main.yflux_aperture235_err, 
main.n921flux_aperture235_err, main.n816flux_aperture235_err

FROM
    s16a_uwide.forced AS main
WHERE
    (main.detect_is_tract_inner = 't' AND main.detect_is_patch_inner = 't') AND\n""")

#create location component of SQL (8713 long)
for a,d in zip(RA, DEC):
	ra_min = str(a - rad)
	ra_max = str(a + rad)
	dec_min = str(d - rad)
	dec_max = str(d + rad)

	coordstr = "(ra BETWEEN " + ra_min + " AND " + ra_max + " AND dec BETWEEN " + dec_min + " AND " + dec_max + ") OR\n"

	f.write(coordstr)

f.write("main.imag_psf <= 22\n")
f.write("LIMIT\n")
f.write("20000")

f.close()