<script lang="ts">
	import { fade } from 'svelte/transition';
</script>

<svelte:head>
	<title>Capping Stock History | Arima</title>
</svelte:head>

<div in:fade={{ duration: 200 }} class="space-y-6">
	<!-- Page Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Capping Stock History</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">View historical capping stock records</p>
		</div>
		<div class="flex gap-3">
			<button
				class="px-4 py-2 bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors shadow-sm font-medium"
			>
				Export Data
			</button>
			<button
				class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium"
			>
				Filter
			</button>
		</div>
	</div>

	<!-- Content -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-gray-200 dark:border-white/5 shadow-sm"
	>
		<div class="overflow-x-auto">
			<table class="w-full">
				<thead>
					<tr class="border-b border-gray-200 dark:border-white/10">
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Date</th
						>
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Stock Code</th
						>
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Stock Name</th
						>
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Capping Value</th
						>
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Status</th
						>
						<th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300"
							>Action</th
						>
					</tr>
				</thead>
				<tbody>
					<tr
						class="border-b border-gray-100 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-neutral-700/30"
					>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">2025-12-06</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">BBCA</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">Bank Central Asia</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">10,000</td>
						<td class="py-3 px-4">
							<span
								class="px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400"
							>
								Active
							</span>
						</td>
						<td class="py-3 px-4">
							<button class="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium">
								View Details
							</button>
						</td>
					</tr>
					<tr
						class="border-b border-gray-100 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-neutral-700/30"
					>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">2025-12-05</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">BBRI</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">Bank Rakyat Indonesia</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">15,000</td>
						<td class="py-3 px-4">
							<span
								class="px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-500/10 dark:text-green-400"
							>
								Active
							</span>
						</td>
						<td class="py-3 px-4">
							<button class="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium">
								View Details
							</button>
						</td>
					</tr>
					<tr class="hover:bg-gray-50 dark:hover:bg-neutral-700/30">
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">2025-12-04</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">TLKM</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">Telkom Indonesia</td>
						<td class="py-3 px-4 text-sm text-gray-900 dark:text-white">8,500</td>
						<td class="py-3 px-4">
							<span
								class="px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 dark:bg-gray-500/10 dark:text-gray-400"
							>
								Inactive
							</span>
						</td>
						<td class="py-3 px-4">
							<button class="text-blue-600 dark:text-blue-400 hover:underline text-sm font-medium">
								View Details
							</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<div
			class="flex items-center justify-between mt-6 pt-4 border-t border-gray-200 dark:border-white/10"
		>
			<p class="text-sm text-gray-500 dark:text-gray-400">Showing 1 to 3 of 3 entries</p>
			<div class="flex gap-2">
				<button
					class="px-3 py-1.5 text-sm border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors disabled:opacity-50"
					disabled
				>
					Previous
				</button>
				<button
					class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
				>
					1
				</button>
				<button
					class="px-3 py-1.5 text-sm border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors disabled:opacity-50"
					disabled
				>
					Next
				</button>
			</div>
		</div>
	</div>
</div>
