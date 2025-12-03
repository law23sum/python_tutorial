import {useConfig} from '../../allauth_auth'
import {redirectToProvider, Client, settings} from '../../lib/allauth'
import {Provider} from '../../types/allauth'

export default function ProviderList(props: { callbackURL: string, process: string }) {
  const config = useConfig()
  const providers: Provider[] = config.data.socialaccount.providers.filter((p: Provider) => p.client_id)
  if (!providers.length) {
    return null
  }

  function getRedirectToProvider(provider: Provider) {
    // @ts-expect-error - process is a string
    redirectToProvider(provider.id, props.callbackURL, props.process);
  }

  return (
    <>
      {settings.client === Client.BROWSER && <ul>
        {providers.map(provider => {
          return (
            <li key={provider.id}>
              <button className="btn btn-primary btn-outline btn-block flex justify-center my-2"
                onClick={() => getRedirectToProvider(provider)}>
                  Continue with {provider.name}
              </button>
            </li>
          )
        })}
      </ul>}
    </>
  )
}
