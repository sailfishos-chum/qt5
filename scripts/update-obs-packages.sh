# Update Qt or KF packages at OBS

set -e

ARGS_PROCESSED=$(getopt -o kqrt --long kf5,qt5,release,testing -- "$@")

INPUT=
KF5=
QT5=
GITHUB_BASE=https://github.com/rinigus
OBS_PROJECT=

eval set -- "$ARGS_PROCESSED"
while [ : ]; do
  case "$1" in
    -k | --kf5) KF5=1; INPUT=packages.kf5; shift; ;;
    -q | --qt5) QT5=1; INPUT=packages.qt5; shift; ;;
    -r | --release) OBS_PROJECT=home:rinigus:qt515:packaging; shift; ;;
    -t | --testing) OBS_PROJECT=home:rinigus:qt515:packaging; shift; ;;
    --) shift; break; ;;
  esac
done

# check options
[ -z "$KF5" ] && [ -z "$QT5" ] && echo "Specify whether KF5 or QT5 is updated" && exit 1
[ ! -z "$KF5" ] && [ ! -z "$QT5" ] && echo "Specify either KF5 or QT5 is updated" && exit 1
[ -z "$OBS_PROJECT" ] && echo "Specify whether you want to update release (sailfishos:chum) or testing (sailfishos:chum:testing) OBS project" && exit 1
[ -z "$INPUT" ] && echo "Input file missing" && exit 1

[ -d tmp ] && echo "Directory tmp exists. Please remove before starting." && exit 1

echo "Starting updates in ${OBS_PROJECT}"

# process packages
mkdir -p tmp
while read -r line; do
    [ -z "$line" ] && continue
    package_arr=($line)
    package_git=${package_arr[0]}
    package_obs=$package_git
    (( ${#package_arr[@]} > 1 )) && package_obs=${package_arr[1]}

    # get the tag with the largest version
    VERSION=$(git -c 'versionsort.suffix=-' ls-remote --exit-code \
		  --refs --sort='version:refname' --tags \
		  ${GITHUB_BASE}/${package_git} '*.*.*' | tail --lines=1 | cut --delimiter='/' --fields=3)

    echo
    echo "Update: ${package_git} -> ${package_obs}; Version: ${VERSION}"
    echo

    pushd tmp

    echo "Checking out: ${OBS_PROJECT} ${package_obs}"
    osc co -o ${package_obs} ${OBS_PROJECT} ${package_obs}
    pushd ${package_obs}
    sed -i \
	"s|<param name=\"revision\">.*</param>|<param name=\"revision\">${VERSION}</param>|g" _service
    osc commit -m "Update to ${VERSION}"
    popd
    popd
    echo
done < <(grep -v NOAUTO $INPUT)
