<script lang="ts">
	import { fade } from 'svelte/transition';

	let selectedStock = $state('');
	let cappingValue = $state('');
	let effectiveDate = $state('');
	let notes = $state('');
</script>

<svelte:head>
	<title>Capping Stock Review | Arima</title>
</svelte:head>

<div in:fade={{ duration: 200 }} class="space-y-6">
	<!-- Page Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Capping Stock Review</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Review and approve capping stock requests</p>
		</div>
	</div>

	<!-- Pending Reviews -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-gray-200 dark:border-white/5 shadow-sm"
	>
		<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Pending Reviews</h2>

		<div class="space-y-4">
			<!-- Review Item 1 -->
			<div
				class="p-4 border border-gray-200 dark:border-white/10 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/30 transition-colors"
			>
				<div class="flex items-start justify-between gap-4">
					<div class="flex-1">
						<div class="flex items-center gap-3 mb-2">
							<h3 class="text-base font-semibold text-gray-900 dark:text-white">
								BBCA - Bank Central Asia
							</h3>
							<span
								class="px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700 dark:bg-yellow-500/10 dark:text-yellow-400"
							>
								Pending Review
							</span>
						</div>
						<div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
							<div>
								<span class="text-gray-500 dark:text-gray-400">Requested Value:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">12,000</span>
							</div>
							<div>
								<span class="text-gray-500 dark:text-gray-400">Effective Date:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">2025-12-07</span>
							</div>
							<div>
								<span class="text-gray-500 dark:text-gray-400">Requested By:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">John Doe</span>
							</div>
						</div>
						<p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
							Notes: Increase capping due to high demand
						</p>
					</div>
					<div class="flex gap-2">
						<button
							class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
						>
							Approve
						</button>
						<button
							class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
						>
							Reject
						</button>
					</div>
				</div>
			</div>

			<!-- Review Item 2 -->
			<div
				class="p-4 border border-gray-200 dark:border-white/10 rounded-xl hover:bg-gray-50 dark:hover:bg-neutral-700/30 transition-colors"
			>
				<div class="flex items-start justify-between gap-4">
					<div class="flex-1">
						<div class="flex items-center gap-3 mb-2">
							<h3 class="text-base font-semibold text-gray-900 dark:text-white">
								BBRI - Bank Rakyat Indonesia
							</h3>
							<span
								class="px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700 dark:bg-yellow-500/10 dark:text-yellow-400"
							>
								Pending Review
							</span>
						</div>
						<div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
							<div>
								<span class="text-gray-500 dark:text-gray-400">Requested Value:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">18,000</span>
							</div>
							<div>
								<span class="text-gray-500 dark:text-gray-400">Effective Date:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">2025-12-08</span>
							</div>
							<div>
								<span class="text-gray-500 dark:text-gray-400">Requested By:</span>
								<span class="ml-2 font-medium text-gray-900 dark:text-white">Jane Smith</span>
							</div>
						</div>
						<p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
							Notes: Market volatility adjustment
						</p>
					</div>
					<div class="flex gap-2">
						<button
							class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
						>
							Approve
						</button>
						<button
							class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
						>
							Reject
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- New Capping Request Form -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-gray-200 dark:border-white/5 shadow-sm"
	>
		<h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
			Create New Capping Request
		</h2>

		<form class="space-y-4">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label
						for="stock"
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
					>
						Stock Code
					</label>
					<select
						id="stock"
						bind:value={selectedStock}
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
					>
						<option value="">Select stock...</option>
						<option value="BBCA">BBCA - Bank Central Asia</option>
						<option value="BBRI">BBRI - Bank Rakyat Indonesia</option>
						<option value="TLKM">TLKM - Telkom Indonesia</option>
						<option value="ASII">ASII - Astra International</option>
					</select>
				</div>

				<div>
					<label
						for="capping"
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
					>
						Capping Value
					</label>
					<input
						type="number"
						id="capping"
						bind:value={cappingValue}
						placeholder="Enter capping value"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
					/>
				</div>

				<div>
					<label for="date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Effective Date
					</label>
					<input
						type="date"
						id="date"
						bind:value={effectiveDate}
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
					/>
				</div>

				<div>
					<label
						for="notes"
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
					>
						Notes
					</label>
					<input
						type="text"
						id="notes"
						bind:value={notes}
						placeholder="Add notes (optional)"
						class="w-full bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
					/>
				</div>
			</div>

			<div class="flex justify-end gap-3 pt-4">
				<button
					type="button"
					class="px-6 py-2.5 bg-white dark:bg-neutral-700 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-600 transition-colors font-medium"
				>
					Cancel
				</button>
				<button
					type="submit"
					class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium"
				>
					Submit Request
				</button>
			</div>
		</form>
	</div>
</div>
