import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "custom.LoadBytesFile",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "LoadBytesFile") return;
        const onCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onCreated?.apply(this, arguments);
            const w = this.widgets.find((x) => x.name === "file");

            const input = document.createElement("input");
            input.type = "file";
            input.style.display = "none";
            document.body.append(input);

            input.onchange = async () => {
                const f = input.files[0];
                if (!f) return;
                const body = new FormData();
                body.append("file", f);
                const r = await api.fetchApi("/keyfiles/upload", {
                    method: "POST",
                    body,
                });
                const data = await r.json();
                if (!r.ok) return alert(data.error || r.statusText);
                if (!w.options.values.includes(data.name))
                    w.options.values.push(data.name);
                w.value = data.name;
                input.value = "";
            };

            this.addWidget("button", "Upload file...", null, () =>
                input.click(),
            );
            this.onRemoved = () => input.remove();
        };
    },
});
