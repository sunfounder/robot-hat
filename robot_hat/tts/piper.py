import os
import logging
import wave
from pathlib import Path
from typing import Callable
from urllib.request import urlopen
from piper import PiperVoice
from piper.download_voices import _needs_download, VOICE_PATTERN, URL_FORMAT
from onnxruntime.capi.onnxruntime_pybind11_state import InvalidProtobuf
from tqdm import tqdm

from .piper_models import PIPER_MODELS, MODELS, COUNTRYS
from ..utils import enable_speaker
from ..audio_player import AudioPlayer

PIPER_MODEL_DIR = "/opt/piper_models"

class Piper():

    def __init__(self, model: str = None, log: logging.Logger = None):
        self.log = log or logging.getLogger(__name__)
        # Init model directory
        if not os.path.exists(PIPER_MODEL_DIR):
            os.makedirs(PIPER_MODEL_DIR, 0o777)
            os.chown(PIPER_MODEL_DIR, 1000, 1000)
        self.model = None
        if model is not None:
            self.set_model(model)
        else:
            self.piper = None
        enable_speaker()

    def get_language(self):
        language = self.model.split("-")[0]
        return language

    def is_model_downloaded(self, model: str):
        if model is None:
            model = self.model
        onnx_file = os.path.join(PIPER_MODEL_DIR, model + ".onnx")
        json_file = onnx_file + ".json"
        onnx_exists = os.path.exists(onnx_file)
        json_exists = os.path.exists(json_file)
        self.log.debug(f"Model {model} onnx file exists: {onnx_exists}")
        self.log.debug(f"Model {model} json file exists: {json_exists}")
        return onnx_exists and json_exists
    
    def download_model(self,
                        model: str,
                        force: bool = False,
                        progress_callback: Callable[[int, int], None] = None):
        model_path = self.get_model_path(model)
        if not self.is_model_downloaded(model) or force:
            self.log.info(f"Downloading model {model} to {model_path}")
            download_voice(model,
                            Path(PIPER_MODEL_DIR),
                            force_redownload=force,
                            progress_callback=progress_callback)

    def fix_chinese_punctuation(self, text: str):
        """Replace Chinese punctuation with English punctuation"""
        if self.get_language() != "zh_CN":
            return text
        MAP = {
            '，': '. ',
            '。': '. ',
            '！': '! ',
            '？': '? ',
            '——': '. ',
            '“': '"',
            '”': '"',
            '‘': "'",
            '’': "'",
            "~": ". ",
            "～": ". ",
            "：": ". ",
            "...": ". ",
            "……": ". ",
            "、": ". ",
        }
        for k, v in MAP.items():
            text = text.replace(k, v)
        # find number followed by dot and replace with number followed by 点
        import re
        text = re.sub(r'(\d)\.(\d)', r'\1点\2', text)

        return text

    def tts(self, text: str, file: str):
        if self.piper is None:
            raise ValueError("Model not set, set model first, with Piper.set_model(model)")
        text = self.fix_chinese_punctuation(text)

        with wave.open(file, "wb") as wav_file:
            self.piper.synthesize_wav(text, wav_file)

    def stream(self, text: str):
        if self.piper is None:
            raise ValueError("Model not set, set model first, with Piper.set_model(model)")
        text = self.fix_chinese_punctuation(text)

        with AudioPlayer(self.piper.config.sample_rate) as player:
            for chunk in self.piper.synthesize(text):
                player.play(chunk.audio_int16_bytes)

    def say(self, text: str, stream: bool = True):
        if self.piper is None:
            raise ValueError("Model not set, set model first, with Piper.set_model(model)")
        if stream:
            self.stream(text)
        else:
            self.tts(text, "/tmp/tts_piper.wav")
            with AudioPlayer(self.piper.config.sample_rate) as player:
                with open("/tmp/tts_piper.wav", "rb") as f:
                    player.play(f.read())

    def available_models(self, country: str = None):
        if country is None:
            return MODELS
        else:
            return PIPER_MODELS.get(country, [])

    def available_countrys(self):
        return COUNTRYS

    def get_model_path(self, model: str):
        return os.path.join(PIPER_MODEL_DIR, model + ".onnx")

    def set_model(self, model: str):
        if model in MODELS:
            model_path = self.get_model_path(model)
            if not self.is_model_downloaded(model):
                self.log.warning(f"Model {model} not downloaded, downloading...")
                self.download_model(model)
            try:
                self.piper = PiperVoice.load(model_path)
            except InvalidProtobuf as e:
                self.log.warning(f"Failed to load model {model_path}: {e}, try to redownload model.")
                self.download_model(model, force=True)
                self.piper = PiperVoice.load(model_path)
            self.model = model
        else:
            raise ValueError("Model not found")
    
def download_voice(voice: str,
                    download_dir: Path,
                    force_redownload: bool = False,
                    progress_callback: Callable[[int, int], None] = None
                    ) -> None:
    """Download a voice model and config file to a directory."""
    voice = voice.strip()
    voice_match = VOICE_PATTERN.match(voice)
    if not voice_match:
        raise ValueError(
            f"Voice '{voice}' did not match pattern: <language>-<name>-<quality> like 'en_US-lessac-medium'",
        )

    lang_family = voice_match.group("lang_family")
    lang_code = lang_family + "_" + voice_match.group("lang_region")
    voice_name = voice_match.group("voice_name")
    voice_quality = voice_match.group("voice_quality")

    voice_code = f"{lang_code}-{voice_name}-{voice_quality}"
    format_args = {
        "lang_family": lang_family,
        "lang_code": lang_code,
        "voice_name": voice_name,
        "voice_quality": voice_quality,
    }

    # 下载模型文件（带进度条）
    model_path = download_dir / f"{voice_code}.onnx"
    if force_redownload or _needs_download(model_path):
        model_url = URL_FORMAT.format(extension=".onnx",** format_args)
        _download_with_progress(model_url, model_path, progress_callback)

    # 下载配置文件（带进度条）
    config_path = download_dir / f"{voice_code}.onnx.json"
    if force_redownload or _needs_download(config_path):
        config_url = URL_FORMAT.format(extension=".onnx.json", **format_args)
        _download_with_progress(config_url, config_path, progress_callback)

    # _LOGGER.info("Downloaded: %s", voice)


def _download_with_progress(url: str,
                            output_path: Path,
                            progress_callback: Callable[[int, int], None] = None) -> None:
    """带进度条的文件下载函数"""
    with urlopen(url) as response:
        file_size = int(response.headers.get("Content-Length", 0))
        
        if progress_callback:
            progress_callback(0, file_size)
        else:
            progress_bar = tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Downloading {output_path.name}",
                leave=True
            )
        
        with open(output_path, "wb") as out_file:
            while True:
                chunk = response.read(8192)  # 8KB 块
                if not chunk:
                    break
                out_file.write(chunk)
                if progress_callback:
                    progress_callback(len(chunk), file_size)
                else:
                    progress_bar.update(len(chunk))
        
        if progress_callback:
            progress_callback(file_size, file_size)
        else:
            progress_bar.close()
