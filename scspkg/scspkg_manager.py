"""
This file contains properties which are globally accessible to all
scspkg modules. This can be used to configure various aspects
of scspkg.
"""
import pathlib
import inspect
from jarvis_util import *
import os
from enum import Enum


class ModuleType(Enum):
    TCL = 'tcl'
    LMOD = 'lmod'


class ScspkgManager:
    """
    A singleton which stores various properties that can be queried by
    internally by scspkg modules.
    """

    instance_ = None

    @staticmethod
    def get_instance():
        if ScspkgManager.instance_ is None:
            ScspkgManager.instance_ = ScspkgManager()
        return ScspkgManager.instance_

    def __init__(self):
        self.scspkg_root = str(
            pathlib.Path(inspect.getfile(self.__class__)).
                parent.parent.resolve())
        self.pkg_dir = f'{self.scspkg_root}/packages'
        self.module_dir = f'{self.scspkg_root}/modulefiles'
        self.config_dir = f'{self.scspkg_root}/config'
        self.env = LocalExecInfo().basic_env
        self.env_path = f'{self.config_dir}/env.yaml'
        self.module_type = ModuleType.TCL
        self.config = {}
        self.config_path = f'{self.config_dir}/scspkg_config.yaml'

    def init(self):
        """
        Create the configuration directories. Ensure that modules
        are scanned from the module_dir automatically
        """
        os.makedirs(self.pkg_dir, exist_ok=True)
        os.makedirs(self.module_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        self.build_env()
        self.save()
        return self

    def build_env(self):
        """
        Build the env.yaml file for scspkg.

        :return: self
        """
        YamlFile(self.env_path).save(self.env)
        return self

    def reset(self):
        """
        Destroy all packages in scspkg

        :return: self
        """
        Rm(self.pkg_dir, LocalExecInfo())
        Rm(self.module_dir, LocalExecInfo())
        Rm(self.config_dir, LocalExecInfo())
        return self

    def save(self):
        """
        Save the SCSPKG configuration files
        """
        self.config['MODULE_TYPE'] = self.module_type
        YamlFile(self.config_path).save(self.config)

    def load(self):
        """
        Load the SCSPKG configuration files

        :return: self
        """
        self.env = YamlFile(self.env_path).load()
        self.config = YamlFile(self.config_path).load()
        self.module_type = self.config['MODULE_TYPE']
        return self

    def build_profile(self):
        """
        Create a snapshot of important currently-loaded environment variables.

        :return: None
        """
        vars = ['PATH', 'LD_LIBRARY_PATH', 'LIBRARY_PATH', 'INCLUDE', 'CPATH',
                'PKG_CONFIG_PATH', 'CMAKE_PREFIX_PATH', 'JAVA_HOME']
        profile = [self._get_env(var) for var in vars]
        profile = [val for val in profile if val is not None]
        if self._get_env('INCLUDE') is not None:
            profile.append(self._get_env('INCLUDE'))
        profile = ";".join(profile, )
        print(profile)

    def _get_env(self, var, prefix=None):
        """
        Get an environment variable from the OS.

        :param var: The name of the variable
        :param prefix: What to rename the variable to. None means don't
        rename the variable
        :return: String or None
        """
        os_var = os.getenv(var)
        if os_var is None:
            return None
        if prefix is None:
            return f'{var}={os_var}'
        else:
            return f'{prefix}={os_var}'
