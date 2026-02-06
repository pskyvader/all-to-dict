from typing_extensions import override
from comfy_api.latest import ComfyExtension
from .lora_node import LoraFromJson
from .model_node import ModelFromJson
from .params_builder_node import ParametersBuilder


class AllToDict(ComfyExtension):
    @override
    async def get_node_list(self):
        return [LoraFromJson, ModelFromJson, ParametersBuilder]


async def comfy_entrypoint():
    return AllToDict()
