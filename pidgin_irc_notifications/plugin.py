#!/usr/bin/python3
"""
Copyright (C) 2012 Aaron Godfrey.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse
import dbus
import dbus.mainloop.glib
import gobject
import pynotify


class IRCNotificationPlugin(object):
    """
    Pidgin IRC Notification 'plugin'
    """
    def __init__(self, args):
        self.verbose = args.verbose

        bus = dbus.SessionBus()
        # Add sginal receiver for irc chat msg
        bus.add_signal_receiver(self.received_chat_msg_callback,
                                dbus_interface="im.pidgin.purple.PurpleInterface",
                                signal_name="ReceivedChatMsg")

        # Get the pidgin purple interface
        obj = bus.get_object("im.pidgin.purple.PurpleService",
                             "/im/pidgin/purple/PurpleObject")
        self.purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

    def received_chat_msg_callback(self, account, sender, message, conversation, flags):
        """
        Creates a notification for IRC channel message if in one of the
        approved channels.
        """
        try:
            # username in format user@irc.someserver.net
            username = self.purple.PurpleAccountGetUsername(account).split('@')[0]
        except IndexError:
            print("Whoops...username wasn't in expected format...")
            return
        channel = self.purple.PurpleConversationGetTitle(conversation)
        if channel.startswith('#') and username != sender \
                and message.find(username) == -1:
            msg = "%s said: %s" % (sender, message)
            if self.verbose:
                print(msg)
            pynotify.Notification(channel, msg).show()


def parse_args():
    parser = argparse.ArgumentParser(description="Enables notifications in"
                                     " irc channels provided in Pidgin.")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False, help="Enables verbose mode.")
    args = parser.parse_args()
    return args


def main():
    """
    Runs main loop and sets up listener
    """
    # Get command line args
    args = parse_args()

    # Initialize pynotify
    pynotify.init('Initializing IRC Notifications...')

    # Setup dbus glib mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # Init plugin
    IRCNotificationPlugin(args)

    # Obtain main loop and run it
    gobject.MainLoop().run()


if __name__ == "__main__":
    main()
