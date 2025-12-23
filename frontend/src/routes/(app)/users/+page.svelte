```ts
<script lang="ts">
	import { fade, slide } from 'svelte/transition';

    // Mock Permission Configuration
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

	// Mock Data with Granular Permissions
	let users = $state([
		{
			id: '1',
			name: 'Rizky',
			email: 'rizky@arima.com',
            role: 'Superadmin',
            access: ['*'], // * means all
			status: 'active',
			lastActive: 'Just now',
			avatar: 'https://ui-avatars.com/api/?name=Rizky&background=0D8ABC&color=fff'
		},
		{
			id: '2',
			name: 'John Doe',
			email: 'john@example.com',
            role: 'User',
            access: ['dashboard.view', 'trans_data.view'],
			status: 'inactive',
			lastActive: '2 days ago',
			avatar: 'https://ui-avatars.com/api/?name=John+Doe&background=random'
		},
		{
			id: '3',
			name: 'Sarah Smith',
			email: 'sarah@example.com',
            role: 'Admin',
            access: ['dashboard.view', 'trans_data.view', 'risk_event.view', 'risk_event.create', 'risk_event.approval', 'upload_data.view'],
			status: 'active',
			lastActive: '5 mins ago',
			avatar: 'https://ui-avatars.com/api/?name=Sarah+Smith&background=random'
		},
        {
			id: '4',
			name: 'Michael Chen',
			email: 'michael@example.com',
            role: 'User',
            access: ['dashboard.view', 'risk_event.view', 'risk_event.create'],
			status: 'active',
			lastActive: '1 hour ago',
			avatar: 'https://ui-avatars.com/api/?name=Michael+Chen&background=random'
		},
        {
			id: '5',
			name: 'Emily Davis',
			email: 'emily@example.com',
            role: 'User',
            access: ['dashboard.view'],
			status: 'active',
			lastActive: '3 hours ago',
			avatar: 'https://ui-avatars.com/api/?name=Emily+Davis&background=random'
		}
	]);

	let SearchQuery = $state('');
    let selectedUser = $state<string | null>(null);

	// Derived state logic (manual filtering since no $derived in this snippet scope simply)
    // Using a function to get filtered users or just filtering in the each block
    function getFilteredUsers() {
        return users.filter(u => 
            u.name.toLowerCase().includes(SearchQuery.toLowerCase()) ||
            u.email.toLowerCase().includes(SearchQuery.toLowerCase())
        );
    }

    function handleDelete(id: string) {
        if(confirm('Are you sure you want to delete this user? (Mock Action)')) {
            users = users.filter(u => u.id !== id);
        }
    }

    function handleForceLogout(userName: string) {
        if(confirm(`Are you sure you want to force logout ${userName}?`)) {
            alert(`User ${userName} has been forced to logout.`);
            // In real app, this would call API to revoke sessions
        }
    }

    // Edit Modal Logic
    let isEditModalOpen = $state(false);
    let editingUser = $state<any>(null); 
    
    function openEditModal(user: any) {
        // Clone to avoid direct mutation
        editingUser = JSON.parse(JSON.stringify(user));
        // If user has '*', expand it to all permissions for UI checking purposes, or handle logically.
        // For simplicity, let's keep '*' as a special case in backend, but expand in frontend edit if needed.
        // Or better, just keep it simple: if specific permission logic is complex, just manually adding string keys.
        if (editingUser.access.includes('*')) {
            // Flatten all permissions
            let allPerms: string[] = [];
            PERMISSION_GROUPS.forEach(g => {
                g.permissions.forEach(p => allPerms.push(`${g.id}.${p.id}`));
            });
            editingUser.access = allPerms;
        }
        isEditModalOpen = true;
    }

    function saveUserChanges() {
        if (!editingUser) return;
        // Update user in list
        users = users.map(u => u.id === editingUser.id ? editingUser : u);
        isEditModalOpen = false;
        editingUser = null;
    }

    // Helper to toggle a specific permission
    function togglePermission(moduleId: string, permId: string, checked: boolean) {
        const key = `${moduleId}.${permId}`;
        if (checked) {
            editingUser.access = [...editingUser.access, key];
        } else {
            editingUser.access = editingUser.access.filter((a: string) => a !== key);
        }
    }

    // Helper to toggle all permissions in a module
    function toggleModuleAll(moduleId: string, checked: boolean) {
        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return;

        const allKeys = group.permissions.map(p => `${moduleId}.${p.id}`);
        
        if (checked) {
            // Add all missing keys
            const newKeys = allKeys.filter(k => !editingUser.access.includes(k));
            editingUser.access = [...editingUser.access, ...newKeys];
        } else {
            // Remove all keys belonging to this module
            editingUser.access = editingUser.access.filter((a: string) => !a.startsWith(`${moduleId}.`));
        }
    }

    function isModuleFullyChecked(moduleId: string) {
        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return false;
        return group.permissions.every(p => editingUser.access.includes(`${moduleId}.${p.id}`));
    }
    
    function isModulePartiallyChecked(moduleId: string) {
        const group = PERMISSION_GROUPS.find(g => g.id === moduleId);
        if (!group) return false;
        const count = group.permissions.filter(p => editingUser.access.includes(`${moduleId}.${p.id}`)).length;
        return count > 0 && count < group.permissions.length;
    }

    // Helper to display access in table
    function getAccessDisplay(access: string[]) {
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
		
        <button class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Add New User
        </button>
	</div>

	<!-- Filters & Search -->
	<div class="bg-white dark:bg-neutral-800 p-4 rounded-xl border border-gray-200 dark:border-white/5 shadow-sm flex flex-col sm:flex-row gap-4">
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
				bind:value={SearchQuery}
				placeholder="Search users by name or email..."
				class="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-gray-900 dark:text-white"
			/>
		</div>
        <div class="flex gap-2">
            <select class="px-4 py-2 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-lg text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                <option value="all">All Roles</option>
                <option value="admin">Admin</option>
                <option value="user">User</option>
            </select>
             <select class="px-4 py-2 bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-lg text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
            </select>
        </div>
	</div>

	<!-- Users Table -->
	<div class="bg-white dark:bg-neutral-800 rounded-xl border border-gray-200 dark:border-white/5 shadow-sm overflow-hidden">
		<div class="overflow-x-auto">
			<table class="w-full text-left">
				<thead>
					<tr class="bg-gray-50 dark:bg-white/5 border-b border-gray-200 dark:border-white/5">
						<th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">User</th>
						<th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Role</th>
                        <th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Access</th>
						<th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
						<th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Last Active</th>
                        <th class="px-6 py-4 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Force Logout</th>
						<th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-white/5">
					{#each getFilteredUsers() as user (user.id)}
						<tr class="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors group">
							<td class="px-6 py-4 whitespace-nowrap">
								<div class="flex items-center gap-3">
									<img
										src={user.avatar}
										alt={user.name}
										class="w-10 h-10 rounded-full bg-gray-200 dark:bg-neutral-700"
									/>
									<div>
										<div class="text-sm font-medium text-gray-900 dark:text-white">{user.name}</div>
										<div class="text-xs text-gray-500 dark:text-gray-400">{user.email}</div>
									</div>
								</div>
							</td>
							<td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2.5 py-1 rounded-full text-xs font-medium border"
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
									class:bg-green-100={user.status === 'active'}
									class:text-green-800={user.status === 'active'}
                                    class:bg-red-100={user.status === 'inactive'}
									class:text-red-800={user.status === 'inactive'}
								>
									<span class="w-1.5 h-1.5 rounded-full" class:bg-green-600={user.status === 'active'} class:bg-red-600={user.status === 'inactive'}></span>
									{user.status === 'active' ? 'Active' : 'Inactive'}
								</span>
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
								{user.lastActive}
							</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <button 
                                    onclick={() => handleForceLogout(user.name)}
                                    class="px-3 py-1 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-500/10 dark:text-red-400 dark:hover:bg-red-500/20 border border-red-200 dark:border-red-500/20 rounded-lg transition-colors"
                                >
                                    Force Logout
                                </button>
                            </td>
							<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button onclick={() => openEditModal(user)} class="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-500/10 rounded-lg transition-colors" title="Edit">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button onclick={() => handleDelete(user.id)} class="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors" title="Delete">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
        
        <!-- Pagination Mock -->
        <div class="bg-gray-50 dark:bg-white/5 px-6 py-4 border-t border-gray-200 dark:border-white/5 flex items-center justify-between">
            <div class="text-sm text-gray-500 dark:text-gray-400">
                Showing <span class="font-medium">1</span> to <span class="font-medium">{getFilteredUsers().length}</span> of <span class="font-medium">{users.length}</span> results
            </div>
            <div class="flex gap-2">
                <button disabled class="px-3 py-1 text-sm border border-gray-300 dark:border-white/10 rounded-lg opacity-50 cursor-not-allowed">Previous</button>
                <button disabled class="px-3 py-1 text-sm border border-gray-300 dark:border-white/10 rounded-lg opacity-50 cursor-not-allowed">Next</button>
            </div>
        </div>
	</div>

    {#if isEditModalOpen && editingUser}
        <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" transition:fade>
            <div class="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col border border-gray-100 dark:border-white/10">
                <div class="p-6 border-b border-gray-100 dark:border-white/5">
                     <div class="flex items-center gap-3">
                        <img src={editingUser.avatar} alt="avatar" class="w-12 h-12 rounded-full" />
                        <div>
                            <h3 class="text-lg font-bold text-gray-900 dark:text-white">Edit Permissions</h3>
                            <p class="text-sm text-gray-500">{editingUser.name} &bull; {editingUser.email}</p>
                        </div>
                    </div>
                </div>

                <div class="p-6 overflow-y-auto flex-1">
                    <div class="grid gap-6">
                        <!-- Role Selection -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">User Role</label>
                            <select bind:value={editingUser.role} class="w-full px-3 py-2 bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-lg text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                                <option value="User">User</option>
                                <option value="Admin">Admin</option>
                                <option value="Superadmin">Superadmin</option>
                            </select>
                             <p class="mt-1 text-xs text-gray-500">Role defines the base level access, but specific permissions override functionality.</p>
                        </div>

                        <hr class="border-gray-100 dark:border-white/5" />

                        <!-- Granular Permissions -->
                        <div>
                             <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-4 uppercase tracking-wider">Module Permissions</h4>
                             <div class="grid md:grid-cols-2 gap-4">
                                 {#each PERMISSION_GROUPS as group}
                                    <div class="border border-gray-200 dark:border-white/10 rounded-xl p-4 bg-gray-50/50 dark:bg-white/5">
                                        <div class="flex items-center justify-between mb-3">
                                            <span class="font-semibold text-gray-900 dark:text-white text-sm">{group.label}</span>
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
                                                        checked={editingUser.access.includes(`${group.id}.${perm.id}`)}
                                                        onchange={(e) => togglePermission(group.id, perm.id, e.currentTarget.checked)}
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
                        <button onclick={() => isEditModalOpen = false} class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl transition-all">
                            Cancel
                        </button>
                        <button onclick={saveUserChanges} class="flex-1 px-4 py-2.5 text-sm font-medium bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20">
                            Save Permissions
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
