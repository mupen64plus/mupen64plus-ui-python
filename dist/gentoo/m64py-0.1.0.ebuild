# Copyright 1999-2012 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: Exp $

EAPI=3

PYTHON_DEPEND="2"
SUPPORT_PYTHON_ABIS="1"
RESTRICT_PYTHON_ABIS="3.*"

inherit distutils

DESCRIPTION="A frontend for Mupen64Plus"
HOMEPAGE="http://m64py.sourceforge.net/"
SRC_URI="mirror://sourceforge/m64py/${P}.tar.gz"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="7zip rar"

RDEPEND="media-libs/libsdl
	dev-python/PyQt4
	>=games-emulation/mupen64plus-1.99.5
	7zip? ( || ( dev-python/pylzma app-arch/p7zip ) )
	rar? ( || ( app-arch/unrar app-arch/rar ) )"

DOCS="AUTHORS ChangeLog README"
