import os
from ..utils import run_command, enable_speaker
import logging
from .piper_models import PIPER_MODELS, MODELS, COUNTRYS

PIPER_MODEL_DIR = "/opt/piper_models"

class Piper():
    DEFAULT_MODEL = "en_US-danny-low"

    TTS_TEMPELATE = "echo \"{text}\" | piper \
--model {model} \
--output_file {output_file}"

    STREAM_TEMPELATE = "echo \"{text}\" | piper \
--model {model} \
--output-raw | aplay -r 16000 -f S16_LE -t raw -"

    def __init__(self, model=None, log=None):
        self.log = log or logging.getLogger(__name__)
        self.model = model or self.DEFAULT_MODEL
        if not os.path.exists(PIPER_MODEL_DIR):
            run_command(f"mkdir -p {PIPER_MODEL_DIR}")
            run_command(f"chown 1000:1000 {PIPER_MODEL_DIR}")
        self.set_model(self.model)
        enable_speaker()

    def is_model_downloaded(self, model=None):
        if model is None:
            model = self.model
        onnx_file = os.path.join(PIPER_MODEL_DIR, model + ".onnx")
        json_file = onnx_file + ".json"
        onnx_exists = os.path.exists(onnx_file)
        json_exists = os.path.exists(json_file)
        self.log.debug(f"Model {model} onnx file exists: {onnx_exists}")
        self.log.debug(f"Model {model} json file exists: {json_exists}")
        return onnx_exists and json_exists
    
    def download_model(self, model=None):
        if model is None:
            model = self.model
        self.log.debug(f"Downloading model: {model}")
        onnx_file = os.path.join(PIPER_MODEL_DIR, model + ".onnx")
        json_file = onnx_file + ".json"

        cmd = f"python3 -m piper.download_voices {model} --download-dir {PIPER_MODEL_DIR}"
        status, result = run_command(cmd)
        if status != 0:
            raise RuntimeError(f"Download model error: \n  Command:{cmd}\n  Status {status}\n  Error: {result}")

        cmd = f"chown 1000:1000 {onnx_file}"
        status, result = run_command(cmd)
        if status != 0:
            raise RuntimeError(f"Chown model error: \n  Command:{cmd}\n  Status {status}\n  Error: {result}")

        cmd = f"chown 1000:1000 {json_file}"
        status, result = run_command(cmd)
        if status != 0:
            raise RuntimeError(f"Chown model error: \n  Command:{cmd}\n  Status {status}\n  Error: {result}")

    def tts(self, text, file):
        if self.model is None:
            raise ValueError("Model not set")
        text = text.replace('"', '\\"')
        model_path = os.path.join(PIPER_MODEL_DIR, self.model + ".onnx")
        args = {
            "text": text,
            "model": model_path,
            "output_file": file
        }
        cmd = self.TTS_TEMPELATE.format(**args)
        status, result = run_command(cmd)
        if status not in [0, None]:
            raise RuntimeError(f"Run command error: \n  Command:{cmd}\n  Status {status}\n  Error: {result}")
        return status == 0

    def stream(self, text):
        if self.model is None:
            raise ValueError("Model not set")
        text = text.replace('"', '\\"')
        model_path = os.path.join(PIPER_MODEL_DIR, self.model + ".onnx")
        args = {
            "text": text,
            "model": model_path
        }
        cmd = self.STREAM_TEMPELATE.format(**args)
        status, result = run_command(cmd)
        self.log.debug(f"Stream command: {cmd}")
        self.log.debug(f"Stream status: {status}")
        self.log.debug(f"Stream result: {result}")
        if status not in [0, None]:
            raise RuntimeError(f"Run command error: \n  Command:{cmd}\n  Status {status}\n  Error: {result}")

    def say(self, text, stream=True):
        if self.model is None:
            raise ValueError("Model not set")
        if not self.is_model_downloaded(self.model):
            self.log.warning(f"Model {self.model} not downloaded, downloading...")
            self.download_model(self.model)
        if stream:
            self.stream(text)
        else:
            self.tts(text, "/tmp/fusion_hat_piper.wav")
            run_command(f"aplay /tmp/fusion_hat_piper.wav")

    def available_models(self, country=None):
        if country is not None:
            if country not in COUNTRYS:
                raise ValueError("Country not found")
            return PIPER_MODELS[country]
        else:
            return MODELS

    def available_countrys(self):
        return COUNTRYS

    def set_model(self, model):
        if model in MODELS:
            self.model = model
        else:
            raise ValueError("Model not found")
