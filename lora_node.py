from comfy_api.latest import io
from .utils import pick_random_file, load_json_sidecar, merge_json_rules
import os


class LoraFromJson(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="LoraFromJson",
            display_name="LoRA From JSON",
            category="conditioning/lora",
            inputs=[
                io.String.Input("lora_folder", default="models/loras"),
                io.Bool.Input("include_subfolders", default=True),
                io.Dict.Input("parameters"),
                io.Dict.Input("positive_prompts"),
                io.Dict.Input("negative_prompts"),
                io.Bool.Input("modifications_enabled", default=True),
            ],
            outputs=[
                io.LoraStack.Output(),
                io.Dict.Output(),
                io.Dict.Output(),
                io.Dict.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        lora_folder,
        include_subfolders,
        parameters,
        positive_prompts,
        negative_prompts,
        modifications_enabled,
    ):
        lora_path = pick_random_file(lora_folder, include_subfolders, (".safetensors",))
        json_data = load_json_sidecar(lora_path)

        params = dict(parameters)
        pos = dict(positive_prompts)
        neg = dict(negative_prompts)

        merge_json_rules(json_data, params, pos, neg, modifications_enabled)

        name = os.path.basename(lora_path)
        weight = params.get("lora_weight", 0.6)
        lora_stack = [(name, weight, weight)]

        return io.NodeOutput(lora_stack, params, pos, neg)
