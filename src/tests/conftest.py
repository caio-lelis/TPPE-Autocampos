# tests/conftest.py
import sys
import os

# Adiciona o src ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


# python -m pytest tests/unit/models/test_carro.py -v
