import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'light' | 'dark' | 'system';

function createThemeStore() {
    const { subscribe, set, update } = writable<Theme>('system');

    return {
        subscribe,
        set: (theme: Theme) => {
            if (browser) {
                localStorage.setItem('theme', theme);
                updateTheme(theme);
            }
            set(theme);
        },
        toggle: () => {
            update((current) => {
                const newTheme = current === 'dark' ? 'light' : 'dark';
                if (browser) {
                    localStorage.setItem('theme', newTheme);
                    updateTheme(newTheme);
                }
                return newTheme;
            });
        },
        init: () => {
            if (browser) {
                const stored = localStorage.getItem('theme') as Theme | null;
                const theme = stored || 'system';
                set(theme);
                updateTheme(theme);
            }
        }
    };
}

function updateTheme(theme: Theme) {
    if (!browser) return;

    const root = document.documentElement;
    const isDark =
        theme === 'dark' ||
        (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    if (isDark) {
        root.classList.add('dark');
    } else {
        root.classList.remove('dark');
    }
}

export const theme = createThemeStore();
