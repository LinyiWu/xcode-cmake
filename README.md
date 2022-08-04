# Xcode-cmake

A command line tool which extracts build configurations for cmake, from existing xcode project.

## Usage

Using [hello](hello) in this repository as an example.

```bash
cd /path/to/this/repo
```

Generate cmake files from xcode project.pbxproj

```bash
mkdir -p cmake/
plutil -convert json -o cmake/project.json hello/project.pbxproj
./xcode-cmake.py -i cmake/project.json -o cmake/
```

It generates project-level build settings to `cmake/xcode_attr.cmake`, and target-level build settings to `cmake/${targetName}.cmake`. These files are included by [CMakeLists.txt](CMakeLists.txt).

Then generate xcode project files using cmake.

```bash
mkdir -p build/
cmake -GXcode -S ./ -B build/
```

**NOTE**:
+ [project.pbxproj](hello/project.pbxproj) refers to `Info.plist` by relative path(`hello/Info.plist`), so the generated `cmake/hello.cmake` behaves the same. Put `CMakeLists.txt` in the parent directory of `hello` if you want to include target-level cmake files.

## Why another xcode/ios cmake tool

I hope cmake generated projects have xcode-default warnings enabled (see Xcode -> PROJECT -> Build Settings -> Apple Clang - Warnings).
