# Qt5 meta package for Sailfish OS

Packaging of Qt 5.15 for SFOS under /opt. Contains also general issues
regarding the packaging.

## Getting Started

Developpers can following the quick guide at
https://github.com/sailfishos-chum/qt5/wiki/Getting-Started

## Dependencies

To avoid conflict with the system-provided dependencies, we cannot
rely on RPM automatic dependencies handling for libraries or apps and
have to specify them manually.

Reason for manual dependencies handling is simple: libraries with the
same name are provided by system-installed and new Qt. For example,
`libQt5Core` would be otherwise provided by new Qt and the
system-installed one. So, in Qt5 RPM SPECs, we have to disable
automatic search for the libraries by adding

```
%{?opt_qt5_default_filter}
```

at the end of the SPEC header, before the package requirements. If there are
other `__requires_exclude_from`, `__provides_exclude_from`,
`__requires_exclude` and `__provides_exclude` defined in SPEC, those
have to be defined before `opt_qt5_default_filter`.
