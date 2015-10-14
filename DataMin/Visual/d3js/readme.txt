D3.js is an open source javascript library for data visualization
The data processing methods define a callback function, like jquery ajax() method.
D3 adds the implicit loops, you can apply a method to all the elements of the data just by defining the property .data()
To add D3 to a page, the best is to reference the D3 distribution URL directly, whithoud downloading it locally.

D3 Development on Ubuntu with Chromium and WebKit.
To debug D3 and javascript in general, the best is to use the Web Kit environmnet. This is a debugger embedded inside some browsers.
Only Chrome and IE have it, neither run on Linux, so you need Chromium, the linux clone of Chrome. 
Gedit is enough to edit the hetml pages.
In order to allow chromium to read datasets from local files; it must be launched from a terminal, as follows:

chromium-browser --allow-file-access-from-files

HTML pages with D3 javascript can be uploaded to the Forge hosting site, like AdSar.forge.io

Data
D3.js can read a tabilar dataset from a CSV or a TSB file. It can also read json.

readgml
There are many dataset published in Graph Markup Language (not XML), which is similar to Jason in that defines objects and properties hierarchically.
To process these datasets first you need to convert the data to TSB.
I downloaded a GML parser written in C called "readgml" and added a function to output the network in TSB format.



