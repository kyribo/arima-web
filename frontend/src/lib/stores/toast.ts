import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
    id: number;
    message: string;
    type: ToastType;
    duration?: number;
}

function createToastStore() {
    const { subscribe, update } = writable<Toast[]>([]);

    function add(message: string, type: ToastType = 'info', duration = 3000) {
        const id = Date.now();
        update((toasts) => [...toasts, { id, message, type, duration }]);

        if (duration > 0) {
            setTimeout(() => {
                dismiss(id);
            }, duration);
        }
    }

    function dismiss(id: number) {
        update((toasts) => toasts.filter((t) => t.id !== id));
    }

    return {
        subscribe,
        add,
        dismiss,
        success: (msg: string, duration?: number) => add(msg, 'success', duration),
        error: (msg: string, duration?: number) => add(msg, 'error', duration),
        info: (msg: string, duration?: number) => add(msg, 'info', duration),
        warning: (msg: string, duration?: number) => add(msg, 'warning', duration)
    };
}

export const toast = createToastStore();
