NAME REMOVED
============

This is the Django source for the comic website `Name Removed <http://nameremoved.com/>`_.

It used to live at `google code <http://code.google.com/p/nameremoved/>`_ ...

Some Things Have Changed
------------------------

- slug field in contributor
- height and width names in comic
- contribution with null contributor should instead be 666
- also add the following to the dumpdata::
    {
      "pk": 666,
      "model": "contributions.contributor",
      "fields": {
          "info": "Nothing special.",
          "name": "None",
          "slug": "none"
      }
    },

How To Update
-------------

- run convertjson.sh on a recent dumpdata
- run python manage.py sqlflush | python manage.py dbshell
- You have to create the chunks yourself from your old templates
- You have to manually convert your Extra pages into flatpages. Sucks, I know!
