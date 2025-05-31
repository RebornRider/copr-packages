#Copyright © 2021-2025 rusty-snake
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#!/bin/bash

set -e

shopt -s nullglob

cd -P -- "$(readlink -e "$(dirname "$0")")"

USER="${USER:-$(id -un)}"
HOME="${HOME:-$(getent passwd $USER | cut -d: -f7)}"
XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

usage() {
	cat <<-EOM
	./rpmbuild.sh [-hlnsi] <package>

	  -h  Show this help and exit.
	  -l  Do not run rpmlint.
	  -n  Disable build dependencies check, useful if they aren't installed via dnf.
	  -s  Run rpmbuild unsandboxed.
	  -i  Allow rpmbuild to access the network (ignore if used together with -s).
	EOM
}

while getopts "hlnsi" opt; do
	case $opt in
		h)
			usage
			exit 0
		;;
		l)
			RBS_NOLINT=true
		;;
		n)
			RBS_NODEPS=true
		;;
		s)
			RBS_NOSANDBOX=true
		;;
		i)
			RBS_SANDBOX_INET=true
		;;
		*)
			exit 2
		;;
	esac
done
PACKAGE="${!OPTIND}"

if [[ -z "$PACKAGE" ]]; then
	usage
	exit 2
fi

REQUIRED_PROGRAMS=(rpmbuild rpmlint spectool)
for program in "${REQUIRED_PROGRAMS[@]}"; do
	if ! command -v $program >&-; then
		echo "rpmbuild.sh: Please install $program: sudo dnf install \"\$(dnf repoquery --whatprovides \"/usr/bin/$program\" 2>/dev/null)\""
		exit 5
	fi
done

TOPDIR="$(mktemp -d /var/tmp/rpmbuild.sh-XXXXXX)"
# shellcheck disable=SC2064
trap "rm -rf '$TOPDIR'" EXIT

BUILDDIR=$(rpm --define "_topdir $TOPDIR" --eval %_builddir)
RPMDIR=$(rpm --define "_topdir $TOPDIR" --eval %_rpmdir)
SOURCEDIR=$(rpm --define "_topdir $TOPDIR" --eval %_sourcedir)
SPECDIR=$(rpm --define "_topdir $TOPDIR" --eval %_specdir)
SRPMDIR=$(rpm --define "_topdir $TOPDIR" --eval %_srcrpmdir)
mkdir -p "$BUILDDIR" "$RPMDIR" "$SOURCEDIR" "$SPECDIR" "$SRPMDIR"

cp "$PACKAGE/$PACKAGE.spec" "$SPECDIR/$PACKAGE.spec"
if [[ -e "$PACKAGE/setup_sourcedir.sh" ]]; then
	(cd "$PACKAGE" && source ./setup_sourcedir.sh)
else
	spectool -C "$XDG_CACHE_HOME/rpmbuild.sh/$PACKAGE" --gf "$SPECDIR/$PACKAGE.spec"
	while read -r source; do
		sourcefile=$(echo "$source" | sed 's/^Patch[0-9]*: //' | sed 's/^Source[0-9]*: //')
		echo "$sourcefile"
		cp "$XDG_CACHE_HOME/rpmbuild.sh/$PACKAGE/$sourcefile" "$SOURCEDIR/$sourcefile"
	done < <(spectool --lf "$SPECDIR/$PACKAGE.spec" | xargs -d"\n" -L1 basename)
fi

BWRAP_ARGS=(
	# TODO: --seccomp
	--die-with-parent
	--unshare-all
	--new-session
	--cap-drop all
	--proc /proc
	--dev /dev
	--ro-bind /usr /usr
	--symlink usr/bin /bin
	--symlink usr/lib /lib
	--symlink usr/lib64 /lib64
	--symlink usr/sbin /sbin
	--dir /tmp
	--ro-bind-try /etc/alternatives /etc/alternatives
	--ro-bind-try /etc/dnf /etc/dnf
	--ro-bind-try /etc/rpm /etc/rpm
	--ro-bind-try /etc/rpmrc /etc/rpmrc
	--ro-bind-try /etc/yum.repos.d /etc/yum.repos.d
	--ro-bind-try /var/cache/dnf /var/cache/dnf
	--ro-bind-try /var/lib/dnf /var/lib/dnf
	--ro-bind-try /var/lib/rpm /var/lib/rpm
	--dir /var/tmp
	--bind "$TOPDIR" "$TOPDIR"
)
if [[ -n "$RBS_SANDBOX_INET" ]]; then
	BWRAP_ARGS+=(
		--share-net
		--ro-bind-try /etc/resolv.conf /etc/resolv.conf
		--ro-bind-try /etc/pki /etc/pki
		--ro-bind-try /etc/ssl /etc/ssl
	)
fi

RPMBUILD_ARGS=(
	--nodebuginfo
	--define "_topdir $TOPDIR"
)
if [[ -n "$RBS_NODEPS" ]]; then
	RPMBUILD_ARGS+=(--nodeps)
fi

RPMBUILD_CMD=(rpmbuild "${RPMBUILD_ARGS[@]}" -bb "$SPECDIR/$PACKAGE.spec")

if [[ -n "$RBS_NOSANDBOX" ]]; then
	"${RPMBUILD_CMD[@]}"
else
	bwrap "${BWRAP_ARGS[@]}" -- "${RPMBUILD_CMD[@]}"
fi

if [[ -z "$RBS_NOLINT" ]]; then
	rpmlint --info "$SPECDIR"/*.spec "$RPMDIR"/*/*.rpm "$SRPMDIR"/*.rpm ||:
fi

cp "$RPMDIR"/*/*.rpm "$SRPMDIR"/*.rpm .
