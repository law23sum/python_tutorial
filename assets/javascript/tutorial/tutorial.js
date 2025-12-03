import {getApiConfiguration} from "../api";
import {PegasusApi} from "api-client";
import { Charts as TutorialCharts } from './web/charts';

export function getTutorialApiClient(serverBaseUrl) {
  return new PegasusApi(getApiConfiguration(serverBaseUrl));
}

export { TutorialCharts as Charts };

if (typeof window.SiteJS === 'undefined') {
  window.SiteJS = {};
}

// expose tutorial JS helpers via SiteJS.
window.SiteJS.tutorial = {
  Charts: TutorialCharts,
  getTutorialApiClient: getTutorialApiClient,
};
