import streamlit as st
from tempfile import NamedTemporaryFile


def get_temp_file(file):
    with NamedTemporaryFile(delete=False) as tfile:
        filedata = file.read()
        tfile.write(filedata)
        tfilename = tfile.name
        return tfilename