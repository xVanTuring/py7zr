import os
import pathlib

import pytest

import py7zr
from py7zr.exceptions import UnsupportedCompressionMethodError

try:
    import zstandard as Zstd  # type: ignore  # noqa
except ImportError:
    Zstd = None
try:
    import lz4.stream as LZ4  # type: ignore  # noqa
except ImportError:
    LZ4 = None
try:
    import brotli as Brotli  # type: ignore  # noqa
except ImportError:
    Brotli = None

testdata_path = pathlib.Path(os.path.dirname(__file__)).joinpath('data')
os.umask(0o022)


@pytest.mark.files
def test_extract_bzip2(tmp_path):
    archive = py7zr.SevenZipFile(testdata_path.joinpath('bzip2.7z').open(mode='rb'))
    archive.extractall(path=tmp_path)
    archive.close()


@pytest.mark.files
def test_extract_bzip2_2(tmp_path):
    archive = py7zr.SevenZipFile(testdata_path.joinpath('bzip2_2.7z').open(mode='rb'))
    archive.extractall(path=tmp_path)
    archive.close()


@pytest.mark.files
def test_extract_ppmd(tmp_path):
    with pytest.raises(UnsupportedCompressionMethodError):
        archive = py7zr.SevenZipFile(testdata_path.joinpath('ppmd.7z').open(mode='rb'))
        archive.extractall(path=tmp_path)
        archive.close()


@pytest.mark.files
def test_extract_deflate(tmp_path):
    with py7zr.SevenZipFile(testdata_path.joinpath('deflate.7z').open(mode='rb')) as archive:
        archive.extractall(path=tmp_path)


@pytest.mark.files
@pytest.mark.skipif(Zstd is None, reason="No zstandard library exist.")
def test_extract_zstd(tmp_path):
    with py7zr.SevenZipFile(testdata_path.joinpath('zstd.7z').open(mode='rb')) as archive:
        archive.extractall(path=tmp_path)


@pytest.mark.files
@pytest.mark.skipif(LZ4 is None, reason="No LZ4 library exist.")
@pytest.mark.xfail(reason="Incomplete implementation")
def test_extract_lz4(tmp_path):
    with py7zr.SevenZipFile(testdata_path.joinpath('lz4.7z').open(mode='rb')) as archive:
        archive.extractall(path=tmp_path)


@pytest.mark.files
@pytest.mark.skipif(Brotli is None, reason="No Brotli library exist.")
@pytest.mark.xfail(reason="Incomplete implementation")
def test_extract_brotli(tmp_path):
    with py7zr.SevenZipFile(testdata_path.joinpath('brotli.7z').open(mode='rb')) as archive:
        archive.extractall(path=tmp_path)