from project import required_capital, required_return, required_years, required_annual_cf, required_lumpsum
import pytest


def test_required_capital():
    assert pytest.approx(required_capital(12000, 0.08, 20), rel=1e-5) == 117817.77
    assert pytest.approx(required_capital(25000, 0.10, 40), rel=1e-5) == 244476.27


def test_required_return():
    assert pytest.approx(round(required_return(5000, 250000, 25), 3), rel=1e-5) == 0.169
    assert pytest.approx(round(required_return(100000, 1000000, 25), 3), rel=1e-5) == 0.096


def test_required_years():
    assert pytest.approx(round(required_years(10000, 150000, 0.1), 2), rel=1e-5) == 28.41
    assert pytest.approx(round(required_years(1000, 25000, 0.1), 2), rel=1e-5) == 33.77


def test_required_annual_cf():
    assert pytest.approx(required_annual_cf(250000, 0.1, 30, 10000), rel=1e-5) == 459.02
    assert pytest.approx(required_annual_cf(250000, 0.05, 30, 0), rel=1e-5) == 3762.86


def test_required_lumpsum():
    assert pytest.approx(required_lumpsum(100000, 0.08, 6), rel=1e-5) == 63016.96
    assert pytest.approx(required_lumpsum(250000, 0.10, 10), rel=1e-5) == 96385.82
    assert pytest.approx(required_lumpsum(1000000, 0.10, 25), rel=1e-5) == 92295.99


# para correr o ficheiro escrever no terminal: pytest nomeficheiro.py