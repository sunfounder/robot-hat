from .utils import enable_speaker, disable_speaker
import os
import pyaudio
import soundfile as sf
import librosa
import numpy as np
import threading
import time
from uuid import uuid4  # 用于生成唯一播放ID

class Speaker:
    def __init__(self):
        # 初始化喇叭状态
        self.speaker_enabled = False
        self.enable_speaker()  # 启动时开启喇叭
        
        # 初始化音频系统
        self.pa = pyaudio.PyAudio()
        
        # 播放任务管理（ID -> 播放信息）
        self.play_tasks = {}  # 格式: {id: {stream, thread, is_playing, position, total_frames, samplerate}}
        self.task_lock = threading.Lock()  # 线程安全锁
        
        # 支持的格式
        self.supported_formats = {
            'wav': {'handler': 'soundfile'},
            'flac': {'handler': 'soundfile'},
            'ogg': {'handler': 'soundfile'},
            'mp3': {'handler': 'librosa'},
            'm4a': {'handler': 'librosa'},
            'aac': {'handler': 'librosa'},
            'wma': {'handler': 'librosa'}
        }

    def __del__(self):
        # 销毁时关闭喇叭和音频资源
        self.disable_speaker()
        self.pa.terminate()
        
        # 停止所有播放任务
        with self.task_lock:
            for task_id in list(self.play_tasks.keys()):
                self.stop(task_id)

    def enable_speaker(self):
        """开启喇叭"""
        if not self.speaker_enabled:
            enable_speaker()
            self.speaker_enabled = True

    def disable_speaker(self):
        """关闭喇叭"""
        if self.speaker_enabled:
            disable_speaker()
            self.speaker_enabled = False

    def _get_handler(self, file_path):
        """获取文件处理方式"""
        ext = os.path.splitext(file_path)[-1].lower().lstrip('.')
        if ext not in self.supported_formats:
            raise ValueError(f"不支持的格式：{ext}，支持格式：{list(self.supported_formats.keys())}")
        return self.supported_formats[ext]['handler']

    def _read_audio(self, file_path, handler):
        """读取音频数据"""
        if handler == 'soundfile':
            data, samplerate = sf.read(file_path)
        else:  # librosa
            data, samplerate = librosa.load(file_path, sr=None, mono=False)
            if data.ndim > 1:
                data = data.T  # 转置为(帧数, 声道数)
        return data.astype(np.float32), samplerate

    def _play_background(self, task_id, data, samplerate, channels):
        """后台播放线程函数"""
        try:
            # 打开音频流
            stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=channels,
                rate=samplerate,
                output=True
            )

            # 更新任务信息
            with self.task_lock:
                self.play_tasks[task_id].update({
                    'stream': stream,
                    'is_playing': True,
                    'position': 0,
                    'total_frames': len(data),
                    'samplerate': samplerate
                })

            chunk_size = 1024
            task = self.play_tasks[task_id]

            # 播放循环
            while task['position'] < len(data) and task['is_playing']:
                # 检查暂停状态
                while not task['is_playing']:
                    time.sleep(0.1)
                    if task.get('stopped', False):
                        break

                if task.get('stopped', False):
                    break

                # 计算当前块
                end = min(task['position'] + chunk_size, len(data))
                chunk = data[task['position']:end]
                
                # 处理单声道
                if channels == 1 and len(chunk.shape) == 1:
                    chunk = np.expand_dims(chunk, axis=1)

                # 播放
                stream.write(chunk.tobytes())
                
                # 更新位置
                with self.task_lock:
                    task['position'] = end

        except Exception as e:
            print(f"播放错误 (ID: {task_id}): {str(e)}")
        finally:
            # 清理资源
            with self.task_lock:
                if task_id in self.play_tasks:
                    stream = self.play_tasks[task_id].get('stream')
                    if stream:
                        stream.stop_stream()
                        stream.close()
                    del self.play_tasks[task_id]

    def play(self, file_path):
        """
        后台播放音频并返回唯一ID
        :return: 播放任务ID（字符串）
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        # 读取音频数据
        handler = self._get_handler(file_path)
        data, samplerate = self._read_audio(file_path, handler)
        channels = data.shape[1] if len(data.shape) > 1 else 1

        # 生成唯一ID
        task_id = str(uuid4())

        # 初始化任务信息
        with self.task_lock:
            self.play_tasks[task_id] = {
                'is_playing': False,
                'position': 0,
                'thread': None,
                'stopped': False
            }

        # 创建并启动播放线程
        thread = threading.Thread(
            name=f"play_background_{task_id}",
            target=self._play_background,
            args=(task_id, data, samplerate, channels),
            daemon=True
        )
        thread.start()

        # 记录线程信息
        with self.task_lock:
            self.play_tasks[task_id]['thread'] = thread

        return task_id

    def get_progress(self, task_id):
        """
        获取播放进度
        :return: 字典包含 position(当前帧数), total(总帧数), progress(0-1), time(秒)
        """
        with self.task_lock:
            if task_id not in self.play_tasks:
                raise ValueError(f"无效的播放ID：{task_id}")
            
            task = self.play_tasks[task_id]
            total = task['total_frames']
            position = task['position']
            samplerate = task['samplerate']
            
            return {
                'position': position,
                'total': total,
                'progress': position / total if total > 0 else 0,
                'time': position / samplerate if samplerate > 0 else 0,
                'total_time': total / samplerate if samplerate > 0 else 0,
                'is_playing': task['is_playing']
            }

    def pause(self, task_id):
        """暂停播放"""
        with self.task_lock:
            if task_id not in self.play_tasks:
                raise ValueError(f"无效的播放ID：{task_id}")
            self.play_tasks[task_id]['is_playing'] = False

    def resume(self, task_id):
        """恢复播放"""
        with self.task_lock:
            if task_id not in self.play_tasks:
                raise ValueError(f"无效的播放ID：{task_id}")
            self.play_tasks[task_id]['is_playing'] = True

    def stop(self, task_id):
        """停止播放并清理资源"""
        with self.task_lock:
            if task_id not in self.play_tasks:
                return False  # 已停止或不存在
            
            task = self.play_tasks[task_id]
            task['is_playing'] = False
            task['stopped'] = True

        # 等待线程结束
        task['thread'].join(timeout=1.0)
        return True

    def list_tasks(self):
        """列出所有活跃的播放任务ID"""
        with self.task_lock:
            return list(self.play_tasks.keys())


# 使用示例
if __name__ == "__main__":
    speaker = Speaker()
    try:
        # 启动后台播放
        task1 = speaker.play("test.mp3")
        print(f"启动播放任务 1: {task1}")
        
        task2 = speaker.play("music.wav")
        print(f"启动播放任务 2: {task2}")

        # 展示控制功能
        time.sleep(2)
        print("暂停任务1")
        speaker.pause(task1)

        time.sleep(1)
        print("任务1进度:", speaker.get_progress(task1))
        print("任务2进度:", speaker.get_progress(task2))

        time.sleep(2)
        print("恢复任务1")
        speaker.resume(task1)

        time.sleep(3)
        print("停止所有任务")
        for task_id in speaker.list_tasks():
            speaker.stop(task_id)

    finally:
        del speaker  # 触发析构函数，清理资源
