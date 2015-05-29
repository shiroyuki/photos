""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""
from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from imagination.locator          import Locator

def load_services(locator=None, *paths):
    if not locator:
        locator = Locator()

    transformer = Transformer(locator)
    assembler   = Assembler(transformer)

    assembler.activate_passive_loading()
    [assembler.load(path) for path in paths]
    assembler.deactivate_passive_loading()

    return locator