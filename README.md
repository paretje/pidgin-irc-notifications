Requirements
============
* libnotify
* pynotify

Install
=======
`sudo python setup.py install`

Running
=======
After installation run:

`pidgin-irc-notify &`

This will enable notifications in pidgin for all irc channels.  For further documentation run:

`pidgin-irc-notify -h`

But How?
--------
This little script uses dbus to listen for events and fires off callbacks to functions.
