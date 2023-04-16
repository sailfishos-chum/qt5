# Update support

To make sure that Qt and KF libraries are up to date, several scripts
and configuration files were made to simplify changing of the
versions.

## Configuration file format

There are three files describing packages that are handled by these
scripts:

- [packages.qt5](packages.qt5) - Qt5 packages;

- [packages.kf5](packages.kf5) - KDE Frameworks packages;

- [applications.obs](applications.obs) - List of applications and
  libraries that are using Qt5 or KF5 packages listed above.

Format is simple and consists of a list with one package per line. If
the package has different GitHub repository and OBS package names, put GitHub
name first then OBS package name. If automatic update is not available
for that package, add NOAUTO keyword at the end of the line. Examples:

```
qtbase
qtwebengine NOAUTO
kirigami2 opt-kf5-kirigami2
```

Comments are not supported. Empty lines can be inserted to improve
readability.

For applications using these libraries, it is recommended to add the
OBS package names to `applications.obs`.


## To update

Update instructions for Qt5 or KF5:

- Clone this repository

- Change current directory to cloned repository directory

- Make sure that you don't have any `tmp` subfolder left from previous
  updates

- For Qt5, run after replacing a version:
  - `scripts/update-sources.sh --qt5 --version 5.15.9`

- For KF5, run after replacing a version:
  - `scripts/update-sources.sh --kf5 --version 5.105.0`

- Observe that the script runs till the end without errors. If there
  are errors, investigate and see what went wrong. You can rerun
  `update-sources.sh` script several times - it will push changes to
  the repository only if there are changes.

- If all went well, you have sources updated in GitHub. Go and check
  repositories, corresponding RPM SPEC files, and upstream commits
  pointed by the package.

- Add a note regarding current Qt5 or KF5 version in corresponding
  repository ([Qt5](https://github.com/sailfishos-chum/qt5) or
  [KF5](https://github.com/sailfishos-chum/kf5)). Tag the repository
  with the corresponding version as well.

- Clean up `tmp` subfolder

- For updating packages at OBS `sailfishos:chum:testing`, run
  - for Qt5: `scripts/update-obs-packages.sh --qt5 --testing`
  - for KF5: `scripts/update-obs-packages.sh --kf5 --testing`

- Wait till update is finished and test it

- If all is fine, update release project by replacing the last option
  of the script:
  - for Qt5: `scripts/update-obs-packages.sh --qt5 --release`
  - for KF5: `scripts/update-obs-packages.sh --kf5 --release`


## To change OBS targets

To add or remove Sailfish OS targets for libraries and applications,
use `scripts/update-obs-targets.sh`:

- To add target:
  - `scripts/update-obs-targets.sh --release --add 4.5.0.19`

- To delete target
  - `scripts/update-obs-targets.sh --release --del 4.5.0.19`
