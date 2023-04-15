# Update support

To make sure that Qt and KF libraries are up to date, several scripts
and configuration files were made to simplify changing of the
versions.

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
  are errors, investigate and see what went wrong. You may have to
  make full update manually then.

- If all went well, you have sources updated in GitHub. Go and check
  repositories, corresponding RPM SPEC files, and upstream commits
  pointed by the package.

- to be continued with OBS part

## Configuration file format

There are three files describing packages that are handled by these
scripts:

- `packages.qt5` - Qt5 packages;

- `packages.kf5` - KDE Frameworks packages;

- `applications.obs` - List of applications and libraries that are
  using Qt5 or KF5 packages listed above.

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
