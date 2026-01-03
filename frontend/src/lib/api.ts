export const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function authFetch(url: string, options: RequestInit = {}) {
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;

    // Default headers
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...options.headers as Record<string, string>
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
    });

    if (response.status === 401) {
        if (typeof localStorage !== 'undefined') {
            localStorage.removeItem('access_token');
        }
        window.location.href = '/';
    }

    return response;
}

export const api = {
    get: async (url: string, config: any = {}) => {
        const query = config.params ? '?' + new URLSearchParams(config.params).toString() : '';
        const res = await authFetch(url + query, {
            method: 'GET',
            headers: config.headers
        });
        if (!res.ok) throw res;
        return res.json();
    },
    post: async (url: string, data: any, config: any = {}) => {
        const res = await authFetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: config.headers
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            // Mimic axios error structure slightly for frontend compat if needed
            throw { response: { data: err, status: res.status } };
        }
        return res.json();
    },
    put: async (url: string, data: any, config: any = {}) => {
        const res = await authFetch(url, {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: config.headers
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw { response: { data: err, status: res.status } };
        }
        return res.json();
    },
    delete: async (url: string, config: any = {}) => {
        const res = await authFetch(url, {
            method: 'DELETE',
            headers: config.headers
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw { response: { data: err, status: res.status } };
        }
        return res.status === 204 ? null : res.json();
    }
};
