import torch
from torch import device

from const import EnumInferenceTypes
from voice_changer.RVC.inferencer.Inferencer import Inferencer
from .models import SynthesizerTrnMsNSFsid


class WebUIInferencer(Inferencer):
    def loadModel(self, file: str, dev: device, isHalf: bool = True):
        super().setProps(EnumInferenceTypes.pyTorchWebUI, file, dev, isHalf)
        cpt = torch.load(file, map_location="cpu")
        model = SynthesizerTrnMsNSFsid(**cpt["params"], is_half=isHalf)

        model.eval()
        model.load_state_dict(cpt["weight"], strict=False)

        model = model.to(dev)
        if isHalf:
            model = model.half()

        self.model = model
        return self

    def infer(
        self,
        feats: torch.Tensor,
        pitch_length: torch.Tensor,
        pitch: torch.Tensor,
        pitchf: torch.Tensor,
        sid: torch.Tensor,
    ) -> torch.Tensor:
        return self.model.infer(feats, pitch_length, pitch, pitchf, sid)
