# -*- coding: utf-8 -*-
import os
from io import open
import shutil

from markdown2 import markdown
from jinja2 import FileSystemLoader, Environment


# path to the directories for your content, templates and where to put the
# generated site.
CONTENT_DIR = "content"
TEMPLATE_DIR = "."
SITE_DIR = "site"

SITE = {}  # directory for posts (key = name, value = content)

# STEP 1 - read files
for current in os.listdir(CONTENT_DIR):
    fqp = os.path.join(CONTENT_DIR, current)

    with open(fqp, 'r', encoding='utf-8') as infile:
        SITE[current] = infile.read()


# STEP 2 - markup
for post in SITE:
    SITE[post] = markdown(SITE[post])


# STEP 3 - template
SITE["index.html"] = ""

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

for post in SITE:
    template = env.get_template("template.html")
    SITE[post] = template.render(
        content=SITE[post],
        site=SITE
    )


# STEP 4 - write
# remove output directory if it exists
if os.path.exists(SITE_DIR):
    shutil.rmtree(SITE_DIR)

# create empty output directory
os.makedirs(SITE_DIR)

for post in SITE:
    fqp = os.path.join(SITE_DIR, post)

    with open(fqp, "w", encoding="utf-8") as output:
        output.write(SITE[post])

print "Done!"
