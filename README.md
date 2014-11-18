TwitterMonitor
==============

[![Build Status](https://travis-ci.org/alissonperez/TwitterMonitor.svg)](https://travis-ci.org/alissonperez/TwitterMonitor) [![Coverage Status](https://coveralls.io/repos/alissonperez/TwitterMonitor/badge.png?branch=master)](https://coveralls.io/r/alissonperez/TwitterMonitor?branch=master)

A small open source library to create monitoring routines of any nature using direct messages (DM) of **Twitter**.

For each message send request, the library will take all the followers of configured account and send instantly a DM to each one.

There is an example bellow of a simple routine (RoutineTest class) that sends "A test message" to all of the followers of configured account in the dictionary *twitter_keys* in a minimum interval of 10 minutes between each notification.

```python
from twitter_monitor import core


# A simple routine example
class RoutineTest(core.Routine):

    name = "Rotina Test 1"
    short_name = "RT1"

    interval_minutes = 10  # You can put a execution interval in minutes

    def _execute(self):
        # Put your logic here
        self.notify("A test message...")


# Manage your keys and tokens on https://apps.twitter.com/
twitter_keys = {
    "consumer_key": "AaAaAaAaAaAaAaAaAaAaAaAaA",
    "consumer_secret": "AaAaAaAaAaAaAaAaAaAaAaAaAAaAaAaAaAaAaAaAaAaAaAaAaA",
    "access_token_key": "999999999-AaAaAaAaAaAaAaAaAaAaAaAaA",
    "access_token_secret": "AaAaAaAaAaAaAaAaAaAaAaAaAAaAaAaAaAaAaAaAaAaAaAaAaA",
}

# A list of routine classes
routines = [
    RoutineTest
]

core.ExecutorFactory(routines, twitter_keys).create_default().run()
```
