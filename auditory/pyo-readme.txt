libraries located in:

/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7


Installing pyo on macOS is a bit more difficult. Here's how to do it. Ideally, it would be possible to install pyo from a .dmg file from here: http://ajaxsoundstudio.com/software/pyo/. Unfortunately, this installs pyo for a Framework build of python. That is, the installer creates folders at "/Library/Frameworks/Python.framework" even if no Framework build of python is installed, and therefore it doesn't work out of the box for a version of python installed with Homebrew, Anaconda, or Enthought Canopy.

You can still use the .dmg installer, but you have to manually move the pyo files from "/Library/Frameworks/Python.framework" to your python. Specifically you have to move the following files.

    _pyo.so
    _pyo64.so
    pyo.py
    pyo64.py
    pyolib (folder)

In addition to creating and compiling these files, the .dmg installer also creates the following dynamic libraries.

    liblo.7.dylib
    libportaudio.2.dylib
    libportmidi.dylib
    libsndfile.1.dylib
    libFLAC.8.dylib
    libvorbisenc.2.dylib
    libvorbis.0.dylib
    libogg.0.dylib

It puts these libraries in your "/usr/local/lib" directory.

If you use Homebrew, this is a problem, as pyo has now put things into folders managed by Homebrew that were not installed by Homebrew, and it might break other stuff. If you don't use Homebrew or some other system for managing what's in your /usr/local/lib, you may at some point install something that breaks pyo.

To compile pyo from source, you first have to install the .dylibs with Homebrew, and then install pyo from github.

brew install liblo libsndfile portaudio portmidi

Then you can install pyo from git.

pip install \
  --install-option="--use-coreaudio" \
  --install-option "--use-double" \
  git+git://github.com/belangeo/pyo.git

Assuming all goes well, you can now use pyo as your audio lib for psychopy.

import pyo
