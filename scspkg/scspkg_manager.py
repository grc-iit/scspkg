"""
This file contains properties which are globally accessible to all
scspkg modules. This can be used to configure various aspects
of scspkg.
"""
import pathlib
import inspect
import os
from enum import Enum
# pylint: disable=W0401,W0614
from jarvis_util import *
# pylint: enable=W0401,W0614

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
        self.init()
        self.load()

    def init(self):
        """
        Create the configuration directories. Ensure that modules
        are scanned from the module_dir automatically
        """
        if os.path.exists(self.module_dir):
            return
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
        self.config['MODULE_TYPE'] = self.module_type.name
        YamlFile(self.config_path).save(self.config)

    def load(self):
        """
        Load the SCSPKG configuration files

        :return: self
        """
        if os.path.exists(self.env_path):
            self.env = YamlFile(self.env_path).load()
        if os.path.exists(self.config_path):
            self.config = YamlFile(self.config_path).load()
        if 'MODULE_TYPE' in self.config:
            self.module_type = ModuleType[self.config['MODULE_TYPE']]
        return self

    def build_profile(self, path=None, method=None):
        """
        Create a snapshot of important currently-loaded environment variables.

        :return: None
        """
        env_vars = ['PATH', 'LD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'INCLUDE', 'CPATH', 'PKG_CONFIG_PATH', 'CMAKE_PREFIX_PATH',
                    'JAVA_HOME', 'PYTHONPATH']
        profile = {}
        for env_var in env_vars:
            env_data = self._get_env(env_var)
            if len(env_data) == 0:
                profile[env_var] = []
            else:
                profile[env_var] = env_data.split(':')
        self.env_profile(profile, path, method)
        return profile

    def env_profile(self, profile, path=None, method='dotenv'):
        # None-path profiles
        if method == 'clion':
                prof_list = [f'{env_var}={":".join(env_data)}'
                            for env_var, env_data in profile.items()]
                print(';'.join(prof_list))
        elif method == 'vscode':
            vars = [f'  \"{env_var}\": \"{":".join(env_data)}\"' for env_var, env_data in profile.items()]
            print('\"environment\": {')
            print(',\n'.join(vars))
            print('}')
        if path is None:
            return
        
        # Path-based profiles
        with open(path, 'w') as f:
            if method == 'dotenv':
                for env_var, env_data in profile.items():
                    f.write(f'export {env_var}=\"{":".join(env_data)}\"\n')
            elif method == 'cmake':
                for env_var, env_data in profile.items():
                    f.write(f'set(ENV{{{env_var}}} \"{":".join(env_data)}\")\n')

    def _get_env(self, env_var):
        """
        Get an environment variable from the OS.

        :param env_var: The name of the variable
        :return: String
        """
        os_var = os.getenv(env_var)
        if os_var is None:
            return ''
        return os_var
