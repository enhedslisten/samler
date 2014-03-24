# Samler

Samler is an app for gathering and showcasing social media content. It periodically searches social media content tagged with certain keywords and saves them locally to a sqlite db. Users are presented with a view of the latest content. It is currently under development.

## Admin

Samler has an in-progress admin view. This allows admin users to hide irrelevant content. Admin users must be defined in the config.ini file.

## Deploy

In order to deploy Samler, save all the files locally in an area accessible to your web server. Create a copy of config.ini.example called config.ini. Populate the users section with the names and passwords of your admin users in the style `<username>: password`. Next generate the secret key and save it to the relevant field in config.ini.
Using a python console:
  import os
  os.urandom(24)
 