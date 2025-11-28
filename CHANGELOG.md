# Changelog
All notable changes to this project will be documented in this file.

## [2.1.2] - 2025-11-28
### Fixed
-adjust dependencies for Python 3.13.9

## [2.1.1] - 2025-11-28
### Fixed
- Picture drawing smoothing issue

## [2.1.0] - 2025-11-28
### Added
- Mouse-wheel zooming
- Space + drag panning
- Navigation help panel in sidebar

### Changed
- Removed manual zoom spinbox
- Removed ArrowButton panning
- Improved fullscreen toggle behavior
- Simplified & Modernized Right-Side Panel

### Fixed
- Coordinate drawing after zoom/pan
- Offset calculation stability

## Version 2.0.9 (2025-11-27)

* Removed the “always on top” behavior and added a toggle button for fullscreen display instead.
* Fixed an issue where recorded pixel coordinates became non-integers when converting from zoomed view to original image coordinates; coordinates are now rounded and stored as integer pixel values.
* Optimized the display of zoom levels to show more user-friendly values.
* Updated the codebase to work with the latest versions of Python and required libraries.


## Version 2.0.8 (2023-11-30)

* Add image transition button and remove usage instructions text.

## Version 2.0.7 (2023-11-30)

* Enable to read video and get frames.
* Added a function to resume recording based on the information in the coordinate recording file saved after interrupting recording in the middle.

## Version 2.0.6 (2023-10-31)

* Fixed to be able to run from terminal.

## Version 2.0.5 (2023-10-30)

* Release on pypi

## Version 2.0.4 (2023-09-15)

* Add mouse wheel click function to record nan position

## Version 2.0.3 (2023-08-07)

* cm/px can now be specified separately for x and y.
* If x=y, the same value must be entered for both, and no conversion will be performed unless valid values are entered for both xy and y.
* The number of record points in the displayed image is displayed as Record points in the bottom bar.
* Fixed a problem in which the screen would overflow when connected to multiple monitors with a magnification factor other than 100%.
* When Excel output is selected, the following settings are available.
* (Old) Vertical sheet of time-series changes per point +
* (New) a sheet of spatial distribution of multiple points per time frame, arranged vertically.

## Version 2.0.2 (2023-07-04)

* Bug fixes and UI improvements
* published on GitHub https://github.com/tnku10/pycorec

  **UI**
* Moved image number/number of all images loaded & the name of the currently displayed image file from the bottom to the title bar.
* Simplified button descriptions.
* To prevent accidental operation, the mouse wheel zoom has been removed and replaced with a + - numerical value box.
* The zoom size of the image display can now be specified numerically.
* The image display zoom size can now be specified numerically.

  **Bug Fix**
* Fixed a bug that the dialog box is not displayed when the file specification is canceled.
* Fixed a bug that a point can't be typed before an image is displayed.
* Fix - Cannot return to the previous image from the first image.
* Fixed so that coordinate records are maintained correctly even if you go back to the previous image, and display dots of record points are also maintained.

  **Output File**
* Fonts of output file are changed to Segoe UI for better viewing, columns of File name are added, image size is added, and xlsx and csv are selectable.

## Version 2.0.1 (2023-06-27)

* GUI modernized to allow zooming in and out, moving the image forward and backward
* GUI engine changed from tkinter to customtkinter
* Changed image processing engine from opencv to pillow.
* Changed so that a dot is drawn on the image when clicked.

## Version 1.0.6 (2022-02-24)

* Changed so that pressing the key does not move to the next image unless one point per image is recorded for the second and subsequent images. (This is a measure to avoid a situation in which the user presses a key to move on without clicking and cannot return to the previous image, but must start over from the beginning.)

## Version 1.0.5 (2022-02-03)

* Added functions to input frame rate (fps) and physical coordinate conversion scale (cm/px) values, and to output physical coordinates (cm) and relative time (s) in the y-axis forward downward direction.
* Changed reading mode to A "Folder selection (batch selection of images in folder)", B "File selection (continuous range selection)", and C "File selection (multiple and arbitrary selection possible)".
* Enabled to load images with a specified frame interval for any continuous range in folder B in addition to A.

## Version 1.0.4 (2022-02-02)

* Limit the number of rows and columns of the data frame displayed when clicking on an image to only 3 rows and 6 columns (x,y for 3 points).

## Version 1.0.3 (2022-02-01)

* Changed so that images containing "Bkg" in the file name are not loaded.
* Changed so that csv can be saved before force close
* Changed so that the csv save screen is displayed after all images are displayed.
* Changed the skip number specification e.g.) If the number of images to load is 001,003,005, the skip number is > 2.

## Version 1.0.2 (2022-02-01)

* Added support for file paths containing Japanese characters (modified to read via Numpy)
* Add real-time mouse position image coordinate display function
* Add image skip reading mode
* Added ability to specify image magnification

## Version 1.0.1 (2022-01-28)

* First release
