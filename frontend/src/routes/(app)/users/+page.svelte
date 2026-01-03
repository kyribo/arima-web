<script lang="ts">
	import { fade, slide } from 'svelte/transition';
    import { onMount } from 'svelte';
    import { api } from '$lib/api';

    // Permission Configuration (kept as constant)
    const PERMISSION_GROUPS = [
        {
            id: 'dashboard',
            label: 'Dashboard',
            permissions: [
                { id: 'view', label: 'View Dashboard' }
            ]
        },
        {
            id: 'trans_data',
            label: 'Trans Data',
            permissions: [
                { id: 'view', label: 'View Data' },
                { id: 'export', label: 'Export Excel' }
            ]
        },
        {
            id: 'risk_event',
            label: 'Risk Event',
            permissions: [
                { id: 'view', label: 'View Events' },
                { id: 'create', label: 'Create Event' },
                { id: 'edit', label: 'Edit Event' },
                { id: 'delete', label: 'Delete Event' },
                { id: 'approval', label: 'Approve Event' }
            ]
        },
        {
            id: 'upload_data',
            label: 'Upload Data',
            permissions: [
                { id: 'view', label: 'View Page' },
                { id: 'upload', label: 'Upload Files' }
            ]
        },
        {
            id: 'reports',
            label: 'Reports',
            permissions: [
                { id: 'view', label: 'View Reports' },
                { id: 'generate', label: 'Generate Report' }
            ]
        },
        {
            id: 'users',
            label: 'User Management',
            permissions: [
                { id: 'view', label: 'View Users' },
                { id: 'manage', label: 'Manage Users' }
            ]
        }
    ];

    interface User {
        id: string;
        username: string;
        email: string;
        first_name: string;
        last_name: string;
        role: string;
        access: string[];
        is_active: boolean;
        avatar_url: string;
        lastActive?: string; // Not yet in backend
    }

	let users = $state<User[]>([]);
    let isLoading = $state(false);

	let SearchQuery = $state('');
    
    async function loadUsers() {
        isLoading = true;
        try {
            const res = await api.get('/users/', { params: { search: SearchQuery } });
            users = res.map((u: any) => ({
                ...u,
                avatar_url: u.avatar_url || `https://ui-avatars.com/api/?name=${u.username}&background=random`
            }));
        } catch (error) {
            console.error(error);
            alert('Failed to load users');
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        loadUsers();
    });

    // Debounce search
    let searchTimeout: any;
    $effect(() => {
        SearchQuery;
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadUsers();
        }, 500);
    });

    async function handleDelete(id: string) {
        if(confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            try {
                await api.delete(`/users/${id}`);
                await loadUsers();
            } catch (error) {
                console.error(error);
                alert('Failed to delete user');
            }
        }
    }

    // Force logout (not yet implemented backend endpoint for specific user logout, keeping as mock UI or placeholder)
    function handleForceLogout(userName: string) {
        alert(`Feature to logout ${userName} coming soon.`);
    }

    // Modal Logic
    let isModalOpen = $state(false);
    let modalMode = $state<'create' | 'edit'>('create');
    let editingUser = $state<any>(null); 
    
    function openCreateModal() {
        modalMode = 'create';
        editingUser = {
            username: '',
            email: '',
            password: '', 
            first_name: '',
            last_name: '',
            role: 'User',
            access: [],
            is_active: true
        };
        isModalOpen = true;
    }

    function openEditModal(user: any) {
        modalMode = 'edit';
        // Clone to avoid direct mutation
        editingUser = JSON.parse(JSON.stringify(user));
        
        // Handle '*' access expansion for UI if needed, but for now we just show what is there
        if (editingUser.access.includes('*')) {
            let allPerms: string[] = [];
            PERMISSION_GROUPS.forEach(g => {
                g.permissions.forEach(p => allPerms.push(`${g.id}.${p.id}`));
            });
            // We don't overwrite the '*' in the data sent back unless user changes it, 
            // but for UI checking we might need logic. 
            // For simplicity, let's just leave it as is. Interactive checkboxes might behave weirdly if we don't handle '*' logic.
        }
        isModalOpen = true;
    }

    async function saveUserChanges() {
        if (!editingUser) return;
        
        try {
            if (modalMode === 'create') {
                await api.post('/users/', editingUser);
            } else {
                await api.put(`/users/${editingUser.id}`, editingUser);
            }
            await loadUsers();
            isModalOpen = false;
            editingUser = null;
        } catch (error: any) {
            console.error('Save error:', error);
            let msg = 'Failed to save user';
            
            if (error?.response?.data?.detail) {
                const detail = error.response.data.detail;
                if (Array.isArray(detail)) {
                    // Pydantic validation errors
                    msg = detail.map((e: any) => `${e.loc?.join('.')} : ${e.msg}`).join('\n');
                } else if (typeof detail === 'object') {
                    msg = JSON.stringify(detail);
                } else {
                    msg = String(detail);
                }
            } else if (error?.message) {
                msg = error.message;
            }
            
            alert(msg);
        }
    }

    // Helper to toggle a specific permission
    function togglePermission(moduleId: string, permId: string, checked: boolean) {
        const key = `${moduleId}.${permId}`;
        let currentAccess = editingUser.access || [];
        
        if (checked) {
            editingUser.access = [...currentAccess, key];
        } else {
            editingUser.access = currentAccess.filter((a: string) => a !== key);
        }
    }

    // Helper to toggle all permissions in a module
    function toggleModuleAll(moduleId: string, checked: boolean) {
        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return;

        const allKeys = group.permissions.map(p => `${moduleId}.${p.id}`);
        let currentAccess = editingUser.access || [];
        
        if (checked) {
            // Add all missing keys
            const newKeys = allKeys.filter(k => !currentAccess.includes(k));
            editingUser.access = [...currentAccess, ...newKeys];
        } else {
            // Remove all keys belonging to this module
            editingUser.access = currentAccess.filter((a: string) => !a.startsWith(`${moduleId}.`));
        }
    }

    function isModuleFullyChecked(moduleId: string) {
        if (!editingUser?.access) return false;
        if (editingUser.access.includes('*')) return true;
        
        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return false;
        return group.permissions.every(p => editingUser.access.includes(`${moduleId}.${p.id}`));
    }
    
    function isModulePartiallyChecked(moduleId: string) {
        if (!editingUser?.access) return false;
        if (editingUser.access.includes('*')) return false;

        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return false;
        const count = group.permissions.filter(p => editingUser.access.includes(`${moduleId}.${p.id}`)).length;
        return count > 0 && count < group.permissions.length;
    }

    // Helper to display access in table
    function getAccessDisplay(access: string[]) {
        if (!access) return 'No Access';
        if (access.includes('*')) {
            return 'Full Access';
        }
        if (access.length === 0) {
            return 'No Access';
        }
        return `${access.length} Permissions`;
    }
</script>

<div in:fade class="space-y-6">
	<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">User Management</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Manage system access and user roles.</p>
		</div>

		<button
			onclick={openCreateModal}
			class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium flex items-center gap-2"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-5 w-5"
				viewBox="0 0 20 20"
				fill="currentColor"
			>
				<path
					fill-rule="evenodd"
					d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
					clip-rule="evenodd"
				/>
			</svg>
			Add New User
		</button>
	</div>

	<!-- Filters & Search -->
	<div
		class="bg-white dark:bg-neutral-800 p-4 rounded-xl border border-gray-200 dark:border-white/5 shadow-sm flex flex-col sm:flex-row gap-4"
	>
		<div class="relative flex-1">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
				/>
			</svg>
			<input
				type="text"
				name="search-users"
				autocomplete="off"
				bind:value={SearchQuery}
				placeholder="Search users..."
				class="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-gray-900 dark:text-white"
			/>
		</div>
	</div>

	<!-- Users Table -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-xl border border-gray-200 dark:border-white/5 shadow-sm overflow-hidden"
	>
		<div class="overflow-x-auto">
			<table class="w-full text-left">
				<thead>
					<tr class="bg-gray-50 dark:bg-white/5 border-b border-gray-200 dark:border-white/5">
						<th
							class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>User</th
						>
						<th
							class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>Role</th
						>
						<th
							class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>Access</th
						>
						<th
							class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>Status</th
						>
						<th
							class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>Force Logout</th
						>
						<th
							class="px-6 py-4 text-right text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider"
							>Actions</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-white/5">
					{#if isLoading}
						<tr>
							<td colspan="6" class="px-6 py-8 text-center text-gray-500">Loading users...</td>
						</tr>
					{:else if users.length === 0}
						<tr>
							<td colspan="6" class="px-6 py-8 text-center text-gray-500">No users found.</td>
						</tr>
					{:else}
						{#each users as user (user.id)}
							<tr class="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
								<td class="px-6 py-4 whitespace-nowrap">
									<div class="flex items-center gap-3">
										<img
											src={user.avatar_url}
											alt={user.username}
											class="w-10 h-10 rounded-full bg-gray-200 dark:bg-neutral-700"
										/>
										<div>
											<div class="text-sm font-medium text-gray-900 dark:text-white">
												{user.first_name
													? `${user.first_name} ${user.last_name || ''}`
													: user.username}
											</div>
											<div class="text-xs text-gray-500 dark:text-gray-400">{user.email}</div>
										</div>
									</div>
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span
										class="px-2.5 py-1 rounded-full text-xs font-medium border"
										class:bg-purple-100={user.role === 'Superadmin'}
										class:text-purple-800={user.role === 'Superadmin'}
										class:border-purple-200={user.role === 'Superadmin'}
										class:bg-blue-100={user.role === 'Admin'}
										class:text-blue-800={user.role === 'Admin'}
										class:border-blue-200={user.role === 'Admin'}
										class:bg-gray-100={user.role === 'User'}
										class:text-gray-800={user.role === 'User'}
										class:border-gray-200={user.role === 'User'}
									>
										{user.role}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
									{getAccessDisplay(user.access)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span
										class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
										class:bg-green-100={user.is_active}
										class:text-green-800={user.is_active}
										class:bg-red-100={!user.is_active}
										class:text-red-800={!user.is_active}
									>
										<span
											class="w-1.5 h-1.5 rounded-full"
											class:bg-green-600={user.is_active}
											class:bg-red-600={!user.is_active}
										></span>
										{user.is_active ? 'Active' : 'Inactive'}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<button
										onclick={() => handleForceLogout(user.username)}
										class="px-3 py-1 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-500/10 dark:text-red-400 dark:hover:bg-red-500/20 border border-red-200 dark:border-red-500/20 rounded-lg transition-colors"
									>
										Force Logout
									</button>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
									<div
										class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity"
									>
										<button
											onclick={() => openEditModal(user)}
											class="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-500/10 rounded-lg transition-colors"
											title="Edit"
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												class="h-4 w-4"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
												/>
											</svg>
										</button>
										<button
											onclick={() => handleDelete(user.id)}
											class="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
											title="Delete"
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												class="h-4 w-4"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
												/>
											</svg>
										</button>
									</div>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>
	</div>

	{#if isModalOpen && editingUser}
		<div
			class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
			transition:fade
		>
			<div
				class="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col border border-gray-100 dark:border-white/10"
			>
				<div class="p-6 border-b border-gray-100 dark:border-white/5">
					<div class="flex items-center gap-3">
						{#if modalMode === 'create'}
							<div
								class="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-6 w-6"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0z"
									/>
								</svg>
							</div>
							<div>
								<h3 class="text-lg font-bold text-gray-900 dark:text-white">Create New User</h3>
								<p class="text-sm text-gray-500">Fill in user details and permissions.</p>
							</div>
						{:else}
							<img
								src={editingUser.avatar_url ||
									`https://ui-avatars.com/api/?name=${editingUser.username}`}
								alt="avatar"
								class="w-12 h-12 rounded-full"
							/>
							<div>
								<h3 class="text-lg font-bold text-gray-900 dark:text-white">Edit User</h3>
								<p class="text-sm text-gray-500">{editingUser.username}</p>
							</div>
						{/if}
					</div>
				</div>

				<div class="p-6 overflow-y-auto flex-1">
					<div class="grid gap-6">
						<!-- Basic Info -->
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
							<div>
								<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
									>Username</label
								>
								<input
									bind:value={editingUser.username}
									disabled={modalMode === 'edit'}
									type="text"
									class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm disabled:opacity-50"
								/>
							</div>
							<div>
								<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
									>Email</label
								>
								<input
									bind:value={editingUser.email}
									type="email"
									class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm"
								/>
							</div>
							{#if modalMode === 'create'}
								<div class="md:col-span-2">
									<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
										>Password</label
									>
									<input
										bind:value={editingUser.password}
										type="password"
										class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm"
									/>
								</div>
							{/if}
							<div>
								<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
									>First Name</label
								>
								<input
									bind:value={editingUser.first_name}
									type="text"
									class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm"
								/>
							</div>
							<div>
								<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
									>Last Name</label
								>
								<input
									bind:value={editingUser.last_name}
									type="text"
									class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm"
								/>
							</div>
						</div>

						<!-- Role Selection -->
						<div>
							<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
								>User Role</label
							>
							<select
								bind:value={editingUser.role}
								class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
							>
								<option value="User">User</option>
								<option value="Admin">Admin</option>
								<option value="Superadmin">Superadmin</option>
							</select>
						</div>

						<!-- Active Status -->
						<div class="flex items-center gap-3">
							<label class="flex items-center gap-2 cursor-pointer">
								<input
									type="checkbox"
									bind:checked={editingUser.is_active}
									class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
								/>
								<span class="text-sm font-medium text-gray-700 dark:text-gray-300">Active User</span
								>
							</label>
						</div>

						<hr class="border-gray-100 dark:border-white/5" />

						<!-- Granular Permissions -->
						<div>
							<h4
								class="text-sm font-bold text-gray-900 dark:text-white mb-4 uppercase tracking-wider"
							>
								Module Permissions
							</h4>
							<div class="grid md:grid-cols-2 gap-4">
								{#each PERMISSION_GROUPS as group}
									<div
										class="border border-gray-200 dark:border-white/10 rounded-xl p-4 bg-gray-50/50 dark:bg-white/5"
									>
										<div class="flex items-center justify-between mb-3">
											<span class="font-semibold text-gray-900 dark:text-white text-sm"
												>{group.label}</span
											>
											<!-- Select All Group Checkbox -->
											<label class="flex items-center gap-1.5 cursor-pointer">
												<input
													type="checkbox"
													checked={isModuleFullyChecked(group.id)}
													indeterminate={isModulePartiallyChecked(group.id)}
													onchange={(e) => toggleModuleAll(group.id, e.currentTarget.checked)}
													class="w-3.5 h-3.5 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
												/>
												<span class="text-xs text-gray-500">All</span>
											</label>
										</div>
										<div class="space-y-2">
											{#each group.permissions as perm}
												<label class="flex items-center gap-2 cursor-pointer">
													<input
														type="checkbox"
														checked={editingUser.access?.includes(`${group.id}.${perm.id}`)}
														onchange={(e) =>
															togglePermission(group.id, perm.id, e.currentTarget.checked)}
														class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
													/>
													<span class="text-sm text-gray-700 dark:text-gray-300">{perm.label}</span>
												</label>
											{/each}
										</div>
									</div>
								{/each}
							</div>
						</div>
					</div>
				</div>

				<div class="p-6 border-t border-gray-100 dark:border-white/5 bg-gray-50 dark:bg-white/5">
					<div class="flex gap-3">
						<button
							onclick={() => (isModalOpen = false)}
							class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl transition-all"
						>
							Cancel
						</button>
						<button
							onclick={saveUserChanges}
							class="flex-1 px-4 py-2.5 text-sm font-medium bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20"
						>
							Save Changes
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
