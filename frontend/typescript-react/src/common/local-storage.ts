const localStoragePrefix = 'mti_verification';

export const localStorage = {
    getToken: () => {
        return JSON.parse(window.localStorage.getItem(`${localStoragePrefix}_token`) as string);
    },
    setToken: (token: string) => {
        window.localStorage.setItem(`${localStoragePrefix}_token`, JSON.stringify(token));
    },
    clearToken: () => {
        window.localStorage.removeItem(`${localStoragePrefix}_token`);
    },
};

export default localStorage;
