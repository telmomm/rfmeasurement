"""Synthetic skrf.Network builders shared across validation-rule tests."""

from __future__ import annotations

import numpy as np
import skrf as rf


def matched_two_port(n_points: int = 3) -> rf.Network:
    """A perfectly matched, lossless-thru 2-port: passive and reciprocal."""
    freq = rf.Frequency(1, 2, n_points, unit="GHz")
    s = np.zeros((n_points, 2, 2), dtype=complex)
    s[:, 0, 1] = 1.0
    s[:, 1, 0] = 1.0
    return rf.Network(frequency=freq, s=s)


def active_two_port(n_points: int = 3) -> rf.Network:
    """A 2-port with gain in one direction: not passive."""
    network = matched_two_port(n_points)
    network.s[:, 1, 0] = 5.0
    return network


def nonreciprocal_two_port(n_points: int = 3) -> rf.Network:
    """An isolator-like 2-port: transmits in one direction only."""
    freq = rf.Frequency(1, 2, n_points, unit="GHz")
    s = np.zeros((n_points, 2, 2), dtype=complex)
    s[:, 1, 0] = 0.9
    s[:, 0, 1] = 0.0
    return rf.Network(frequency=freq, s=s)


def one_port(n_points: int = 3, magnitude: complex = 0.0) -> rf.Network:
    freq = rf.Frequency(1, 2, n_points, unit="GHz")
    s = np.full((n_points, 1, 1), magnitude, dtype=complex)
    return rf.Network(frequency=freq, s=s)


def one_port_with_nonfinite(n_points: int = 3) -> rf.Network:
    network = one_port(n_points)
    network.s[1, 0, 0] = np.nan
    return network


def one_port_with_disordered_frequency() -> rf.Network:
    """Frequency grid with both an out-of-order point and a duplicate."""
    f_hz = np.array([2e9, 1e9, 1e9])
    freq = rf.Frequency.from_f(f_hz, unit="Hz")
    s = np.zeros((3, 1, 1), dtype=complex)
    return rf.Network(frequency=freq, s=s)


def one_port_with_discontinuity() -> rf.Network:
    network = one_port(3, magnitude=0.01)  # about -40 dB
    network.s[1, 0, 0] = 0.99  # jumps to about -0.1 dB
    return network


def one_port_near_noise_floor() -> rf.Network:
    return one_port(3, magnitude=1e-6)  # about -120 dB
