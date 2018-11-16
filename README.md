## Macros to help in Python packaing using Virtualenv

This is a small set of RPM macros to help in packaging Python applications along
with virtualenv. This project is following the ideas from
https://dh-virtualenv.readthedocs.io/en/1.0/

The available macros will be updated regularly, right now we have very limit
macros.


## Example usage

```

# Use our interpreter for brp-python-bytecompile script
%global __python /opt/venvs/%{name}/bin/python3


%prep
%setup -q

%build
%pyvenv_create
%{__pyvenvpip3} install --upgrade pip
%pyvenv_build

%install
%pyvenv_create
%{__pyvenvpip3} install --upgrade pip
%pyvenv_install


%files
%doc README.md LICENSE
/opt/venvs/%{name}/*
```

In Fedora 29, I also had to add the following to the spec file.

```
# Fedora 27 and newer, no need to build the debug package
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%global debug_package %{nil}
%endif
```

We really don't need the debug package here, as the wheels are already compiled.

You can find more examples in the `examples` directory in the git repository.

### Installing the executable(s)

Remember to install all of the executable(s) installed under virtualenv into
`/usr/bin/` or similar directory by creating symlinks.


### Available macros

The following are the available macros/variables:

#### %__pyvenv_root

This points to the directory where the virtualenv has been created. Right now
the default path is `/opt/venvs/projectname`.

#### %__pyvenv

The Python interpreter installed in the virtualenv.

#### %__pyvenvpip3

The `pip3` tool installed in the virtualenv.


#### %pyvenv_create()

This is the macro which creates the actual virtualenv. We have to call it twice
in both `%build` and `%install`section, because rpmbuild tool deletes the
buildroot after `%build` and recreates it in `%install` section.

#### %pyvenv_build()

Use this macro to build the wheel for the project we are packaging.

#### %pyvenv_install()

Use this macro install the wheel we built into the RPM buildroot.


## License: GPLv3+
