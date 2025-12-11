<script lang="ts">
  import { fade } from 'svelte/transition';
</script>

<div class="space-y-6" in:fade>
	<div class="flex justify-between items-center">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Weekly Report PTB</h1>
			<p class="text-sm text-gray-500 dark:text-gray-400">
				View and manage weekly reports for PTB.
			</p>
		</div>
		<div class="flex gap-3">
			<button
				class="px-4 py-2 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors"
			>
				Export
			</button>
			<button
				class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-blue-500/20"
			>
				+ New Report
			</button>
		</div>
	</div>

	<div
		class="bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/5 rounded-xl p-8 text-center py-20"
	>
		<div
			class="w-16 h-16 bg-gray-100 dark:bg-neutral-700 rounded-full flex items-center justify-center mx-auto mb-4"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="w-8 h-8 text-gray-400 dark:text-gray-500"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
				/>
			</svg>
		</div>
		<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No Reports Found</h3>
		<p class="text-gray-500 dark:text-gray-400 max-w-sm mx-auto">
			There are no weekly reports available for this period. Create a new report to get started.
		</p>
	</div>
</div>
