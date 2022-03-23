const functions = {};


functions.parseJwt = (token) => {
    // return json version of jwt
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};


functions.jwtGetId = (token) => {
    // return uid from jwt
    jwt = functions.parseJwt(token)
    return jwt.id;
}

module.exports = functions;