# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypkamd']

package_data = \
{'': ['*'], 'pypkamd': ['G54a7pHt.ff/*', 'fixbox/*']}

install_requires = \
['pypka>=2.4.0']

entry_points = \
{'console_scripts': ['pypkamd = pypkamd.__main__:main']}

setup_kwargs = {
    'name': 'pypkamd',
    'version': '0.2.0',
    'description': 'PypKa + GROMACS = an awesome Constant-pH Molecular Dynamics implementation',
    'long_description': '# PypKa-MD\n\nPypKa + MD = constant-pH molecular dynamics\n\nImplementation of the stochastic titration method <sup>1</sup>\n\n[1] Baptista *et al.*, J. Chem. Phys. 117, 4184 (2002) DOI: 10.1063/1.1497164\n\n## Installation\n\n```\npython3 -m pip install pypkamd\n```\n\n## Dependencies\n\nBoth PypKa and GROMACS are required to be installed in the system.\n\n- PypKa >= 2.3.0\n- GROMACS >=5.1.5\n\n## Usage\n\nUpon installation a PypKa-MD executable should have been added to your bin. You may call it directly giving as an argument a modified GROMACS .mdp input file to include Constant-pH specific variables.\n\n```\npypkamd System.mdp\n```\n\nIn case the executable as not been added to your bin, you may use:\n\n```\npython3 -m pypkamd System.mdp\n```\n\nYou may find an example .mdp file in /utils/cphmd.mdp. \n\n```\n; GROin = system_000.gro     ; input GRO file\n; TOPin = system_000.top     ; input TOP file\n; DATin = fixgro.dat         ; input DAT file (to be removed)\n; NDXin = system.ndx         ; input NDX file\n; sysname = system_001       ; output files root name\n; sites = all                ; to be titrating sites in the protein\n; titrating_group = Protein  ; index group of the protein\n; nCycles = 50               ; number of CpHMD cycles\n                            ;; total simulation time = nCycles * tau_prot\n                            ;; 1ns = 50 * 20ps\n; nCPUs = 4                  ; number of CPUs to be used\n; pH = 7.0                   ; pH value of the protonation states sampling\n; ionicstr = 0.1             ; ionic strength used in PB\n; GroDIR="/gromacs/gromacs-5.1.5_pH_I/bin/" ; GROMACS bin path\n```',
    'author': 'Pedro Reis',
    'author_email': 'pdreis@fc.ul.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mms-fcul/PypKa-MD',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
