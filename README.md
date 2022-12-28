###### **Web Scanner for No Controls Automations**

Since the past few years, there are quite a few standard ways in the industry how one can find a specific element on a page using Selenium. One could:

Search by the name of the tag,
Filter for a specific HTML class or HTML ID,
Use CSS selectors or XPath expressions
Problem Statement Description We need to identify controls without their properties of DOM or, Find components without searching the page source.

**Expected Outcome**

Target to build a repository of all the controls and elements on the webpage
Create a website with a grid listing the scanned objects
Give users the option to crop the element's area to ensure accurate identification
Provide the ability to scan missing elements, rename the controls or to use the controls to add new elements with their names
Write an API that returns all of these identified controls as webElements to consume the controls for automation in Java/.net/python

**Tools & Technologies Used**

Python
numpy
regular expressions
ovencv
pytesseract
Selenium: webdriver
Flask: render_template, redirect, url_for, request
SearchElement: get_website_data, custom_detection
sqlalchemy
bootstrap
json