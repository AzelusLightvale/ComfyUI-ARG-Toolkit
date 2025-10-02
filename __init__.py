"""Top-level package for comfyui-arg-toolkit."""
import os
import importlib.util

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# track which module defined each key
NODE_CLASS_SOURCES = {}
NODE_DISPLAY_NAME_SOURCES = {}

BASE_FOLDER = os.path.dirname(__file__)
SRC_FOLDER = os.path.join(BASE_FOLDER, "src")

for root, _, files in os.walk(SRC_FOLDER):
    for filename in files:
        if filename.endswith(".py") and filename != "__init__.py":
            module_path = os.path.join(root, filename)

            # module name like "src.subfolder.plugin"
            rel_path = os.path.relpath(module_path, BASE_FOLDER)
            module_name = rel_path.replace(os.sep, ".")[:-3]

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if getattr(module, "NODE_CLASS_MAPPINGS", None):
                for key, value in module.NODE_CLASS_MAPPINGS.items():
                    if key in NODE_CLASS_MAPPINGS:
                        print(
                            f"[ComfyUI-ARG-Toolkit] [Duplicate NODE_CLASS_MAPPINGS] '{key}' "
                            f"overwritten by {module_name} (was {NODE_CLASS_SOURCES[key]})"
                        )
                    NODE_CLASS_MAPPINGS[key] = value
                    NODE_CLASS_SOURCES[key] = module_name

            if getattr(module, "NODE_DISPLAY_NAME_MAPPINGS", None):
                for key, value in module.NODE_DISPLAY_NAME_MAPPINGS.items():
                    if key in NODE_DISPLAY_NAME_MAPPINGS:
                        print(
                            f"[ComfyUI-ARG-Toolkit] [Duplicate NODE_DISPLAY_NAME_MAPPINGS] '{key}' "
                            f"overwritten by {module_name} (was {NODE_DISPLAY_NAME_SOURCES[key]})"
                        )
                    NODE_DISPLAY_NAME_MAPPINGS[key] = value
                    NODE_DISPLAY_NAME_SOURCES[key] = module_name

__author__ = """AzelusLightvale"""
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
WEB_DIRECTORY = "./web"

