"""
This module is responsible for creating, removing, and indexing packages.
"""

from scspkg.scspkg_manager import ScspkgManager
from scspkg.pkg import Package
import os
import re


class PackageManager:
    """
    This package is responsible for creating, removing, and indexing packages.
    """

    def __init__(self):
        self.scspkg = ScspkgManager.get_instance()

    def create_pkgs(self, pkgs):
        """
        Create packages. Does not override if they already exist.

        :param pkgs: A list of pkgs or string
        """
        if isinstance(pkgs, str):
            pkgs = [pkgs]
        for pkg_name in pkgs:
            Package(pkg_name).create()
        return self

    def destroy_pkgs(self, pkgs):
        """
        Remove packages.

        :param pkgs: A list of packages or string
        """
        if isinstance(pkgs, str):
            pkgs = [pkgs]
        for pkg_name in pkgs:
            Package(pkg_name).destroy()
        return self

    def reset(self):
        """
        Remove all pkgs from scspkg

        :return: self
        """
        while True:
            x = input('Are you sure you want to destroy all packages? '
                      '(yes/no): ')
            if x == 'yes':
                break
            elif x == 'no':
                return
            else:
                print(f'{x} is neither yes or no')
                continue

        for pkg_name in self.avail():
            Package(pkg_name).destroy()
        return self

    def rebuild_modules(self):
        """
        This will rebuild the modulefiles for all packages
        """
        for pkg_name in self.avail():
            Package(pkg_name).save()

    def avail(self):
        """
        List all available packages in scspkg

        :return: None
        """
        return os.listdir(self.scspkg.module_dir)

    def change_module_type(self, module_type):
        """
        Change the module type of scspkg

        :param module_type: The new module type
        :return: None
        """
        self.module_type = module_type
        for pkg_name in self.avail():
            Package(pkg_name).load().save()
            print(f'Package {pkg_name} updated to {self.module_type.name} module type')
        self.scspkg.save()
        return self

    def reset_module(self, pkgs):
        """
        This will recreate the modulefiles for a set of pkgs.
        """
        if isinstance(pkgs, str):
            pkgs = [pkgs]
        if pkgs[0] == '*':
            for pkg_name in self.avail():
                Package(pkg_name).reset_config().save()
        else:
            for pkg_name in pkgs:
                Package(pkg_name).reset_config().save()

    def list(self, regexes=None):
        """
        List either all pkgs or a subset matching the regex
        """
        if regexes is None:
            self.list_all()
        else:
            if isinstance(regexes, str):
                regexes = [regexes]
            for regex in regexes:
                self.list_re(regex)
        return self

    def list_all(self):
        """
        List all pkgs

        :return: self
        """
        for pkg_name in self.avail():
            print(pkg_name)
        return self

    def list_re(self, regex):
        """
        List all pkgs matching the regex

        :param regex: The regex to match
        :return: self
        """
        print(f'pkgs matching {regex}: ')
        for pkg_name in self.avail():
            if re.search(regex, pkg_name):
                print(pkg_name)
        print()
        return self

