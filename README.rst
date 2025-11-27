=======
PyCorec
=======

| Python Coordinates Recoder for Sequence Images (PyCorec)

| Version 2.1.0 (2025-11-28)

| PyCorec is a python GUI application that can read images with sequential numbers in the same file name, display them in numerical order, and record the coordinate points on the image using mouse operations.

.. image:: docs/images/gui.png
   :alt: gui

Installation: how to install PyCorec
------------------------------------
| pycorec is available on PyPI. You can install it with pip

::

    pip install pycorec


Update
------
| pycorec is available on PyPI. You can update it with pip

::

    pip install --upgrade pycorec


How to use
----------

Naming of image data🖼️
"""""""""""""""""""""""
* When using sequential images in a time series, please add a sequential number to the end of the file name of the image data.
* This is not necessary when loading a video file.
* It is recommended that the images to be analyzed be placed under a single directory to be loaded at a time.
* Supports **.jpg, .png, .tiff, .bmp** image extensions.
* If the file name contains **"Bkg" and "Sub"**, the image will not be loaded.
* For time-series images, prepare files with the same file name followed by a number, so that the images with the lowest number are read in order.

  Example:

  * ``picture_001.jpg``, ``picture_002.jpg``, ...
  * ``pic-1.jpg``, ``pic-2.jpg``, ...
  * ``syashin1.jpg``, ``syashin2.jpg``, ...
  * ``mov_202308231159.jpg``, ``mov_202308231201.jpg``, ...
  * ``e 43.jpg``, ``e 47.jpg``, ...
  * ``Shashin (1).jpg``, ``Shashin (2).jpg``, ...

Launch the application💻
""""""""""""""""""""""""
| Enter :code:`pycorec` or :code:`python -m pycorec` in a terminal in a python environment where pycorec is installed.

::

    pycorec

::

    python -m pycorec


Loading data📥
""""""""""""""
* Select one of the modes from the buttons on the right

  * Video capture (reads frames in the video)
  * Directory Selection (reads all images in a directory)
  * Bounded Selection (selects a range of images to load)
  * Click Selection (selectively load images)

  .. image:: docs/images/open.png
     :alt: open

  .. image:: docs/images/directory.png
     :alt: directory

* In the above three modes, a dialog box for setting the frame interval appears.

  * 1 for sequential loading, 2 for skipping one.

  .. image:: docs/images/interval.png
     :alt: interval

* Optional settings

  * Entering "fps" (frames per second, the reciprocal of the frame interval) creates a column of relative time (s).

  .. image:: docs/images/fps.png
     :alt: fps

  * If you enter cm/px (value at 100% image size), which indicates how many centimeters one px on the image corresponds to in reality, a value converted to the coordinate cm will be output.

    * If there is an object of known size on the image, it can be calculated by first reading only one image, taking a point, and dividing the distance between the two points (cm) by the difference in coordinates (px) for each x and y.

  .. image:: docs/images/cmpx.png
     :alt: cmpx

Change the screen display size📺
""""""""""""""""""""""""""""""""
* By default, the image is displayed at the largest size that fits the screen.
* 🔍 Zoom

  * Mouse wheel up: zoom in
  * Mouse wheel down: zoom out
  * Zoom centers on the mouse cursor

* 🖱️ Pan

  * Hold Space + drag: pan the image
  * Cursor changes to a fleur during panning

* Press "Reset to Window Size" to return to the initial size and position.
* Press "Fit image to Actual size" to display the image at 100% of its original size.
* Press "Toggle Fullscreen" to switch between fullscreen and windowed mode.
* The zoomed state is maintained and the image is moved to the next image.
* **Image coordinates are converted to the value at 100% image size no matter what size the image is displayed.**

.. image:: docs/images/size.png
   :alt: size

Record the coordinates 🖱️
"""""""""""""""""""""""""
* Left-click to record coordinates.
* Right-click to cancel the previous record in the same image.
* When you press Shift + Left-click, NaN coordinates are recorded as missing values, and the next point in the same image can be recorded.
* The point where the coordinates were acquired is displayed as a red dot.
* The number of points recorded in the image is displayed as "Record Points" in the bar at the bottom.
* When the recording of coordinates in an image is finished, press the right arrow key (→) to move to the next image.
* Press the left arrow key (←) to go back to the previous image.
* The title bar at the top displays the image number / total number of images and the name of the image file currently being displayed.
* The coordinates of the mouse position and other information are displayed at any time at the bottom of the screen.

.. image:: docs/images/record.png
   :alt: record

Save the coordinate data 💾
""""""""""""""""""""""""""
* When recording is finished with the last image, press → again to open the file save screen.
* Or press "Save as..." in the lower right corner to save the data up to that point.
* To interrupt coordinate recording, press "Save as..." to output the coordinate recording file, and when resuming, press "Resume Recording" to read the file you have just output.
* If the path to the image file changes, it cannot be loaded. In the case of video, the output image file is referenced. Please correct the ``Filepath`` column in the coordinate record file using the Replace function, etc., and then read the file again.
* Output file can be selected from xlsx or csv.

  .. image:: docs/images/save.png
     :alt: save dialog

* Image coordinate px is the origin at the upper left of the image, x-axis is positive rightward, and y-axis is positive downward as per the standard.
* When outputting in physical coordinates cm, the origin is the upper left corner of the image, the x-axis is positive rightward, and the y-axis is positive upward.

  * For the position on the image, x: positive value (cm), y: negative value (cm).

.. image:: docs/images/coordinates.png
   :alt: coordinates


Release
-------
See the full changelog here:
https://github.com/tnku10/pycorec/blob/main/CHANGELOG.md

Future update
-------------
(Planned features will be documented here in future releases.)

Credits
-------
| Programmed by Yuto Tanaka

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
