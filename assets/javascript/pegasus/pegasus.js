import {getApiConfiguration} from "../api";
import {PegasusApi} from "api-client";
import { Charts as PegasusCharts } from './examples/charts';

export function getPegasusApiClient(serverBaseUrl) {
  return new PegasusApi(getApiConfiguration(serverBaseUrl));
}

export { PegasusCharts as Charts };

if (typeof window.SiteJS === 'undefined') {
  window.SiteJS = {};
}

// preserve legacy SiteJS.pegasus behavior.
window.SiteJS.pegasus = {
  Charts: PegasusCharts,
  getPegasusApiClient: getPegasusApiClient,
};
