from comfy_api.latest import io
from .utils import pick_random_file, load_json_sidecar, merge_json_rules


class ModelFromJson(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ModelFromJson",
            display_name="Model From JSON",
            category="model",
            inputs=[
                io.String.Input("model_folder", default="models/checkpoints"),
                io.Bool.Input("include_subfolders", default=True),
                io.Dict.Input("parameters"),
                io.Dict.Input("positive_prompts"),
                io.Dict.Input("negative_prompts"),
                io.Bool.Input("modifications_enabled", default=True),
            ],
            outputs=[
                io.String.Output(),
                io.Dict.Output(),
                io.Dict.Output(),
                io.Dict.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        model_folder,
        include_subfolders,
        parameters,
        positive_prompts,
        negative_prompts,
        modifications_enabled,
    ):
        model_path = pick_random_file(
            model_folder, include_subfolders, (".safetensors", ".ckpt")
        )
        json_data = load_json_sidecar(model_path)

        params = dict(parameters)
        pos = dict(positive_prompts)
        neg = dict(negative_prompts)

        merge_json_rules(json_data, params, pos, neg, modifications_enabled)

        return io.NodeOutput(model_path, params, pos, neg)
