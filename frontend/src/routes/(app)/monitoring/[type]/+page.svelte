<script lang="ts">
    import { page } from '$app/stores';
    import { fade } from 'svelte/transition';

    let type = $derived($page.params.type);
    
    const titles: Record<string, string> = {
        'basic-limit': 'Basic Limit Monitoring',
        'loan-limit': 'Loan Limit Monitoring'
    };

    let title = $derived(titles[type as string] || 'Monitoring');

    // Mock Data
    const basicLimits = [
        { id: 1, user: 'John Doe', limit: 5000000, used: 2500000, status: 'Healthy' },
        { id: 2, user: 'Sarah Smith', limit: 10000000, used: 9000000, status: 'Warning' },
        { id: 3, user: 'Mike Ross', limit: 7500000, used: 100000, status: 'Healthy' },
    ];

    const loanLimits = [
        { id: 1, user: 'John Doe', maxLoan: 20000000, currentLoan: 5000000, repuchaseRate: '95%' },
        { id: 2, user: 'Jessica Pearson', maxLoan: 50000000, currentLoan: 45000000, repuchaseRate: '80%' },
    ];

    interface MonitoringData {
        id: number;
        user: string;
        limit?: number;
        used?: number;
        status?: string;
        maxLoan?: number;
        currentLoan?: number;
        repuchaseRate?: string;
    }

    let data = $derived(type === 'basic-limit' ? basicLimits as MonitoringData[] : loanLimits as MonitoringData[]);
</script>

<div in:fade class="space-y-6">
	<div class="flex justify-between items-center">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">{title}</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">
				Monitor {type === 'basic-limit' ? 'daily transaction' : 'lending'} limits.
			</p>
		</div>
		<div class="flex gap-3">
			<button
				class="px-4 py-2 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-xl text-sm font-medium hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors"
			>
				Export Report
			</button>
			<button
				class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 text-sm font-medium"
			>
				Update Limits
			</button>
		</div>
	</div>

	<!-- Stats Cards -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
		<div
			class="bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Utilization</h3>
			<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">
				{type === 'basic-limit' ? '45%' : '62%'}
			</p>
			<span class="text-xs text-green-500 font-medium flex items-center gap-1 mt-1">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-3 h-3"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path
						fill-rule="evenodd"
						d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 8.586 14.586 5H12z"
						clip-rule="evenodd"
					/>
				</svg>
				+2.5% from last month
			</span>
		</div>
		<div
			class="bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Accounts</h3>
			<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">1,248</p>
			<span class="text-xs text-gray-400 mt-1">Total registered users</span>
		</div>
		<div
			class="bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Alerts</h3>
			<p class="text-2xl font-bold text-gray-900 dark:text-white mt-2">5</p>
			<span class="text-xs text-red-500 mt-1">Requires attention</span>
		</div>
	</div>

	<!-- Data Table -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm overflow-hidden"
	>
		<div
			class="px-6 py-4 border-b border-gray-100 dark:border-white/5 flex justify-between items-center"
		>
			<h2 class="font-semibold text-gray-900 dark:text-white">Limit Details</h2>
			<div class="flex items-center gap-2">
				<input
					type="text"
					name="search-monitoring"
					autocomplete="off"
					placeholder="Search user..."
					class="bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50"
				/>
			</div>
		</div>
		<div class="overflow-x-auto">
			<table class="w-full text-left">
				<thead
					class="bg-gray-50 dark:bg-neutral-900/30 border-b border-gray-200 dark:border-white/5"
				>
					<tr>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">User</th>
						{#if type === 'basic-limit'}
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white"
								>Total Limit</th
							>
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white"
								>Used Amount</th
							>
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Status</th>
						{:else}
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Max Loan</th
							>
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white"
								>Current Loan</th
							>
							<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white"
								>Repurchase Rate</th
							>
						{/if}
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white text-right"
							>Action</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-white/5">
					{#each data as item}
						<tr class="hover:bg-gray-50 dark:hover:bg-neutral-700/30 transition-colors">
							<td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{item.user}</td>
							{#if type === 'basic-limit'}
								<td class="px-6 py-4 text-gray-500 dark:text-gray-400"
									>Rp {(item.limit ?? 0).toLocaleString()}</td
								>
								<td class="px-6 py-4 text-gray-500 dark:text-gray-400"
									>Rp {(item.used ?? 0).toLocaleString()}</td
								>
								<td class="px-6 py-4">
									<span
										class="px-2.5 py-1 rounded-lg text-xs font-medium border
                                        {item.status === 'Healthy'
											? 'bg-green-100 dark:bg-green-500/20 text-green-700 dark:text-green-300 border-green-200 dark:border-green-500/20'
											: 'bg-yellow-100 dark:bg-yellow-500/20 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-500/20'}"
									>
										{item.status}
									</span>
								</td>
							{:else}
								<td class="px-6 py-4 text-gray-500 dark:text-gray-400"
									>Rp {(item.maxLoan ?? 0).toLocaleString()}</td
								>
								<td class="px-6 py-4 text-gray-500 dark:text-gray-400"
									>Rp {(item.currentLoan ?? 0).toLocaleString()}</td
								>
								<td class="px-6 py-4 text-gray-500 dark:text-gray-400">{item.repuchaseRate}</td>
							{/if}
							<td class="px-6 py-4 text-right">
								<button class="text-blue-600 dark:text-blue-400 text-sm font-medium hover:underline"
									>Details</button
								>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
