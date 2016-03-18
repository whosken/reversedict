import setuptools

setuptools.setup(name='reversedict',
                 version='0.2.2',
                 description='Look up words by definition',
                 url='http://github.com/whosken/reversedict',
                 author='Ken Hu',
                 author_email='whosbacon@gmail.com',
                 license='MIT',
                 packages=['reversedict'],
                 install_requires=['textblob','elasticsearch'],
                 zip_safe=False)
