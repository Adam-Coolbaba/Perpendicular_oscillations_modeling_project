import numpy as np


def calculate_kinetic_energy(m, v):
    return m*v**2/2

# w = czestosc wlasna, jesli masz jakis lepszy pomysl na oznaczenie to mozesz zmienic
def calculate_potential_energy(m, w, x):
    return m*(w*x)**2/2


def calculate_osc_speed(t, w, a):
    return a*w*np.cos(w*t)


def calculate_osc_acceleration_magnitude(t, w, a):
    return -a*w**2*np.sin(w*t)

#jesli masz jakis pomysl na inne parametry ktore warto by umiescic w tabeli powiazanej z amimacja to smialo dodawaj