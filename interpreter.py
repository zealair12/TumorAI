import numpy as np

def interpret_mask(mask: np.ndarray) -> str:
    class_names = {
        0: "Background",
        1: "Edema",
        2: "Enhancing Tumor",
        3: "Necrotic Core"
    }

    counts = {class_names[c]: int(np.sum(mask == c)) for c in np.unique(mask)}
    interpretation = []

    if len(counts.keys()) == 1 and "Background" in counts:
        return "No tumor regions detected in this slice."

    if "Enhancing Tumor" in counts and "Necrotic Core" in counts:
        interpretation.append("The lesion demonstrates contrast enhancement with a central necrotic region, features commonly associated with high-grade gliomas.")
    elif "Enhancing Tumor" in counts:
        interpretation.append("An enhancing lesion is present, raising suspicion for tumor progression.")
    elif "Necrotic Core" in counts:
        interpretation.append("Central necrosis is visible without contrast enhancement, which may still suggest aggressive behavior.")

    if "Edema" in counts:
        if counts["Edema"] > 5000:
            interpretation.append("Extensive peritumoral edema is observed, possibly indicating mass effect or infiltration.")
        else:
            interpretation.append("Mild surrounding edema is noted.")

    if not interpretation:
        return "Tumor tissue present, but without clear aggressive features."

    return " ".join(interpretation)
