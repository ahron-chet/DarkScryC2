export function pathToSegments(path: string) {
    let isUNC = false;

    if (path.startsWith("\\\\")) {
        isUNC = true;
        path = path.slice(2); // Remove leading `\\`
    }

    // Convert backslashes to forward slashes for uniform processing
    let replaced = path.replace(/\\/g, "/");

    // Remove trailing slashes
    replaced = replaced.replace(/\/+$/, "");

    if (!replaced) return isUNC ? ["UNC"] : [];

    const parts = replaced.split("/");

    if (isUNC) {
        return ["UNC", ...parts];
    }

    return parts.filter(Boolean);
}




export function segmentsToPath(segments: string[]): string {
    if (segments.length === 0) return "";

    // Preserve UNC paths
    if (segments[0] === "UNC") {
        return "\\\\" + segments.slice(1).join("\\");
    }

    return segments.join("\\");
}
