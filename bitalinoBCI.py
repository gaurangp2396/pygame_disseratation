from ndf_lsl import ndf_lsl
import numpy as np

# Setup LSL object and resolve incoming stream from Bitalino
ndf = ndf_lsl(stream_name="OpenSignals")
ndf.ndf_setup()

while True:
    buffer = ndf.ndf_read()[1]
    ecg = buffer[:,1] - buffer[:,0]
    AvgAbsECG = np.mean(np.abs(ecg))
    if AvgAbsECG > 500:
        print("yes!!!")
    else:
        print("No!!!!")
