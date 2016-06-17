from setuptools import setup, find_packages

requirements = ["cffi>=1.0.0"]

setup(name="pycallgrind",
      version="0.1",
      packages=find_packages(exclude=["pycallgrind/_build_wrapper.py"]),
      setup_requires=requirements,
      install_requires=requirements,
      ext_package="pycallgrind",
      cffi_modules=["pycallgrind/_build_wrapper.py:ffi"])
