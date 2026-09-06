#
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
#

project('pynotify', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
src_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

#
# top-level files
#

#
# Python submodules
#
subdir('src/pynotify')

#
# Deps
#

#
# Executables
#

#
# Install
#

s_license = 'src/data/license'
s_changelog = 'src/data/changelog'
s_docs = 'src/data/docs'
s_examples = 'src/data/examples'
s_scripts = 'src/scripts'
manual = 'pynotify.pdf'

# 
# /usr/share/pynotify/docs
# 
install_data(
  [
    s_docs / manual,
  ],
  install_dir: d_share / 'pynotify/docs'
)

install_subdir(
  [
    s_docs / 'html',
  ],
  install_dir: d_share / 'pynotify/docs',
  strip_directory: false
)

# 
# /usr/share/pynotify 
# 
install_data(
  [
    'README.rst',
    s_changelog / 'Changelog.rst',
    'packaging/Changelog',
  ],
  install_dir: d_share / 'pynotify'
)

install_data(
  [
    s_examples / 'test_inotify.py',
    ],
  install_dir: d_share / 'pynotify/examples',
)

# 
# /usr/share/licenses/pynotify 
# 
install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_dir: d_share / 'licenses/pynotify'
)

