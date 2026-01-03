import type { UserProfile } from '$lib/stores/user';

export const PERMISSIONS = {
    RISK_EVENT: {
        READ: 'risk_event.read',
        CREATE: 'risk_event.create',
        APPROVE: 'risk_event.approve'
    }
};

export function hasPermission(user: UserProfile | null, permission: string): boolean {
    if (!user) return false;

    // Superadmin role bypass
    if (user.role === 'Superadmin') return true;

    if (!user.access) return false; // Safety check

    // Superadmin wildcard
    if (user.access.includes('*')) return true;

    return user.access.includes(permission);
}
