Downloads:
Download Brackets.1.5.Extract
Download bootstrap: http://getbootstrap.com/getting-started/#download
Font Awesome
Icons for Social Networkds

Tools:
 - Brackets: is an open source front-end IDE developed in JavaScript and CSS, by Adobe.

Read Full-Stack references:
Frameworks
 - Bootstrap is the most popular
 - Semantic UI is the most innovative (not open source?)

http-server
 - Engine X (nginx) is te most high performance

Full Stack JS frameworks:
 - Meteor
 - Node

Full-Stack
 - There is almost no full-stack developers, everybody is either front or back end.

Less and Sass
- preprocessors, input a macro language, to generate CSS
Less code is more compact and is used to write the source code of bootstrap css.


Web Tools
---------

Node and NPM
 - Node: the JavaScript engine of the Chome browser.
 - NPM: Node package manager

Yeoman toolset
Toolset to automate build, test, install.
The whole toolset is developed in JavaScript and runs on node, from command line.
To create build workflows.
- Yo: web app scafolding
- Bower: package manager for the web.
- Grunt/Gulp: task automation (test)



Bower
-----
Automates the process of downloading packages and installing them.
bower.json: contains all the instructions for the bower process.
bower init: command to create a new bower.json file with generic info about our project

The following 2 commands download and install packages (with all their dependencies), and update the bower.json file:
- bower install bootstrap -S
- bower install font-awesome -S

After the above, if we want to reinstall, we just run:
bower install
