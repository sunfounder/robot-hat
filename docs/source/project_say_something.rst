Say Something
====================


In this section, you'll learn how to convert text into speech and have Robot HAT speak it aloud.

**Steps**

#. We retrieve text from the command line to enable Robot HAT to articulate it. To achieve this, save the following code as a ``.py`` file, such as ``tts.py``.


    .. code-block:: python

        import sys
        from robot_hat import TTS

        # Check if there are enough command line arguments
        if len(sys.argv) > 1:
            text_to_say = sys.argv[1]  # Get the first argument passed from the command line
        else:
            text_to_say = "Hello SunFounder"  # Default text if no arguments are provided

        # Initialize the TTS class
        tts = TTS(lang='en-US')

        # Read the text
        tts.say(text_to_say)

        # Display all supported languages
        print(tts.supported_lang())

#. To make Robot HAT vocalize a specific sentence, you can use the following command: ``sudo python3 tts.py "any text"`` - simply replace ``"any text"`` with the desired phrase.

    .. note::

        * :ref:`faq_speaker`

