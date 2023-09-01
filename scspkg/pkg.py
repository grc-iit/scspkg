from scspkg.scspkg_manager import ScspkgManager, ModuleType
import os
import json
from jarvis_util import *


class Package:
    def __init__(self, package_name):
        self.scspkg = ScspkgManager.get_instance()
        self.name = package_name
        self.pkg_root = os.path.join(self.scspkg.pkg_dir, package_name)
        self.pkg_src = os.path.join(self.pkg_root, 'src')
        self.module_path = os.path.join(self.scspkg.module_dir, self.name)
        self.module_schema_path = os.path.join(self.pkg_root,
                                               f'{self.name}.yaml')
        self.sections = {}
        self.reset_config()

    def reset_config(self):
        """
        Create the skeleton configuration.
        """
        self.sections = {}
        self.sections['doc'] = {
            'Name': self.name,
            'Version': 'None',
            'doc': 'None'
        }
        self.sections['deps'] = {}
        self.sections['setenvs'] = {}
        self.sections['prepends'] = {
            'PATH': [os.path.join(self.pkg_root, 'bin'),
                     os.path.join(self.pkg_root, 'sbin')],
            'LD_LIBRARY_PATH': [os.path.join(self.pkg_root, 'lib'),
                                os.path.join(self.pkg_root, 'lib64')],
            'LIBRARY_PATH': [os.path.join(self.pkg_root, 'lib'),
                             os.path.join(self.pkg_root, 'lib64')],
            'INCLUDE': [os.path.join(self.pkg_root, 'include')],
            'CPATH': [os.path.join(self.pkg_root, 'include')],
            'CFLAGS': [os.path.join(self.pkg_root, 'include')],
            'LDFLAGS': [os.path.join(self.pkg_root, 'lib'),
                        os.path.join(self.pkg_root, 'lib64')]
        }

    def create(self):
        """
        Create the modulefile directories and initial modulefiles.

        :return: self
        """
        os.makedirs(self.pkg_root, exist_ok=True)
        os.makedirs(self.pkg_src, exist_ok=True)
        self.save()
        return self

    def save(self):
        """
        Save the YAML + modulefiles to the directories.
        """
        YamlFile(self.module_schema_path).save(self.sections)
        if self.scspkg.module_type == ModuleType.TCL:
            self._save_as_tcl()
        else:
            self._save_as_lmod()
        return self

    def _save_as_tcl(self):
        """
        Save the TCL representation of the YAML schema

        :return: None
        """
        module = []
        # The module header
        module.append('#%Module1.0')
        # The module doc
        for doc_key, doc_val in self.sections['doc'].items():
            module.append(f'module-whatis \'{doc_key}: {doc_val}\'')
        # The module dependencies
        for dep in self.sections['deps'].keys():
            module.append(f'module load \'{dep}\'')
        # The module environment variables
        for env, env_data in self.sections['setenvs'].items():
            module.append(f'setenv {env} \'{env_data}\'')
        # The module environment prepends
        for env, values in self.sections['prepends'].items():
            for value in values:
                module.append(f'prepend-path {env} \'{value}\'')
        # Write the lines
        with open(self.module_path, 'w') as fp:
            module = '\n'.join(module)
            fp.write(module)

    def _save_as_lmod(self):
        """
        Save the LMOD representation of the YAML schema

        :return: None
        """
        module = []
        # The module header
        module.append('-- Module1.0')
        # The module doc
        for doc_key, doc_val in self.sections['doc'].items():
            module.append(f'help(\"{doc_key}: {doc_val}\")')
        # The module dependencies
        for dep in self.sections['deps'].keys():
            module.append(f'depends_on(\"{dep}\")')
        # The module environment variables
        for env, env_data in self.sections['setenvs'].items():
            module.append(f'setenv(\"{env}\", \"{env_data}\")')
        # The module environment prepends
        for env, values in self.sections['prepends'].items():
            for value in values:
                module.append(f'prepend_path(\"{env}\", \"{value}\")')
        # Write the lines
        with open(self.module_path, 'w') as fp:
            module = '\n'.join(module)
            fp.write(module)

    def destroy(self):
        """
        Destroy all data for this package

        :return: self
        """
        Rm(self.pkg_root)
        Rm(self.module_path)
        return self

    def set_env(self, env_name, env_data):
        """
        Set the value of an environment variable.

        :param env_name: the environment variable to set
        :param env_data: the value of the variable
        :return: self
        """
        self.sections['setenvs'][env_name] = env_data
        if env_name in self.sections['prepends']:
            del self.sections['prepends'][env_name]
        return self

    def prepend_env(self, env_name, env_data):
        """
        Prepend data to an environment variable

        :param env_name: The environment variable to prepend to
        :param env_data: The data to prepend
        :return: self
        """
        if env_name not in self.sections['prepends']:
            self.sections['prepends'][env_name] = []
        self.sections['prepends'][env_name].insert(0, env_data)
        return self

    def rm_env(self, env_name):
        """
        Remove an environment

        :param env_name: The environment variable to remove
        :return: self
        """
        if env_name in self.sections['setenvs']:
            del self.sections['setenvs'][env_name]
        if env_name in self.sections['prepends']:
            del self.sections['prepends'][env_name]
        return self

    def rm_prepend(self, env_name, env_data):
        """
        Remove one of the prepend paths from this module

        :param env_name: The name of the environment variable in question
        :param env_data: The entry to remove
        :return: self
        """
        self.sections['prepends'][env_name].remove(env_data)
        return self

    def add_deps(self, deps):
        """
        Add dependencies to the module

        :param deps: A list or string of exact module names
        :return: self
        """
        for dep in deps:
            self.sections['deps'][dep] = True
        return self

    def rm_deps(self, deps):
        """
        Remove dependencies in the module

        :param deps: A list or string of exact module names
        :return: self
        """
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
            if dep in self.sections['deps']:
                del self.sections['deps'][dep]
        self.save()
        return self

    def ls_deps(self):
        """
        Print all dependencies of the module
        """
        for dep in self.sections['deps'].keys():
            print(dep)

    def get_module_schema(self):
        """
        Load the contents of the YAML module schema
        """
        if os.path.exists(self.module_schema_path):
            return json.dumps(self.sections, indent=4)
        else:
            print('Error: Package {} does not exist'.format(self.name))
            exit(1)

    def get_modulefile(self):
        """
        Load the text of the modulefile

        :return: String
        """
        try:
            with open(self.module_path, 'r') as f:
                return f.read()
        except:
            print('Error: Package {} does not exist'.format(self.name))
            exit(1)