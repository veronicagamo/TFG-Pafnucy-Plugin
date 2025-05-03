# **************************************************************************
# *
# * Authors: Verónica Gamo (veronica.gamoparejo@usp.ceu.es)
# *
# * Biocomputing Unit, CNB-CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

# Scipion em imports
import os, subprocess
from subprocess import run
from scipion.install.funcs import InstallHelper

# Scipion chem imports
import pwchem

# Plugin imports
from .constants import PLUGIN_VERSION, PAFNUCY_DIC

_version_ = PLUGIN_VERSION
_logo = ""
_references = ['']

class Plugin(pwchem.Plugin):
	@classmethod
	def _defineVariables(cls):
		""" Return and write a variable in the config file. """
		cls._defineEmVar(PAFNUCY_DIC['home'], '{}-{}'.format(PAFNUCY_DIC['name'], PAFNUCY_DIC['version']))

	@classmethod
	def defineBinaries(cls, env):
		""" Install the necessary packages. """
		cls.addPafnucy(env)

	########################### PACKAGE FUNCTIONS ###########################
	@classmethod
	def addPafnucy(cls, env, default=True):
		"""This function installs PAFNUCY's package."""
		
		# Instantiating install helper
		installer = InstallHelper(PAFNUCY_DIC['name'], packageHome=cls.getVar(PAFNUCY_DIC['home']), packageVersion=PAFNUCY_DIC['version'])

		pafnuncy_env_name = f"{PAFNUCY_DIC['name']}-{PAFNUCY_DIC['version']}"
		absolute_download_dir = os.path.abspath(cls.getVar(PAFNUCY_DIC['home']))
		repo_dir = os.path.join(absolute_download_dir, "pafnucy")

		# Check if it is already cloned
		if not os.path.exists(repo_dir):
			clone_command = f'cd {absolute_download_dir} && git clone https://gitlab.com/cheminfIBB/pafnucy'
		else:
			clone_command = f'cd {repo_dir} && git pull origin main'  # Update if it exists

		# Installing package
		installer.getCondaEnvCommand(binaryName=PAFNUCY_DIC['name'], binaryVersion=PAFNUCY_DIC['version']) \
			.addCommand(clone_command) \
			.addCommand(f'cd {repo_dir} && conda env update --name {pafnuncy_env_name} --file environment_gpu.yml') \
			.addPackage(env, dependencies=['conda'], default=default)

	@classmethod
	def runPafnuncy(cls, program, args, cwd=None):
		""" Run Pafnuncy command from a given protocol. """
		absolute_download_dir = os.path.abspath(cls.getVar(PAFNUCY_DIC['home']))
		repo_dir = os.path.join(absolute_download_dir, "pafnucy")
		full_program = '%s && cd %s && %s ' % (cls.getEnvActivationCommand(PAFNUCY_DIC), repo_dir, program)
		print('full_program ', full_program +args )
		run(full_program + args, env=cls.getEnviron(), cwd=cwd, shell=True)
