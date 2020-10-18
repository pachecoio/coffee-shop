/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */
import * as auth0 from "./../../secrets.json";

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0,
};
