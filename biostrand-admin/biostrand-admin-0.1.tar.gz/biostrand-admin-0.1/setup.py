from setuptools import setup, find_namespace_packages

package = "biostrand-admin"
version = '0.1'

setup(name=package,
      version=version,
      description="admin",
      url='https://github.com/BioStrand/biostrand-admin',
      packages=find_namespace_packages(include=['biostrand.*']),
      install_requires=[
        # Include necessary packages for primary functionality
        ],
      zip_safe=False,
      entry_points={
        #'console_scripts': ["biopip=biostrand.admin.__main__:main"]
        },
      include_package_data=True,
      package_data={
          #'biostrand': ["admin/templates/*.tmplt"]
      }
)
