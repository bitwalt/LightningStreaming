export const validateEmail = function (email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

export const escapeSpecialUrlCharacters = function (string) {
    return string
        .replace(/'/g, "%27")
        .replace(/&/g, "%26")
        .replace(/%/g, "%25")
        .replace(/#/g, "%23")
        .replace(/\s/g, "%20");
}