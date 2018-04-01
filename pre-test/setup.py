from distutils.core import setup
# from distutils.extension import Extension
from Cython.Build import cythonize

# ext_modules = [
#     Extension(
#         "test",
#         ["test.pyx"],
#         extra_compile_args=['-fopenmp'],
#         extra_link_args=['-fopenmp'],
#     )
# ]

setup(
    name='parallel-test',
    ext_modules=cythonize('test.pyx'),
)