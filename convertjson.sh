#!/usr/bin/sed -f
# converts the pre-Django1.0 version of the dumpdata to one that
# is compatible with the new version.

# NOTA BENE
# you have to MANUALLY convert the EXTRA pages into flatpages

# ALSO you have to delete the random_image entries by hand

# adds the "None" contributor to the database
2i\
{\
  "pk": 666,\
  "model": "contributions.contributor",\
  "fields": {\
      "info": "Nothing special.",\
      "name": "None",\
      "slug": "none"\
  }\
},
s/comics.contributor/contributions.contributor/
s/comics.contribution/contributions.contribution/
s/"contributor": null/"contributor": 666/
s/"comic_height"/"height"/
s/"comic_width"/"width"/
