// this is a types file for the allauth library to avoid having to modify it directly

export interface FormError {
  message: string;
  param: string;
  code?: string;
}

export interface AllauthResponse {
  status: number;
  meta?: {
    session_token?: string;
    is_authenticated?: boolean;
  };
  data?: {
    [key: string]: never;
  };
  errors?: FormError[]
}

export interface AccountConfiguration {
  login_methods?: ("email" | "username")[];
  is_open_for_signup: boolean;
  email_verification_by_code_enabled: boolean;
  login_by_code_enabled: boolean;
}

export interface Provider {
  id: string;
  name: string;
  client_id?: string;
  flows: ("provider_redirect" | "provider_token")[];
}

export interface ConfigurationResponse {
  data: {
    account: AccountConfiguration;
    socialaccount?: {
      providers: Provider[]
    };
    mfa?: {
      supported_types: ("recovery_codes" | "totp")[];
    };
    usersessions?: {
      track_activity: boolean;
    };
  };
  status: number;
}

export const Client: {
  APP: 'app';
  BROWSER: 'browser';
};

export const AuthProcess: {
  LOGIN: 'login';
  CONNECT: 'connect';
};

// ... you can add other type definitions as needed ...

export declare function login(data: { email: string; password: string }): Promise<AllauthResponse>;

export declare function logout(): Promise<AllauthResponse>;

export declare function signUp(data: { email: string, password: string }): Promise<AllauthResponse>;

export declare function useConfig(): ConfigurationResponse;

export declare function authenticateByToken(provider: string, token: {id_token: string, client_id: string}, process: string): Promise<AllauthResponse>;

export declare function redirectToProvider (providerId: string, callbackURL: string, process: string);
// ... other function declarations ...
