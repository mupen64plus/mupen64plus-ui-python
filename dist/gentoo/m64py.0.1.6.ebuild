# Copyright 1999-2013 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: Exp $
EAPI=5

PYTHON_COMPAT=( python2_7 )

inherit distutils-r1

DESCRIPTION="A frontend for Mupen64Plus"
HOMEPAGE="http://m64py.sourceforge.net/"
SRC_URI="mirror://sourceforge/m64py/${P}-bundle.tar.gz"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="7zip rar"

RDEPEND="media-libs/libsdl
	dev-python/PyQt4[opengl,${PYTHON_USEDEP}]
	>=games-emulation/mupen64plus-2.0
	7zip? ( || ( dev-python/pylzma app-arch/p7zip ) )
	rar? ( || ( app-arch/unrar app-arch/rar ) )"

DOCS=( AUTHORS ChangeLog README )
