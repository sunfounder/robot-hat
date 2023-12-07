.. _class_tts:

class ``TTS``
==================================================

.. warning::
    * You need to add ``sudo`` when running this script, in case the speaker doesn't work.
    * :ref:`faq_speaker`.

**Example**

.. code-block:: python

    # Import TTS class
    from robot_hat import TTS

    # Initialize TTS class
    tts = TTS(lang='en-US')
    # Speak text
    tts.say("Hello World")
    # show all supported languages
    print(tts.supported_lang())


**API**

.. currentmodule:: robot_hat

.. autoclass:: TTS
    :show-inheritance:
    :special-members: __init__
    :members:
