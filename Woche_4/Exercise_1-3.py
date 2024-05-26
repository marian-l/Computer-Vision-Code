import numpy as np
import scipy as sc
from matplotlib import pyplot as plt

f = np.array([0, 1, 0, -1])
f_T = f.T

# Calculate the Fourier Transform F for f
FourierTransform = sc.fft.fft(f)
print('FourierTransform:', FourierTransform)

n = 4
x = f

frequency = np.fft.fftfreq(4)
print('frequency', frequency)

magnitudes = np.abs(FourierTransform)
print('magnitudes (strength of each frequeny component: ', magnitudes)
phases = np.angle(FourierTransform)
print('phases (PhaseShift of each component in radians (pi/2)', phases)

FourierTransform_manual = np.sum(x * np.exp(-2j * np.pi * frequency * np.arange(n)/n))
print('FourierTransform_manual', FourierTransform_manual)

# Plot the Fourier Transform magnitudes
plt.stem(frequency, magnitudes)
plt.title('magnitudes Spectrum')
plt.xlabel('Frequency')
plt.ylabel('magnitudes')
plt.show()

# Plot the Fourier Transform phases
plt.stem(frequency, phases)
plt.title('Phase Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Phase (Radians)')
plt.show()

FourierTransformSquared = FourierTransform * FourierTransform
print('FourierTransformSquared', FourierTransformSquared)

InverseFT = np.fft.ifft(FourierTransformSquared)
print('InverseFT', InverseFT)

# Optionally, plot the result to visualize it
plt.stem(np.abs(InverseFT))
plt.title('Result of Convolution f * f')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()