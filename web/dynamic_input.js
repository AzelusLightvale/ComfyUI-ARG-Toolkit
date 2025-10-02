import { ComfyApp, app } from "../../scripts/app.js";

app.registerExtension({
    name: "Custom.DynamicHashInputs",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        const dynamicNodes = ["SHA2", "SHA3", "BLAKE2", "SHA1", "MD5", "SM3", "SHAKE"];

        if (dynamicNodes.includes(nodeData.name)) {
            const origOnConnectionsChange = nodeType.prototype.onConnectionsChange;

            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (origOnConnectionsChange) {
                    origOnConnectionsChange.apply(this, arguments);
                }
                if (!link_info || type !== 1) return;

                // Filter to only key inputs (ignore widgets)
                const keyInputs = this.inputs.filter(input => input.name.startsWith("key") && !input.widget);

                // Renumber key slots
                keyInputs.forEach((input, i) => {
                    input.name = `key${i + 1}`;
                });

                if (connected) {
                    // Check if connected to last key slot
                    const lastKeyIndex = this.inputs.findIndex(input => input === keyInputs[keyInputs.length - 1]);
                    if (index === lastKeyIndex) {
                        this.addInput(`key${keyInputs.length + 1}`, "STRING");
                    }
                } else {
                    // Check if disconnected from a key slot that's not the first
                    const disconnectedInput = this.inputs[index];
                    if (disconnectedInput?.name.startsWith("key") && 
                        disconnectedInput.name !== "key1" &&
                        !disconnectedInput.widget) {
                        this.removeInput(index);
                    }
                }
            };
        }
    }
});