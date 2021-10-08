class ``TTS`` - text to speech
==============================

**Usage**

.. code-block:: python

       from robot_hat import *

       tts = TTS()                     # create a TTS object
       tts.say('hello')                # write word

       # tts.write('hi')                # write word
       tts.lang('en-GB')                # change language

       tts.supported_lang()            # return language

**Constructors**


``class robot_hat.TTS(engine)``: Create a TTS object, ``engine`` could be ``"espeak"`` as Espeak, ``"gtts"`` as Google TTS and ``polly`` as AWS Polly.

**Methods**


- ``say`` - Write word on TTS.

.. code-block:: python

       TTS.say(words)

-  ``lang`` - Change on TTS.

.. code-block:: python

       TTS.lang(language)

-  ``supported_lang`` - Inquire all supported language.

.. code-block:: python

       TTS.supported_lang()

-  parameter adjustment

.. code-block:: python

       # amp: amplitude, volume
       # speed: speaking speed
       # gap: gap
       # pitch: pitch
       def espeak_params(self, amp=None, speed=None, gap=None, pitch=None)

