# Update Qt or KF package sources

set -e

ARGS_PROCESSED=$(getopt -o kqv: --long kf5,qt5,version: -- "$@")

INPUT=
KF5=
QT5=
VERSION=
GITHUB_BASE=https://github.com/rinigus

eval set -- "$ARGS_PROCESSED"
while [ : ]; do
  case "$1" in
    -k | --kf5) KF5=1; INPUT=packages.kf5; shift; ;;
    -q | --qt5) QT5=1; INPUT=packages.qt5; shift; ;;
    -v | --version) VERSION=$2; shift 2; ;;
    --) shift; break; ;;
  esac
done

# check options
[ -z "$INPUT" ] && echo "Input file missing" && exit 1
[ -z "$VERSION" ] && echo "Target version missing" && exit 1
[ -z "$KF5" ] && [ -z "$QT5" ] && echo "Specify whether KF5 or QT5 is updated" && exit 1
[ ! -z "$KF5" ] && [ ! -z "$QT5" ] && echo "Specify either KF5 or QT5 is updated" && exit 1

[ -d tmp ] && echo "Directory tmp exists. Please remove before starting." && exit 1

# process packages
mkdir -p tmp
while read -r line; do
    [ -z "$line" ] && continue
    package_arr=($line)
    package=${package_arr[0]}

    pushd tmp
    git clone --recursive $GITHUB_BASE/$package
    pushd $package
    # update upstream
    pushd upstream
    if [ $KF5 ]; then
	git checkout v$VERSION
	REAL_VERSION=$VERSION
    elif [ $QT5 ]; then
	git checkout kde/5.15
	desc=`git describe`
	base_version=$(echo $desc | cut -d "-" -f 1)
	offset=$(echo $desc | cut -d "-" -f 4)
	if [ v"$VERSION" = $base_version ]; then
	    if [ -z $offset ]; then
		REAL_VERSION=$VERSION
	    else
		REAL_VERSION="${VERSION}+kde${offset}"
	    fi
	else
	    echo "KDE repository already moved to version ${base_version}; Checking out without KDE patches"
	    git checkout v${VERSION}-lts-lgpl
	    REAL_VERSION=$VERSION
	fi
    fi
    popd
    echo "Setting version to ${REAL_VERSION}"
    git add upstream

    sed -i "s/^Version:.*/Version: ${REAL_VERSION}/g" rpm/*.spec
    if [ $KF5 ]; then
	sed -i "s/^%global kf5_version .*/%global kf5_version ${VERSION}/g" rpm/*.spec
    elif [ $QT5 ]; then
	sed -i "s/^%global qt_version .*/%global qt_version ${VERSION}/g" rpm/*.spec
    fi
    git add rpm/*.spec
    git status
    
    if git diff-index --quiet HEAD; then
	echo "Sources are already updated in the repository, skipping commit"
    else
	git commit -m "Update to version ${REAL_VERSION}"
    fi
    
    if [ $(git tag -l ${REAL_VERSION}) ]; then
	echo "Git tag already set - skipping"
    else
	git tag ${REAL_VERSION}
    fi    

    git push origin main --tags
    popd
    popd
    echo
done < <(grep -v NOAUTO $INPUT)
