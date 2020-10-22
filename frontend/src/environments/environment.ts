import * as auth0 from "./../../secrets.json";

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: auth0.url,
    audience: auth0.audience,
    clientId: auth0.clientId,
    callbackURL: auth0.callbackURL,
  },
};
