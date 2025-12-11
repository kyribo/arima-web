<script lang="ts">
    import type { IncidentStatus, IncidentSeverity } from '$lib/types/risk-event';

    let { 
        isFiltersOpen = $bindable(false),
        dateFrom = $bindable(''),
        dateTo = $bindable(''),
        filterStatus = $bindable('all'),
        filterSeverity = $bindable('all'),
        filterMaker = $bindable('')
    } = $props();

    function clearFilters() {
        dateFrom = '';
        dateTo = '';
        filterStatus = 'all';
        filterSeverity = 'all';
        filterMaker = '';
    }
</script>

<div class="space-y-4">
	<!-- Filters Accordion -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 overflow-hidden transition-all duration-300"
	>
		<!-- Accordion Header -->
		<div
			role="button"
			tabindex="0"
			onclick={() => (isFiltersOpen = !isFiltersOpen)}
			onkeydown={(e) => {
				if (e.key === 'Enter' || e.key === ' ') isFiltersOpen = !isFiltersOpen;
			}}
			class="w-full flex items-center justify-between px-6 py-4 bg-gray-50/50 dark:bg-neutral-800/50 hover:bg-gray-100 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer select-none"
		>
			<div class="flex items-center gap-3">
				<div
					class="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg text-blue-600 dark:text-blue-400"
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
							d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
						/>
					</svg>
				</div>
				<span class="font-bold text-gray-700 dark:text-gray-200">Filter Options</span>
				{#if dateFrom || dateTo || filterStatus !== 'all' || filterSeverity !== 'all' || filterMaker}
					<span
						class="px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold"
					>
						Active
					</span>
				{/if}
			</div>
			<!-- Toggle Icon -->
			<div class="flex items-center gap-3">
				{#if dateFrom || dateTo || filterStatus !== 'all' || filterSeverity !== 'all' || filterMaker}
					<button
						onclick={(e) => {
							e.stopPropagation();
							clearFilters();
						}}
						class="text-xs font-bold text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/30 px-3 py-1.5 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors flex items-center gap-1.5"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-3.5 h-3.5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
						Clear
					</button>
				{/if}
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="w-5 h-5 text-gray-500 transition-transform duration-300 {isFiltersOpen
						? 'rotate-180'
						: ''}"
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

		<!-- Accordion Content -->
		{#if isFiltersOpen}
			<div
				class="p-6 border-t border-gray-100 dark:border-white/5 bg-gray-50/30 dark:bg-neutral-900/30"
			>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<!-- Date Range -->
					<div>
						<span class="block text-xs font-bold text-gray-500 uppercase mb-2" id="date-range-label"
							>Date Range</span
						>
						<div class="flex items-center gap-2" role="group" aria-labelledby="date-range-label">
							<input
								type="date"
								aria-label="Date From"
								bind:value={dateFrom}
								class="w-full bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500/50 outline-none dark:text-white dark:[color-scheme:dark]"
							/>
							<span class="text-gray-400">-</span>
							<input
								type="date"
								aria-label="Date To"
								bind:value={dateTo}
								class="w-full bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500/50 outline-none dark:text-white dark:[color-scheme:dark]"
							/>
						</div>
					</div>

					<!-- Status -->
					<div>
						<label class="block text-xs font-bold text-gray-500 uppercase mb-2" for="filterStatus"
							>Status</label
						>
						<div
							class="bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-xl p-1 flex"
						>
							{#each ['all', 'open', 'resolved', 'closed'] as stat}
								<button
									onclick={() => (filterStatus = stat as any)}
									class="flex-1 py-1.5 rounded-lg text-sm font-medium capitalize transition-all {filterStatus ===
									stat
										? 'bg-white dark:bg-neutral-700 text-gray-900 dark:text-white shadow-sm'
										: 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}"
								>
									{stat}
								</button>
							{/each}
						</div>
					</div>

					<!-- Severity -->
					<div>
						<label class="block text-xs font-bold text-gray-500 uppercase mb-2" for="filterSeverity"
							>Severity</label
						>
						<select
							id="filterSeverity"
							bind:value={filterSeverity}
							class="w-full bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:ring-2 focus:ring-blue-500/50 dark:text-white"
						>
							<option value="all">All Severities</option>
							<option value="critical">Critical</option>
							<option value="high">High</option>
							<option value="medium">Medium</option>
							<option value="low">Low</option>
						</select>
					</div>

					<!-- Maker -->
					<div>
						<label class="block text-xs font-bold text-gray-500 uppercase mb-2" for="filterMaker"
							>Maker</label
						>
						<input
							type="text"
							bind:value={filterMaker}
							id="filterMaker"
							placeholder="Filter by Maker name"
							class="w-full bg-gray-50 dark:bg-neutral-900 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:ring-2 focus:ring-blue-500/50 dark:text-white"
						/>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
