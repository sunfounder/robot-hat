from robot_hat.tts import Piper

tts = Piper()

# tts.set_model('en_US-amy-low')
# tts.say("Hi, I'm piper TTS. A fast and local neural text-to-speech engine that embeds espeak-ng for phonemization.")

tts.set_model('zh_CN-huayan-x_low')
tts.say("滴滴滴！紧急插播一条“贴身警报”！我的超声波小雷达正疯狂闪烁——前方仅6.56cm！这距离都快能和障碍物“手拉手”跳圆圈舞了，比我的车轮直径（悄悄说：约5cm）还近一丢丢呢～ 作为全身铝合金打造的“精致小车”，可不能让小碰撞留下“战斗勋章”，立刻启动“抵抗防御模式”！🤖🛡️")
