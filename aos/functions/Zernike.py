def CreateZernikePolynomials(wfs):
    """
    Zernike clas

    Input:
        wfs (class): useful parameters\n

    Output:
        nadayy (float): Zernike modes\n
    """
    nPx = wfs.nPx
    jModes = wfs.jModes
    pupilLogical = wfs.pupilLogical
    u = nPx

    return u