
from comfy_api.latest import io
import random


class ParametersBuilder(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ParametersBuilder",
            display_name="Parameters Builder",
            category="utils",
            inputs=[
                io.String.Input("width", default="512"),
                io.String.Input("height", default="512"),
                io.String.Input("scheduler", default=""),
                io.String.Input("sampler", default=""),
                io.String.Input("cfg", default="7"),
                io.String.Input("steps", default="30"),
                io.String.Input("seed", default="-1"),
            ],
            outputs=[io.Dict.Output()],
        )

    @classmethod
    def execute(cls, width, height, scheduler, sampler, cfg, steps, seed):
        def parse(v):
            parts = [p.strip() for p in v.split(",") if p.strip()]
            if not parts:
                return None
            chosen = random.choice(parts)
            try:
                return int(chosen)
            except ValueError:
                try:
                    return float(chosen)
                except ValueError:
                    return chosen

        params = {}
        for k, v in {
            "width": width,
            "height": height,
            "scheduler": scheduler,
            "sampler": sampler,
            "cfg": cfg,
            "steps": steps,
            "seed": seed,
        }.items():
            parsed = parse(v)
            if parsed is not None:
                params[k] = parsed

        return io.NodeOutput(params)

