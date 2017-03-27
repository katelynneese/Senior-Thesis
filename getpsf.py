import lsst.daf.persistence as dafPersist
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
import numpy as np

# Get the Butler and the skymap for the whole of HSC
butler = dafPersist.Butler("/tigress/HSC/HSC/rerun/production-20151224/")
skymap = butler.get("deepCoadd_skyMap”)

# These are just example co-ordinates. You could add in an extra line that reads in your fits file and extracts the co-ordinates directly.
ra = 220.0
dec = 0.000

# Create the co-ordinate tuple that HSCPipe can read from ra and dec
raDec = afwCoord.Coord(ra*afwGeom.degrees, dec*afwGeom.degrees)

# Find what tract and patch the object is in
tractInfo, patchInfo = skymap.findClosestTractPatchList([raDec])[0]
tract = tractInfo.getId()
tract=int(tract)
patch = "%d,%d" % patchInfo[0].getIndex()

try:
        # Go retrieve the coadd image in the i-band for the tract and patch of this object
        coadd = butler.get("deepCoadd_calexp", tract=tract, patch=patch, filter="HSC-I", immediate=True)

        # Get the World Coordinate System information for the coadd image and convert the raDec to pixel co-ordinates
        wcs = coadd.getWcs()
        wcs.skyToPixel(raDec)

        # Extract the psf image at those pixel co-ordinates
        psf=coadd.getPsf()
        pstamppsf = psf.computeImage(wcs.skyToPixel(raDec))

        # Write the pdf image to a fits file
        outfile='psf.fits'
        pstamppsf.writeFits(outfile)

except:
        # If there was an error creating the psf then print the co-ordinates
        print str(ra)+' '+str(dec)
