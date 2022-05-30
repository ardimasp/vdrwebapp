var signatures = {
    R0lGODdh: "image/gif",
    iVBORw0KGgo: "image/png",
    "/9j/": "image/jpg",
    "data": ""
};
  
export const detectMimeType = (b64) => {
    for (var s in signatures) {
        if (b64.indexOf(s) == 0) {
            return signatures[s];
        }
    }
}