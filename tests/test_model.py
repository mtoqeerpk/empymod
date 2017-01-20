import pytest
import numpy as np
from numpy.testing import assert_allclose
from scipy.constants import epsilon_0, mu_0

# Test 1: Import main modelling routines from empymod directly to ensure they
#         are in the __init__.py-file.
from empymod import bipole, dipole, frequency, time
# Import rest from model
# from empymod.model import gpr, wavenumber, tem, fem
from empymod.kernel import fullspace, halfspace

# model. Status: 6/13
# These are kind of macro-tests, as they check the final results.
# I try to use different parameters for each test, to cover a wide range of
# possibilities. It won't be possible to check all the possibilities though.
# Add tests when issues arise!

# This approach for the modeller-comparisons:
#
# # Different Sets of Sources
# dipSources = [
#         [0, 0, 400],
#         [100, -100, 400]
#         ]
#
# # Different Sets of Receivers
# dipReceivers = [
#         [1000, 0, 500],
#         [1000, 1000, 1000]
#         ]
#
# # Different Sets of Models
# simpleModels = [
#         {'depth': 0, 'res': [1e12, 10], 'aniso': [1, 1]},
#         {'depth': [0, 500], 'res': [1e12, 0.3, 10], 'aniso': [1, 1, 2]}
#         ]
#
#
# # Create different types of surveys
# class SimpleDipoleSurvey:
#     @pytest.mark.parametrize("src", dipSources)
#     @pytest.mark.parametrize("rec", dipReceivers)
#     @pytest.mark.parametrize("model", simpleModels)
#     def test_single(self, src, rec, model):
#         self.do(src, rec, model)


class TestBipole:                                                   # 1. bipole
    # => Main and most important checks/comparisons

    # 1.1. Comparison to analytical fullspace solution          # 1.1 fullspace
    #      More or less random values, to test a wide range of models.
    #      src fixed at [0, 0, 0]; It will never be possible to test all
    #      combinations...
    sp1 = ("ab", "rec", "freq", "res", "aniso", "epH", "epV", "mpH", "mpV")
    vp1 = [(11, [100000, 0, 500], 0.01, 10, 1, 1, 50, 67, 1),
           (12, [10000, 0, 400], 0.1, 3, 50, 1, 100, 68, 2),
           (13, [1000, 0, 300], 1, 3, 1, 50, 25, 69, 3),
           (14, [100, 0, 100], 10, 20, 1, 100, 1, 70, 4),
           (15, [10, 0, 10], 100, 4, 2, 1, 25, 71, 5),
           (16, [1, 0, 1], 1000, .004, 3, 50, 1, 72, 6),
           (21, [1, 0, -1], 1000, 300, 1, 1, 25, 73, 7),
           (22, [10, 0, -10], 100, 20, 1, 50, 1, 74, 8),
           (23, [100, 0, -100], 10, 1, 1, 1, 25, 75, 9),
           (24, [1000, 0, -300], 1, 100, 1, 50, 1, 76, 10),
           (25, [10000, 0, -400], 0.1, 1000, 1, 1, 25, 77, 11),
           (26, [100000, 100, -500], 0.01, 100, 2, 50, 1, 78, 12),
           (31, [0, 100000, 0], 0.01, 10, 1, 1, 25, 79, 13),
           (32, [0, 10000, 0], 0.1, 10, 1, 50, 1, 80, 14),
           (33, [0, 1000, 500], 1, 10, 1, 1, 25, 81, 15),
           (34, [0, 100, 0], 10, 10, 1, 50, 1, 82, 16),
           (35, [10, 10, 0], 100, 10, 1, 1, 25, 83, 17),
           (41, [0, 1, 0], 1000, 10, 1, 50, 1, 84, 18),
           (42, [0, 1, 0], 1000, 10, 1, 1, 25, 85, 19),
           (43, [0, 10, 0], 100, 10, 1, 50, 1, 86, 20),
           (44, [0, 100, 500], 10, 10, 1, 1, 25, 87, 21),
           (45, [100, 1000, 300], 1, 10, 1, 50, 1, 88, 22),
           (46, [0, 10000, 0], 0.1, 10, 1, 1, 25, 89, 23),
           (51, [0, 100000, 0], 0.01, 10, 1, 50, 1, 90, 24),
           (52, [-1, 0, 0], 1, 10, 1, 1, 25, 91, 25),
           (53, [-10, 0, 500], 10, 10, 1, 50, 1, 92, 26),
           (54, [-100, 100, 300], 1, 10, 1, 1, 25, 93, 27),
           (55, [-1000, 0, 0], 1, 10, 1, 50, 1, 94, 28),
           (56, [0, -1, 0], 100, 10, 1, 1, 25, 95, 29),
           (61, [0, -10, 0], 10, 10, 1, 50, 1, 96, 30),
           (62, [-100, -100, -500], 1, 10, 1, 1, 25, 97, 31),
           (64, [0, -1000, 0], 0.1, 10, 1, 50, 1, 98, 32),
           (65, [0, -10000, 0], 0.01, 10, 1, 1, 25, 99, 33),
           (66, [50, 50, 500], 1, 10, 1, 50, 1, 100, 34)]

    @pytest.mark.parametrize(sp1, vp1)
    def test_fullspace(self, ab, rec, freq, res, aniso, epH, epV, mpH, mpV):
        # Calculate required parameters
        eH = np.array([1/res + 2j*np.pi*freq*epH*epsilon_0])
        eV = np.array([1/(res*aniso**2) + 2j*np.pi*freq*epV*epsilon_0])
        zH = np.array([2j*np.pi*freq*mpH*mu_0])
        zV = np.array([2j*np.pi*freq*mpV*mu_0])
        off = np.sqrt(rec[0]**2 + rec[1]**2)
        angle = np.arctan2(rec[1], rec[0])
        zrec = rec[2]
        srcazm = 0
        srcdip = 0
        if ab % 10 in [3, 6]:
            srcdip = 90
        elif ab % 10 in [2, 5]:
            srcazm = 90
        recazm = 0
        recdip = 0
        if ab // 10 in [3, 6]:
            recdip = 90
        elif ab // 10 in [2, 5]:
            recazm = 90
        msrc = ab % 10 > 3
        mrec = ab // 10 > 3
        if mrec:
            if msrc:
                ab -= 33
            else:
                ab = ab % 10*10 + ab // 10

        # Get fullspace
        fs_res = fullspace(off, angle, 0, zrec, eH, eV, zH, zV, ab, msrc, mrec)

        # Get bipole
        bip_res = bipole([0, 0, 0, srcazm, srcdip],
                         [rec[0], rec[1], zrec, recazm, recdip], 1e20,
                         [res, res+1e-10], freq, None, [aniso, aniso],
                         [epH, epH], [epV, epV], [mpH, mpH], [mpV, mpV], msrc,
                         1, mrec, 1, 0, False, 'fht',
                         None, None, None, None, None, 0)

        # Check
        assert_allclose(fs_res, bip_res)

    # 1.2. Comparison to analytical halfspace solution          # 1.2 halfspace
    #      More or less random values, to test a wide range of models.
    #      src fixed at [0, 0, 0]; It will never be possible to test all
    #      combinations...
    #      halfspace is only implemented for electric sources and receivers so
    #      far, and for the diffusive approximation (low freq).
    sp2 = ("ab", "rec", "freq", "res", "aniso")
    vp2 = [(11, [10000, -300, 500], 0.01, 10, 1),
           (12, [5000, 200, 400], 0.1, 3, 5),
           (13, [1000, 0, 300], 1, 3, 1),
           (21, [100, 500, 500], 1, 3, 5),
           (22, [1000, 200, 300], 1, 4, 2),
           (23, [0, 2000, 200], 0.01, .004, 3),
           (31, [3000, 0, 300], 0.1, 300, 1),
           (32, [10, 1000, 10], 1, 20, 1),
           (33, [100, 6000, 200], 0.1, 1, 1)]

    @pytest.mark.parametrize(sp2, vp2)
    def test_halfspace(self, ab, rec, freq, res, aniso):
        # Calculate required parameters
        srcazm = 0
        srcdip = 0
        if ab % 10 in [3, 6]:
            srcdip = 90
        elif ab % 10 in [2, 5]:
            srcazm = 90
        recazm = 0
        recdip = 0
        if ab // 10 in [3, ]:
            recdip = 90
        elif ab // 10 in [2, ]:
            recazm = 90
        msrc = ab % 10 > 3

        # Get fullspace
        hs_res = halfspace(rec[0], rec[1], 100, rec[2], res, freq, aniso, ab)

        # Get bipole
        bip_res = bipole([0, 0, 100, srcazm, srcdip],
                         [rec[0], rec[1], rec[2], recazm, recdip], 0,
                         [1e20, res], freq, None, [1, aniso],
                         None, None, None, None, msrc, 1, False, 1, 0, False,
                         'fht', None, None, None, None, None, 0)

        # Check
        assert_allclose(hs_res, bip_res)

    # 1.3. Comparison to EMmod

    # 1.4. Comparison to DIPOLE1D

    # 1.5. Comparison to Green3D


def test_dipole():                                                 # 2. dipole
    # As this is a shortcut, just run one test to ensure
    # it is equivalent to bipole.
    src = [5000, 1000, -200]
    rec = [0, 0, 1200]
    model = {'depth': [100, 1000], 'res': [2, 0.3, 100], 'aniso': [2, .5, 2]}
    f = 0.01
    # v  dipole : ab = 26
    # \> bipole : src-dip = 90, rec-azimuth=90, msrc=True
    dip_res = dipole(src, rec, freqtime=f, ab=26, **model, verb=0)
    bip_res = bipole([src[0], src[1], src[2], 0, 90],
                     [rec[0], rec[1], rec[2], 90, 0], msrc=True, freqtime=f,
                     **model, verb=0)
    assert_allclose(dip_res, bip_res)

# 3. gpr (Check it remains as in paper)

# 4. wavenumber (Finish wavenumber properly; write checks)


def test_frequency():                                           # 5. frequency
    # As this is a shortcut, just run one test to ensure
    # it is equivalent to dipole with signal=None.
    src = [100, -100, 400]
    rec = [1000, 1000, 1000]
    model = {'depth': [0, 500], 'res': [1e12, 0.3, 10], 'aniso': [1, 1, 2]}
    f = 1
    ab = 45
    f_res = frequency(src, rec, freq=f, ab=ab, **model, verb=0)
    d_res = dipole(src, rec, freqtime=f, ab=ab, **model, verb=0)
    assert_allclose(f_res, d_res)


def test_time():                                                      # 6. time
    # As this is a shortcut, just run one test to ensure
    # it is equivalent to dipole with signal!=None.
    src = [-100, 300, 600]
    rec = [1000, -500, 400]
    model = {'depth': [-100, 600], 'res': [1e12, 3, 1], 'aniso': [1, 2, 3]}
    t = 10
    ab = 51
    signal = -1
    ft = 'fftlog'
    t_res = time(src, rec, time=t, signal=signal, ab=ab, ft=ft, **model,
                 verb=0)
    d_res = dipole(src, rec, freqtime=t, signal=signal, ab=ab, ft=ft,
                   **model, verb=0)
    assert_allclose(t_res, d_res)


# 7. fem

# 8. tem
