import {Configuration, ConfigurationParameters} from "api-client";
import { getCSRFToken } from "../lib/django";


export function getApiConfiguration() : Configuration {
  // using credentials: 'include' to allow cookies to be sent to the server
  // which also uses the session to handle authentication
  const params: ConfigurationParameters = {
    basePath: import.meta.env.VITE_APP_BASE_URL,
    credentials: 'include',
    headers: {
      'X-CSRFToken': getCSRFToken() || '',
    },
  }
  return new Configuration(params);
}
