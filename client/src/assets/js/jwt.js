const functions = {};


functions.getJwt = () => {
    let jwt = window.localStorage.getItem('jwt');
    if(jwt)
        return jwt;
    return false;
}


functions.parseJwt = () => {
    // return json version of jwt
    let token = functions.getJwt();

    if(!token)
        return false;

    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};


functions.jwtGetId = () => {
    // return uid from jwt
    let token = functions.getJwt();
    if(!token)
        return false;

    jwt = functions.parseJwt(token)
    return jwt.id;
}

module.exports = functions;