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
