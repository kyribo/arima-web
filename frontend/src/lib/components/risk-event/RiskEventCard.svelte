<script lang="ts">
    import type { Incident } from '$lib/types/risk-event';
    import { formatDateID, getSeverityStyles, getStatusColor } from '$lib/utils/risk-helpers';

    let { incident, onclick } = $props<{ 
        incident: Incident;
        onclick: () => void 
    }>();
</script>

<div
	role="button"
	tabindex="0"
	{onclick}
	onkeydown={(e) => {
		if (e.key === 'Enter' || e.key === ' ') onclick();
	}}
	class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-100 dark:border-white/5 p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer group relative overflow-hidden"
>
	<!-- Severity Indicator Strip -->
	<div class="absolute left-0 top-0 bottom-0 w-1.5 {getSeverityStyles(incident.severity).bg}"></div>

	<div class="flex justify-between items-start mb-4 pl-2">
		<div>
			<span
				class="px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider {getSeverityStyles(
					incident.severity
				).badge}"
			>
				{incident.severity}
			</span>
			<h3
				class="font-bold text-lg text-gray-900 dark:text-white mt-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors"
			>
				{incident.reportTitle}
			</h3>
		</div>
		<div
			class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider {getStatusColor(
				incident.status
			)}"
		>
			{incident.status}
		</div>
	</div>

	<div class="space-y-3 pl-2">
		<div class="flex items-start gap-2">
			<span
				class="px-2 py-0.5 bg-gray-100 dark:bg-neutral-700 rounded text-xs font-mono text-gray-600 dark:text-gray-300"
			>
				{incident.clientCode}
			</span>
		</div>
		<p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 leading-relaxed">
			{incident.riskDescription}
		</p>
	</div>

	<!-- Metadata Footer -->
	<div
		class="flex items-center gap-6 mt-4 pl-2 text-xs font-medium text-gray-400 dark:text-gray-500"
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
					d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
				/>
			</svg>
			{formatDateID(incident.date)}
		</div>
		<div class="flex items-center gap-2">
			<div class="w-2 h-2 rounded-full {getSeverityStyles(incident.severity).bg}"></div>
			<span class="capitalize">{incident.severity}</span>
		</div>
		{#if incident.images?.length > 0}
			<div
				class="flex items-center gap-1.5 text-gray-500 bg-gray-100 dark:bg-neutral-700 px-2 py-0.5 rounded-full"
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
						d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
					/>
				</svg>
				{incident.images.length}
			</div>
		{/if}
		<div class="hidden md:block w-px h-3 bg-gray-300 dark:bg-neutral-600"></div>
		<span class="text-xs text-gray-500 dark:text-gray-400">Maker: {incident.maker}</span>
	</div>
</div>
