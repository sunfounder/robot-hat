Þ    L      |              Ü     Ý     å  V   ñ  j   H  T   ³  F     H   O          ¦     Á     á          !     1  %   G     m     z       ­   ¡     O     f     y          ¨     º     Ç     Ö     ê  =   ÿ     =	  
   P	     [	     y	     	  	   ®	  2   ¸	     ë	     ò	     
     
     )
     1
     ?
     _
     t
     
     
     ª
     ¬
     ®
     °
  {   Ç
     C     U     f            U   ¨  ?   þ  ?   >  =   ~  !   ¼  *   Þ     	     !  2   8  -   k          ¬  N   È       ,   '     T  &   f  T       â     d     l  s   t     è  v     m   ÷  L   e     ²  4   Ð  :     :   @  :   {     ¶  '   Í  &   õ          /     B  ê   ^     I     e  6        ¶     Ð     ì     ÿ          4  o   S     Ã     â  $   ò  -     0   E     v  ?        Ï     Ö     ö       	   %     /  0   B     s          ­     É     æ     è     ê     ì  ®        ²     È     Ý     ü       p   +  X     W   õ  S   M  -   ¡  E   Ï  -     *   C  [   n  /   Ê     ú  <     g   S  	   »  1   Å     ÷  0        5   **API** **Example** **Exclusive Previews**: Get early access to new product announcements and sneak peeks. **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team. **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions. **Learn & Share**: Exchange tips and tutorials to enhance your skills. **Special Discounts**: Enjoy exclusive discounts on our newest products. **Why Join?** 3 channel Grayscale Module ADC object or int for channel 0 ADC object or int for channel 1 ADC object or int for channel 2 ADXL345 modules Active buzzer beeping Bases: :py:class:`~robot_hat.i2c.I2C` Common anode Common cathode Get Set reference value Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts. Imports and initialize Initialize ADXL345 Initialize Grayscale Module Initialize RGB LED Initialize buzzer Left Channel Middle Channel PWM object for blue PWM object for green PWM object for passive buzzer or Pin object for active buzzer PWM object for red Parameters Passive buzzer Manual control Passive buzzer Simple usage Play a song! Baby shark! Play freq RGB_LED.ANODE or RGB_LED.CATHODE, default is ANODE Raises Read an axis from ADXL345 Read line status Return type Returns Right Channel Set frequency of passive buzzer Simple 3 pin RGB LED Turn off buzzer Turn on buzzer Write color to RGB LED X Y Z address of the ADXL345 channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT class ``ADXL345`` class ``Buzzer`` class ``Grayscale_Module`` class ``RGB_LED`` class ``Ultrasonic`` color to write, hex string starts with "#", 24-bit int or tuple of (red, green, blue) duration of each note, in seconds, None means play continuously freq to play, you can use Music.note() to get frequency of note frequency of buzzer, use Music.NOTES to get frequency of note if common is not ANODE or CATHODE if r_pin, g_pin or b_pin is not PWM object if set to active buzzer list of grayscale data list of grayscale datas, if None, read from sensor list of line status, 0 for white, 1 for black module ``modules`` read a channel or all datas read value(g) of an axis, ADXL345.X, ADXL345.Y or ADXL345.Z, None for all axis reference value reference value, None to get reference value reference voltage value of the axis, or list of all axis ð Ready to explore and create with us? Click [|link_sf_facebook|] and join today! Project-Id-Version: SunFounder Robot HAT 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2024-05-24 09:22+0800
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ja
Language-Team: ja <LL@li.org>
Plural-Forms: nplurals=1; plural=0;
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.15.0
 **API** **ä¾** **ç¬å çãªãã¬ãã¥ã¼**ï¼æ°è£½åã®çºè¡¨ãåè¡ãã¬ãã¥ã¼ã«æ©æã¢ã¯ã»ã¹ãã¾ãããã **ã¨ã­ã¹ãã¼ããµãã¼ã**ï¼ã³ãã¥ããã£ããã¼ã ã®å©ããåãã¦ãè²©å£²å¾ã®åé¡ãæè¡çãªèª²é¡ãè§£æ±ºãã¾ãã **ç¥­ãã®ãã­ã¢ã¼ã·ã§ã³ã¨ã®ãã**ï¼ã®ãããç¥æ¥ã®ãã­ã¢ã¼ã·ã§ã³ã«åå ãã¾ãããã **å­¦ã³ï¼å±æ**ï¼ãã³ãããã¥ã¼ããªã¢ã«ãäº¤æãã¦ã¹ã­ã«ãåä¸ããã¾ãããã **ç¹å¥å²å¼**ï¼ææ°è£½åã®ç¬å å²å¼ããæ¥½ãã¿ãã ããã  **åå ããçç±ã¯ï¼** 3ãã£ã³ãã«ã°ã¬ã¼ã¹ã±ã¼ã«ã¢ã¸ã¥ã¼ã« ãã£ã³ãã«0ç¨ã®ADCãªãã¸ã§ã¯ãã¾ãã¯æ´æ° ãã£ã³ãã«1ç¨ã®ADCãªãã¸ã§ã¯ãã¾ãã¯æ´æ° ãã£ã³ãã«2ç¨ã®ADCãªãã¸ã§ã¯ãã¾ãã¯æ´æ° ADXL345ã¢ã¸ã¥ã¼ã« ã¢ã¯ãã£ããã¶ã¼ã®ãã¼ãé³ åºåº: :py:class:`~robot_hat.i2c.I2C` å±éã¢ãã¼ã å±éã«ã½ã¼ã åºæºå¤ã®åå¾ã¨è¨­å® ããã«ã¡ã¯ãSunFounderã®Raspberry Pi & Arduino & ESP32æå¥½å®¶ã³ãã¥ããã£ã¸ããããï¼Facebookä¸ã§Raspberry PiãArduinoãESP32ã«ã¤ãã¦ãã£ã¨æ·±ãæãä¸ããä»ã®æå¥½å®¶ã¨äº¤æµãã¾ãããã ã¤ã³ãã¼ãã¨åæå ADXL345ãåæåãã ã°ã¬ã¼ã¹ã±ã¼ã«ã¢ã¸ã¥ã¼ã«ãåæåãã RGB LEDãåæåãã ãã¶ã¼ãåæåãã å·¦ãã£ã³ãã« ä¸­å¤®ãã£ã³ãã« éç¨ã®PWMãªãã¸ã§ã¯ã ç·ç¨ã®PWMãªãã¸ã§ã¯ã ããã·ããã¶ã¼ç¨ã®PWMãªãã¸ã§ã¯ãã¾ãã¯ã¢ã¯ãã£ããã¶ã¼ç¨ã®ãã³ãªãã¸ã§ã¯ã èµ¤ç¨ã®PWMãªãã¸ã§ã¯ã ãã©ã¡ã¼ã¿ ããã·ããã¶ã¼ã®æåå¶å¾¡ ããã·ããã¶ã¼ã®ç°¡åãªä½¿ç¨æ¹æ³ æ²ãæ¼å¥ããï¼ãã¤ãã¼ã·ã£ã¼ã¯ï¼ å¨æ³¢æ°ãæ¼å¥ãã RGB_LED.ANODEã¾ãã¯RGB_LED.CATHODEãããã©ã«ãã¯ANODE ä¾å¤ ADXL345ããè»¸ãèª­ã¿åã ã©ã¤ã³ç¶æã®èª­ã¿åã æ»ãå¤ã®å æ»ãå¤ å³ãã£ã³ãã« ããã·ããã¶ã¼ã®å¨æ³¢æ°ãè¨­å®ãã ã·ã³ãã«ãª3ãã³RGB LED ãã¶ã¼ããªãã«ãã ãã¶ã¼ããªã³ã«ãã RGB LEDã«è²ãæ¸ãè¾¼ã X Y Z ADXL345ã®ã¢ãã¬ã¹ èª­ã¿åããã£ã³ãã«ããã¹ã¦ãèª­ã¿åãã«ã¯ç©ºã®ã¾ã¾ã«ããã0ã1ã2ã¾ãã¯Grayscale_Module.LEFTãGrayscale_Module.CENTERãGrayscale_Module.RIGHT ã¯ã©ã¹ ``ADXL345`` ã¯ã©ã¹ ``Buzzer`` ã¯ã©ã¹ ``Grayscale_Module`` ã¯ã©ã¹ ``RGB_LED`` ã¯ã©ã¹ ``Ultrasonic`` æ¸ãè¾¼ãè²ã"#"ã§å§ã¾ã16é²æ°æå­åã24ãããæ´æ°ãã¾ãã¯(red, green, blue)ã®ã¿ãã« åé³ç¬¦ã®æç¶æéï¼ç§ï¼ãNoneã¯é£ç¶ãã¦æ¼å¥ãããã¨ãæå³ãã æ¼å¥ããå¨æ³¢æ°ãMusic.note()ãä½¿ç¨ãã¦é³ç¬¦ã®å¨æ³¢æ°ãåå¾ã§ãã ãã¶ã¼ã®å¨æ³¢æ°ãMusic.NOTESãä½¿ç¨ãã¦é³ç¬¦ã®å¨æ³¢æ°ãåå¾ãã å±éãANODEã¾ãã¯CATHODEã§ãªãå ´å r_pinãg_pinãã¾ãã¯b_pinãPWMãªãã¸ã§ã¯ãã§ãªãå ´å ã¢ã¯ãã£ããã¶ã¼ã«è¨­å®ããå ´å ã°ã¬ã¼ã¹ã±ã¼ã«ãã¼ã¿ã®ãªã¹ã ã°ã¬ã¼ã¹ã±ã¼ã«ãã¼ã¿ã®ãªã¹ããNoneã®å ´åã¯ã»ã³ãµã¼ããèª­ã¿åã ã©ã¤ã³ç¶æã®ãªã¹ãã0ã¯ç½ã1ã¯é» ã¢ã¸ã¥ã¼ã« ``modules`` ãã£ã³ãã«ã¾ãã¯ãã¹ã¦ã®ãã¼ã¿ãèª­ã¿åã è»¸ã®å¤(g)ãèª­ã¿åããADXL345.XãADXL345.Yã¾ãã¯ADXL345.Zããã¹ã¦ã®è»¸ã®å ´åã¯None åºæºå¤ åºæºå¤ãåºæºå¤ãåå¾ããå ´åã¯None åºæºé»å§ è»¸ã®å¤ãã¾ãã¯ãã¹ã¦ã®è»¸ã®ãªã¹ã ð ç§ãã¡ã¨ä¸ç·ã«æ¢ç´¢ããåµé ããæºåã¯ã§ãã¦ãã¾ããï¼[|link_sf_facebook|]ãã¯ãªãã¯ãã¦ä»ããåå ãã¾ãããï¼ 