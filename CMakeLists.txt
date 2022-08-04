cmake_minimum_required(VERSION 3.20)
set(CMAKE_SYSTEM_NAME iOS)
include(${CMAKE_SOURCE_DIR}/cmake/xcode_attr.cmake)

set(MYNAME "hello")

project(${MYNAME} VERSION 1.2.3
  LANGUAGES C CXX OBJC OBJCXX
)

set(GROUP_SOURCES
  hello/AppDelegate.h
  hello/AppDelegate.m
  hello/SceneDelegate.h
  hello/SceneDelegate.m
  hello/ViewController.h
  hello/ViewController.m
  hello/main.m
)

set(GROUP_RESOURCES
  hello/Assets.xcassets
  hello/Base.lproj/LaunchScreen.storyboard
  hello/Base.lproj/Main.storyboard
)
set_source_files_properties(${GROUP_RESOURCES} PROPERTIES
  MACOSX_PACKAGE_LOCATION Resources
)

add_executable(${MYNAME} MACOSX_BUNDLE
  ${GROUP_SOURCES}
  ${GROUP_RESOURCES}
)

include(${CMAKE_SOURCE_DIR}/cmake/${MYNAME}.cmake)
