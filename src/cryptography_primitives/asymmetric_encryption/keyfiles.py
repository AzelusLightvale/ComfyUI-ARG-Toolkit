# Keyfile loader and saver node for Python, for use with other major serialization nodes... but a bit more overkill
import atexit, glob, os, shutil, tempfile
from aiohttp import web
from server import PromptServer  # ty: ignore[unresolved-import]. Handled by ComfyUI, not base venv.

import folder_paths

PREFIX = "comfy_keys_"

# Sweep leftovers from crashed runs, then make a fresh private dir
for d in glob.glob(os.path.join(tempfile.gettempdir(), PREFIX + "*")):
    shutil.rmtree(d, ignore_errors=True)
KEY_DIR = tempfile.mkdtemp(prefix=PREFIX)   # mode 0700 on POSIX
atexit.register(lambda: shutil.rmtree(KEY_DIR, ignore_errors=True))

def _list():
    return sorted(f for f in os.listdir(KEY_DIR))

@PromptServer.instance.routes.post("/keyfiles/upload")
async def upload(request):
    post = await request.post()
    f = post.get("file")
    name = os.path.basename(getattr(f, "filename", "") or "")
    with open(os.path.join(KEY_DIR, name), "wb") as out:
        out.write(f.file.read())
    return web.json_response({"name": name})

class LoadBytesFile:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"file": (_list(),)}}

    @classmethod
    def VALIDATE_INPUTS(cls, file):
        if os.path.basename(file) != file or not os.path.isfile(os.path.join(KEY_DIR, file)):
            return "Key file not found (re-upload it)"
        return True

    @classmethod
    def IS_CHANGED(cls, file):
        p = os.path.join(KEY_DIR, file)
        return os.path.getmtime(p) if os.path.exists(p) else float("nan")

    RETURN_TYPES = ("BYTESLIKE",)
    FUNCTION = "execute"
    CATEGORY = "ARG Toolkit/Utilities"

    def execute(self, file):
        with open(os.path.join(KEY_DIR, file), "rb") as f:
            return (f.read(),)

import os, stat

class SaveBytesFile:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "data": ("BYTESLIKE",),
            "filename": ("STRING", {"default": "keyfile"}),
            "extension": ("STRING", {"default": "pem", "tooltip": "Make sure to change this to the correct fomat"}),
            "mode": ("STRING", {"default": "400", "tooltip": "The wanted format is in octal, similar to `chmod` in POSIX and related systems."}),      # octal, as in chmod
            "overwrite": ("BOOLEAN", {"default": False}),
        }}

    RETURN_TYPES = ()
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "ARG Toolkit/Utilities"

    @classmethod
    def IS_CHANGED(cls, **kw):
        return float("NaN")                              # always write, never serve from cache

    @classmethod
    def VALIDATE_INPUTS(cls, filename, extension, mode, **kw):
        name = f"{filename}.{extension}" if extension else filename
        if not filename or os.path.basename(name) != name or name in (".", ".."):
            return "Filename must be a bare name (no path separators)"
        try:
            if not 0 <= int(mode, 8) <= 0o777:
                raise ValueError
        except ValueError:
            return "Mode must be octal, e.g. 400 or 600"
        return True

    def save(self, data, filename, extension, mode, overwrite):
        name = f"{filename}.{extension}" if extension else filename
        dest = os.path.join(KEY_DIR, name)               # same private dir the loader uses
        if os.path.lexists(dest):
            if not overwrite:
                raise FileExistsError(f"{name} exists (enable overwrite)")
            try:
                os.remove(dest)
            except PermissionError:                      # Windows read-only attribute
                os.chmod(dest, stat.S_IWRITE)
                os.remove(dest)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        fd = os.open(dest, flags, int(mode, 8))
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        print(f"[SaveBytes] wrote {dest}")
        return ()

NODE_CLASS_MAPPINGS = {
    "LoadBytesFile": LoadBytesFile,
    "SaveBytesFile": SaveBytesFile,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBytesFile": "Load File as Bytes",
    "SaveBytesFile": "Save Bytes as File",
}
