### Etsy Shop Trends Search Tool ###

This Flask web application runs a webserver at localhost:5000.  This server
displays an interface which allows the user to input any number of
Etsy shops as a comma-separated list.  Then after clicking "Search" the top
five words (based on titles and descriptions of all shop items) will be
displayed for each shop.  Please be patient as the default search takes 15-20
seconds to run.

#### How to run: ####
$ python app.py
Visit http://localhost:5000 in a browser