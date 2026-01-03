import { writable } from 'svelte/store';
import { authFetch } from '$lib/api';

export interface UserProfile {
    id: string;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    role: string;
    access: string[];
    avatar_url?: string;
}

function createUserStore() {
    const { subscribe, set, update } = writable<UserProfile | null>(null);

    return {
        subscribe,
        set,
        update,
        fetch: async () => {
            try {
                const res = await authFetch('/users/me');
                if (res.ok) {
                    const data = await res.json();
                    set(data);
                } else {
                    set(null);
                }
            } catch (error) {
                console.error('Failed to fetch user profile:', error);
                set(null);
            }
        },
        logout: () => {
            if (typeof localStorage !== 'undefined') {
                localStorage.removeItem('access_token');
            }
            set(null);
            window.location.href = '/';
        }
    };
}

export const user = createUserStore();
