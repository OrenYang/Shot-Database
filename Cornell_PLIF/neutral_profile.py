import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths



density = np.load('test_density.npz')['arr_0']

px_to_mm = 70/906  #70mm/906 px

centerline = 580

valve_plane = 205

profile = 350

horizontal = np.linspace(-centerline*px_to_mm,(density.shape[1]-centerline)*px_to_mm,num=density.shape[1])
dashed = np.full(density.shape[1],(profile-valve_plane)*px_to_mm)

plt.figure(1)

plt.contourf(density,extent=(-centerline*px_to_mm,(density.shape[1]-centerline)*px_to_mm,-valve_plane*px_to_mm,(density.shape[0]-valve_plane)*px_to_mm))
plt.plot(horizontal,dashed,'r--')

plt.figure(2)

plt.plot(horizontal,density[profile][:])

peaks_pixel, _ = find_peaks(density[profile][:],prominence=1,height=1e16,distance=100)
peaks_mm=(peaks_pixel-centerline)*px_to_mm

full_width = peak_widths(density[profile][:],peaks_pixel, rel_height=0.84)

plt.plot(peaks_mm, density[profile][peaks_pixel], "x")

left_mm = (full_width[2]-centerline)*px_to_mm
right_mm = (full_width[3]-centerline)*px_to_mm

plt.hlines(full_width[1],left_mm,right_mm,color="C3")


plt.figure(3)

ol = float(input('Outer liner pressure:'))
il = float(input('Inner liner pressure:'))
cj = float(input('Central jet pressure:'))

pressures = [1,3,8,3,1]
new_press = [ol,il,cj,il,ol]

for i in range(len(pressures)):
    density[profile][int(full_width[2][i]):int(full_width[3][i])]=density[profile][int(full_width[2][i]):int(full_width[3][i])]/pressures[i]*new_press[i]

plt.plot(horizontal,density[profile][:])
plt.hlines(full_width[1],left_mm,right_mm,color="C3")

plt.show()
