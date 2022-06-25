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



import CryptoJS from "crypto-js";

const key = "1234567890"

export const encryptToken = (token) => {
    if (token == null || token == undefined) return
    var encrypt = CryptoJS.AES.encrypt(JSON.stringify(token), key);
    return encrypt.toString();
}
export const decryptToken = (encrypted) => {
    if (encrypted == null || encrypted == undefined) return
    var decrypt = CryptoJS.AES.decrypt(encrypted, key);
    return decrypt.toString(CryptoJS.enc.Utf8).replace(/['"]+/g, '');
    // return decrypt.toString(CryptoJS.enc.Utf8)
}

// decode JWT token
export const decode = (token) => {
    if (token == null || token == undefined) return
    // var decrypted = decryptToken(token);
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}