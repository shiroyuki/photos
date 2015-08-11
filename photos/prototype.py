""" Prototype for Tori 4.0+ and Imagination 1.10+

    :Author: Juti Noppornpitak
"""

import argparse
from contextlib import contextmanager
import json

from imagination.helper.assembler import Assembler
from imagination.helper.data      import Transformer
from imagination.entity  import CallbackProxy
from imagination.entity  import Entity
from imagination.loader  import Loader
from imagination.locator import Locator

from tori.common import get_logger

class Console(object):
    def __init__(self, name, config_path=None, service_config_paths=[]):
        self.name      = name
        self.container = Container()

        self.config = {}

        if config_path:
            with open(config_path) as f:
                self.config.update(json.load(f))

            if 'db' in self.config:
                self._prepare_db_connections()

        self.container.load(*service_config_paths)

    def activate(self):
        main_parser = argparse.ArgumentParser(self.name)
        subparsers  = main_parser.add_subparsers(help='sub-commands')

        for identifier in self.container.all():
            service = self.container.get(identifier)

            if not isinstance(service, ICommand):
                continue

            documentation  = type(service).__doc__
            command_parser = subparsers.add_parser(identifier, help=documentation)

            service.define(command_parser)

            command_parser.set_defaults(func=service.execute)

        args = main_parser.parse_args()
        args.func(args)

    def _prepare_db_connections(self):
        db_config       = self.config['db']
        manager_config  = db_config['managers']
        service_locator = self.container.locator
        em_factory      = service_locator.get('db')

        for alias in manager_config:
            url = manager_config[alias]['url']

            em_factory.set(alias, url)

            def callback(em_factory, db_alias):
                return em_factory.get(db_alias)

            callback_proxy = CallbackProxy(callback, em_factory, alias)

            service_locator.set('db.{}'.format(alias), callback_proxy)

class Container(object):
    def __init__(self, locator=None):
        self.logger      = get_logger('{}.{}'.format(__name__, self.__class__.__name__))
        self.locator     = Locator()
        self.transformer = Transformer(self.locator)
        self.assembler   = Assembler(self.transformer)

        self.default_services = [
            ('finder',   'tori.common.Finder',                     [], {}),
            ('renderer', 'tori.template.service.RenderingService', [], {}),
            ('db',       'passerine.db.manager.ManagerFactory',    [], {})
        ]

        self.cache_map = None

        self._register_default_services()

    @contextmanager
    def passive_mode(self):
        self.assembler.activate_passive_loading()
        yield
        self.assembler.deactivate_passive_loading()

    def get(self, id):
        return self.locator.get(id)

    def load(self, *paths):
        with self.passive_mode():
            [
                self.assembler.load(path)
                for path in paths
            ]

            self.cache_map = None

    def all(self):
        if not self.cache_map:
            self.cache_map = {
                i: self.locator.get(i)
                for i in self.locator.entity_identifiers
            }

        return self.cache_map

    def _register_default_services(self):
        for entity_id, package_path, args, kwargs in self.default_services:
            try:
                entity = self._create_entity(entity_id, package_path, *args, **kwargs)

                self.locator.set(entity_id, entity)
            except ImportError as exception:
                if entity_id == "db":
                    self.logger.info('Ignored {} as package "passerine" is neither available or loadable (containing errors).'.format(package_path))

                    continue

                raise ImportError('Failed to register {} ({})'.format(entity_id, package_path))

    def _create_entity(self, id, package_path, *args, **kwargs):
        loader = Loader(package_path)

        return Entity(id, loader, *args, **kwargs)

class ICommand(object):
    def define(self, parser):
        pass

    def execute(self, args):
        raise NotImplementedError('Interface method')
