import { LedFirmwareFrontendConfiguration, Configuration } from './types/config';


export default async () => {
  const runtimeConfig = await fetch('/config.json');
  const config = await runtimeConfig.json() as Configuration;

  return {
    apiURL: config.API_URL || process.env.API_URL,
    baseURL: config.BASE_URL || process.env.BASE_URL,
  } as LedFirmwareFrontendConfiguration;
};
