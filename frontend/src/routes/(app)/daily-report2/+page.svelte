<script lang="ts">
	import { fade, slide, fly, crossfade } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	// --- Types ---
	type IncidentSeverity = 'critical' | 'high' | 'medium' | 'low';
	type IncidentStatus = 'open' | 'resolved' | 'closed';

	interface Incident {
		id: string;
		date: string;
		time: string;
		title: string;
		description: string;
		severity: IncidentSeverity;
		status: IncidentStatus;
		reportedBy: string;
		assignedTo: string;
		resolvedAt: string | null;
	}

	// --- Animation ---
	const [send, receive] = crossfade({
		duration: 300,
		easing: cubicOut,
		fallback: (node, params) => {
            const style = getComputedStyle(node);
            const transform = style.transform === 'none' ? '' : style.transform;
            
            return {
                duration: 300,
                easing: cubicOut,
                css: (t) => `
                    transform: ${transform} scale(${t});
                    opacity: ${t}
                `
            };
        }
	});

	// --- State ---
	let selectedDate = $state(new Date().toISOString().split('T')[0]);
	
	// Filters
	let filterStatus = $state<'all' | IncidentStatus>('all');
	let filterSeverity = $state<'all' | IncidentSeverity>('all');

	// Mock Data: Incidents
	let incidents = $state<Incident[]>([
		{
			id: 'INC-2024-001',
			date: '2024-12-06',
			time: '09:15',
			title: 'System Downtime - Trading Platform',
			description: 'Trading platform experienced unexpected downtime during opening hours.',
			severity: 'critical',
			status: 'resolved',
			reportedBy: 'John Doe',
			assignedTo: 'IT Team',
			resolvedAt: '09:30'
		},
		{
			id: 'INC-2024-002',
			date: '2024-12-06',
			time: '11:30',
			title: 'Data Sync Error',
			description: 'Client portfolio data failed to sync with main database, affecting 50 users.',
			severity: 'high',
			status: 'open',
			reportedBy: 'Sarah Johnson',
			assignedTo: 'Database Team',
			resolvedAt: null
		},
		{
			id: 'INC-2024-003',
			date: '2024-12-06',
			time: '14:20',
			title: 'Login Issues - Mobile App',
			description: 'Multiple users reported unable to login via mobile application v2.1.',
			severity: 'medium',
			status: 'open',
			reportedBy: 'Support Team',
			assignedTo: 'Mobile Dev Team',
			resolvedAt: null
		},
		{
			id: 'INC-2024-004',
			date: '2024-12-05',
			time: '16:45',
			title: 'Report Generation Delay',
			description: 'Daily report generation took longer than expected by 15 minutes.',
			severity: 'low',
			status: 'closed',
			reportedBy: 'Admin',
			assignedTo: 'Backend Team',
			resolvedAt: '17:00'
		}
	]);

	// Modal State
	let showModal = $state(false);
	let modalMode = $state<'create' | 'edit'>('create');
	let editingId = $state<string | null>(null);
	
	let formState = $state({
		title: '',
		description: '',
		severity: 'medium' as IncidentSeverity,
		status: 'open' as IncidentStatus,
		assignedTo: 'Pending Assignment'
	});

	// --- Derived ---
	let filteredIncidents = $derived(
		incidents.filter((inc) => {
			const matchStatus = filterStatus === 'all' || inc.status === filterStatus;
			const matchSeverity = filterSeverity === 'all' || inc.severity === filterSeverity;
			return matchStatus && matchSeverity;
		})
	);

	let stats = $derived({
		total: incidents.length,
		open: incidents.filter((i) => i.status === 'open').length,
		resolved: incidents.filter((i) => i.status === 'resolved').length,
		critical: incidents.filter((i) => i.severity === 'critical').length
	});

	// --- Helpers ---
	function getSeverityStyles(severity: string) {
		switch (severity) {
			case 'critical': return { bg: 'bg-red-500', text: 'text-red-700', badge: 'bg-red-50 text-red-700 border-red-200' };
			case 'high': return { bg: 'bg-orange-500', text: 'text-orange-700', badge: 'bg-orange-50 text-orange-700 border-orange-200' };
			case 'medium': return { bg: 'bg-yellow-500', text: 'text-yellow-700', badge: 'bg-yellow-50 text-yellow-700 border-yellow-200' };
			case 'low': return { bg: 'bg-blue-500', text: 'text-blue-700', badge: 'bg-blue-50 text-blue-700 border-blue-200' };
			default: return { bg: 'bg-gray-500', text: 'text-gray-700', badge: 'bg-gray-50 text-gray-700 border-gray-200' };
		}
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'open': return 'bg-purple-50 text-purple-700 border-purple-200';
			case 'resolved': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
			case 'closed': return 'bg-gray-50 text-gray-700 border-gray-200';
			default: return 'bg-gray-50 text-gray-700 border-gray-200';
		}
	}

	// --- Actions ---
	function openCreateModal() {
		modalMode = 'create';
		formState = {
			title: '',
			description: '',
			severity: 'medium',
			status: 'open',
			assignedTo: ''
		};
		showModal = true;
	}

	function openEditModal(incident: Incident) {
		modalMode = 'edit';
		editingId = incident.id;
		formState = {
			title: incident.title,
			description: incident.description,
			severity: incident.severity,
			status: incident.status,
			assignedTo: incident.assignedTo
		};
		showModal = true;
	}

	function closeModal() {
		showModal = false;
		editingId = null;
	}

	function handleFormSubmit() {
		const now = new Date();
		
		if (modalMode === 'create') {
			const newId = `INC-2024-${String(incidents.length + 1).padStart(3, '0')}`;
			const newIncident: Incident = {
				id: newId,
				date: now.toISOString().split('T')[0],
				time: now.toTimeString().slice(0, 5),
				reportedBy: 'User',
				resolvedAt: null,
				title: formState.title,
				description: formState.description,
				severity: formState.severity,
				status: formState.status,
				assignedTo: formState.assignedTo || 'Unassigned'
			};
			incidents = [newIncident, ...incidents];
		} else if (modalMode === 'edit' && editingId) {
			incidents = incidents.map(inc => 
				inc.id === editingId 
					? { ...inc, ...formState } 
					: inc
			);
		}

		closeModal();
	}

	function handleDelete(id: string) {
		if(!confirm('Are you sure you want to delete this incident?')) return;
		incidents = incidents.filter(inc => inc.id !== id);
	}
</script>

<svelte:head>
	<title>Daily Incidents (Direct) | Arima</title>
</svelte:head>

<div class="max-w-7xl mx-auto space-y-8 pb-12">
	<!-- Top Section: Header & Actions -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
		<div in:fly={{ y: -20, duration: 500 }}>
			<h1
				class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent"
			>
				Daily Incidents (Direct)
			</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-2 text-lg">
				Operational oversight with direct management.
			</p>
		</div>
		<div class="flex gap-3" in:fly={{ y: -20, duration: 500, delay: 100 }}>
			<button
				onclick={() => alert(`Exporting ${selectedDate}`)}
				class="px-5 py-2.5 bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-white/10 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-all shadow-sm hover:shadow font-medium flex items-center gap-2 group"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4-4m0 0l-4 4m4-4v12"
					/>
				</svg>
				Export Report
			</button>
			<button
				onclick={openCreateModal}
				class="px-5 py-2.5 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-xl hover:bg-black dark:hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-0.5 font-medium flex items-center gap-2"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-5 h-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 4v16m8-8H4"
					/>
				</svg>
				New Incident
			</button>
		</div>
	</div>

	<!-- Stats Overview (Premium Cards) -->
	<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
		<div
			class="p-6 rounded-2xl bg-gradient-to-br from-white to-gray-50 dark:from-neutral-800 dark:to-neutral-900 border border-gray-200/50 dark:border-white/5 shadow-sm relative overflow-hidden group"
		>
			<div
				class="absolute right-0 top-0 w-32 h-32 bg-gray-100 dark:bg-white/5 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform duration-500"
			></div>
			<p class="text-sm font-medium text-gray-500 dark:text-gray-400 relative z-10">
				Total Incidents
			</p>
			<p class="text-4xl font-bold text-gray-900 dark:text-white mt-2 relative z-10">
				{stats.total}
			</p>
		</div>
		<div
			class="p-6 rounded-2xl bg-gradient-to-br from-red-50 to-white dark:from-red-900/20 dark:to-neutral-900 border border-red-100 dark:border-red-500/10 shadow-sm relative overflow-hidden group"
		>
			<div
				class="absolute right-0 top-0 w-32 h-32 bg-red-100 dark:bg-red-500/10 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform duration-500"
			></div>
			<p class="text-sm font-medium text-red-600 dark:text-red-400 relative z-10">Open Issues</p>
			<p class="text-4xl font-bold text-red-700 dark:text-red-400 mt-2 relative z-10">
				{stats.open}
			</p>
		</div>
		<div
			class="p-6 rounded-2xl bg-gradient-to-br from-emerald-50 to-white dark:from-emerald-900/20 dark:to-neutral-900 border border-emerald-100 dark:border-emerald-500/10 shadow-sm relative overflow-hidden group"
		>
			<div
				class="absolute right-0 top-0 w-32 h-32 bg-emerald-100 dark:bg-emerald-500/10 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform duration-500"
			></div>
			<p class="text-sm font-medium text-emerald-600 dark:text-emerald-400 relative z-10">
				Resolved
			</p>
			<p class="text-4xl font-bold text-emerald-700 dark:text-emerald-400 mt-2 relative z-10">
				{stats.resolved}
			</p>
		</div>
		<div
			class="p-6 rounded-2xl bg-gradient-to-br from-orange-50 to-white dark:from-orange-900/20 dark:to-neutral-900 border border-orange-100 dark:border-orange-500/10 shadow-sm relative overflow-hidden group"
		>
			<div
				class="absolute right-0 top-0 w-32 h-32 bg-orange-100 dark:bg-orange-500/10 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform duration-500"
			></div>
			<p class="text-sm font-medium text-orange-600 dark:text-orange-400 relative z-10">Critical</p>
			<p class="text-4xl font-bold text-orange-700 dark:text-orange-400 mt-2 relative z-10">
				{stats.critical}
			</p>
		</div>
	</div>

	<!-- Filters Bar -->
	<div in:fade={{ duration: 200 }} class="flex flex-col md:flex-row gap-4 p-1">
		<div class="flex-1 relative group">
			<div class="absolute inset-y-0 left-3 flex items-center pointer-events-none">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-5 h-5 text-gray-400"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
					/>
				</svg>
			</div>
			<input
				type="date"
				bind:value={selectedDate}
				class="w-full bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl pl-10 pr-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-gray-900 dark:focus:ring-white focus:border-transparent outline-none transition-shadow shadow-sm"
			/>
		</div>

		<div class="flex gap-4 flex-1">
			<select
				bind:value={filterStatus}
				class="flex-1 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-gray-900 dark:focus:ring-white outline-none shadow-sm cursor-pointer"
			>
				<option value="all">All Status</option>
				<option value="open">Open</option>
				<option value="resolved">Resolved</option>
				<option value="closed">Closed</option>
			</select>

			<select
				bind:value={filterSeverity}
				class="flex-1 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-gray-900 dark:focus:ring-white outline-none shadow-sm cursor-pointer"
			>
				<option value="all">All Severity</option>
				<option value="critical">Critical</option>
				<option value="high">High</option>
				<option value="medium">Medium</option>
				<option value="low">Low</option>
			</select>
		</div>
	</div>

	<!-- List View -->
	<div class="space-y-3">
		{#each filteredIncidents as incident (incident.id)}
			<div
				in:fly|local={{ y: 20, duration: 300 }}
				animate:flip={{ duration: 300 }}
				class="group bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-transparent dark:border-white/5 hover:border-gray-200 dark:hover:border-neutral-700 shadow-sm hover:shadow-lg transition-all duration-300 relative overflow-hidden"
			>
				<!-- Severity Strip -->
				<div
					class="absolute left-0 top-0 bottom-0 w-1 {getSeverityStyles(incident.severity).bg}"
				></div>

				<div class="flex flex-col md:flex-row gap-6">
					<!-- Content -->
					<div class="flex-1 pl-3">
						<div class="flex items-center gap-3 mb-2 flex-wrap">
							<h3
								class="text-lg font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors"
							>
								{incident.title}
							</h3>
							<span
								class="px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider border {getStatusColor(
									incident.status
								)}"
							>
								{incident.status}
							</span>
						</div>

						<p class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed max-w-2xl">
							{incident.description}
						</p>

						<!-- Metadata Footer -->
						<div
							class="flex items-center gap-6 mt-4 text-xs font-medium text-gray-400 dark:text-gray-500"
						>
							<div class="flex items-center gap-2">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-4 h-4"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
									/>
								</svg>
								{incident.time}
							</div>
							<div class="flex items-center gap-2">
								<div
									class="w-5 h-5 rounded-full bg-gray-100 dark:bg-neutral-700 flex items-center justify-center text-[9px] font-bold text-gray-600 dark:text-gray-300"
								>
									{incident.assignedTo.substring(0, 2).toUpperCase()}
								</div>
								{incident.assignedTo}
							</div>
							<div class="flex items-center gap-2">
								<div class="w-2 h-2 rounded-full {getSeverityStyles(incident.severity).bg}"></div>
								<span class="capitalize">{incident.severity}</span>
							</div>
						</div>
					</div>

					<!-- Hover Actions (Slide in) -->
					<div
						class="flex md:flex-col items-center justify-center gap-2 opacity-100 md:opacity-0 md:translate-x-4 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300 ease-out pl-3 md:border-l border-gray-100 dark:border-white/5"
					>
						<button
							onclick={() => openEditModal(incident)}
							class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-500/10 rounded-lg transition-colors"
							title="Edit"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="w-5 h-5"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
								/>
							</svg>
						</button>
						<button
							onclick={() => handleDelete(incident.id)}
							class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
							title="Delete"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="w-5 h-5"
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
				</div>
			</div>
		{/each}

		{#if filteredIncidents.length === 0}
			<div
				class="text-center py-20 bg-gray-50 dark:bg-neutral-800/50 rounded-3xl border border-dashed border-gray-300 dark:border-neutral-700"
			>
				<p class="text-gray-500">No reports found strictly matching criteria.</p>
			</div>
		{/if}
	</div>

	<!-- Modal (Refined) -->
	{#if showModal}
		<div
			class="fixed inset-0 bg-black/60 backdrop-blur-md z-50 flex items-center justify-center p-4"
			onclick={(e) => {
				if (e.target === e.currentTarget) closeModal();
			}}
			onkeydown={(e) => {
				if (e.key === 'Escape') closeModal();
			}}
			role="button"
			tabindex="0"
			transition:fade={{ duration: 200 }}
		>
			<div
				class="bg-white dark:bg-neutral-900 rounded-3xl p-8 max-w-2xl w-full shadow-2xl border border-gray-200 dark:border-white/10"
				role="document"
				transition:fly={{ y: 20, duration: 300 }}
			>
				<h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-8">
					{modalMode === 'create' ? 'New Incident' : 'Edit Incident'}
				</h2>

				<form
					onsubmit={(e) => {
						e.preventDefault();
						handleFormSubmit();
					}}
					class="space-y-6"
				>
					<div>
						<label
							for="title"
							class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Title</label
						>
						<input
							type="text"
							id="title"
							bind:value={formState.title}
							required
							placeholder="E.g., System Latency in Region A"
							class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
						/>
					</div>

					<div>
						<label
							for="description"
							class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>Description</label
						>
						<textarea
							id="description"
							bind:value={formState.description}
							required
							rows="4"
							placeholder="Detailed description..."
							class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white transition-shadow"
						></textarea>
					</div>

					<div class="grid grid-cols-2 gap-6">
						<div>
							<label
								for="severity"
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
								>Severity</label
							>
							<div class="relative">
								<select
									id="severity"
									bind:value={formState.severity}
									class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white appearance-none"
								>
									<option value="low">Low</option>
									<option value="medium">Medium</option>
									<option value="high">High</option>
									<option value="critical">Critical</option>
								</select>
								<div class="absolute inset-y-0 right-4 flex items-center pointer-events-none">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="w-4 h-4 text-gray-400"
										fill="none"
										viewBox="0 0 24 24"
										stroke="currentColor"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								</div>
							</div>
						</div>
						<div>
							<label
								for="assigned"
								class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
								>Assigned To</label
							>
							<input
								type="text"
								id="assigned"
								bind:value={formState.assignedTo}
								placeholder="Team or Person"
								class="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white outline-none focus:ring-2 focus:ring-gray-900 dark:focus:ring-white"
							/>
						</div>
					</div>

					<div class="pt-6 flex justify-end gap-3">
						<button
							type="button"
							onclick={closeModal}
							class="px-6 py-3 font-medium text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-neutral-800 rounded-xl transition-colors"
						>
							Cancel
						</button>
						<button
							type="submit"
							class="px-8 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold rounded-xl shadow-xl hover:scale-105 active:scale-95 transition-all"
						>
							{modalMode === 'create' ? 'Create Incident' : 'Save Changes'}
						</button>
					</div>
				</form>
			</div>
		</div>
	{/if}
</div>
