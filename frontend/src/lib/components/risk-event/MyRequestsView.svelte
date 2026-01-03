<script lang="ts">
    import { fade, fly } from 'svelte/transition';
    import type { ApprovalRequest } from '$lib/types/risk-event';

    let { 
        showView = $bindable(), 
        requests,
        handleViewDetails
    } = $props<{
        showView: boolean;
        requests: ApprovalRequest[];
        handleViewDetails: (req: ApprovalRequest) => void;
    }>();

    function getStatusColor(status: string) {
        switch (status) {
            case 'approved': return 'bg-green-500';
            case 'rejected': return 'bg-red-500';
            default: return 'bg-yellow-500';
        }
    }

    function getActionColor(action: string) {
        switch (action) {
            case 'create': return 'text-emerald-600 bg-emerald-100 dark:bg-emerald-900/30';
            case 'edit': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30';
            case 'delete': return 'text-red-600 bg-red-100 dark:bg-red-900/30';
            default: return 'text-gray-600 bg-gray-100';
        }
    }
</script>

<div in:fade={{ duration: 200 }} class="max-w-5xl mx-auto space-y-8 pt-6 pb-20">
	<!-- Header & Navigation -->
	<div class="flex items-center justify-between">
		<div>
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
				My Request History
				<span
					class="px-3 py-1 bg-gray-100 dark:bg-white/10 text-gray-600 dark:text-gray-300 text-sm rounded-full font-medium"
				>
					{requests.length}
				</span>
			</h2>
			<p class="text-gray-500 dark:text-gray-400 mt-1">Track the status of your submissions.</p>
		</div>
		<button
			onclick={() => (showView = false)}
			class="px-4 py-2 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-300 rounded-xl text-sm font-medium hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors"
		>
			Back to List
		</button>
	</div>

	{#if requests.length === 0}
		<div in:fade class="text-center py-32">
			<h3 class="text-xl font-bold text-gray-900 dark:text-white">No Requests Found</h3>
			<p class="text-gray-500 dark:text-gray-400 mt-2">You haven't made any requests yet.</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6">
			{#each requests as req (req.id)}
				<div
					in:fly={{ y: 20, duration: 200 }}
					class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm overflow-hidden"
				>
					<!-- Status Header -->
					<div
						class="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-white/5 bg-gray-50/50 dark:bg-white/5"
					>
						<div class="flex items-center gap-4">
							<span
								class="px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider {getActionColor(
									req.action
								)}"
							>
								{req.action}
							</span>
							<span class="text-sm font-mono text-gray-500">{req.id}</span>
							<span class="text-xs text-gray-400">{new Date(req.timestamp).toLocaleString()}</span>
						</div>
						<div class="flex items-center gap-2">
							<span class="w-2.5 h-2.5 rounded-full {getStatusColor(req.status)}"></span>
							<span class="text-sm font-bold capitalize text-gray-700 dark:text-gray-300">
								{req.status}
							</span>
						</div>
					</div>

					<div class="p-6">
						<div class="flex items-start justify-between gap-6">
							<div class="space-y-2 flex-1">
								<h4 class="text-base font-semibold text-gray-900 dark:text-white">
									{req.payload.reportTitle || `Incident ${req.targetIncidentId}`}
								</h4>
								{#if req.payload.riskDescription}
									<p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
										{req.payload.riskDescription}
									</p>
								{/if}

								{#if req.note && req.note !== 'User submission via UI'}
									<div
										class="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-100 dark:border-yellow-900/20 rounded-lg"
									>
										<p
											class="text-xs font-bold text-yellow-800 dark:text-yellow-500 uppercase mb-1"
										>
											Note / Rejection Reason
										</p>
										<p class="text-sm text-yellow-900 dark:text-yellow-200 italic">"{req.note}"</p>
									</div>
								{/if}
							</div>

							<button
								onclick={() => handleViewDetails(req)}
								class="px-4 py-2 bg-gray-100 dark:bg-neutral-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-semibold hover:bg-gray-200 dark:hover:bg-neutral-600 transition-colors shrink-0"
							>
								View Details
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
