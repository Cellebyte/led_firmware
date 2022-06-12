import { RequestParams, Api } from '@/types/api';
import { LedFirmwareFrontendConfiguration } from '@/types/config';

export default function apiFactory(config: LedFirmwareFrontendConfiguration) {
  // function getToken(accessToken?: string | null | undefined): string {
  //   return `Bearer ${accessToken || ''}`;
  // }

  const getRequestHeaders = (): RequestParams => ({
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });
  return new Api(
    {
      baseUrl: config.apiURL,
      securityWorker: getRequestHeaders,
    },
  );
}
