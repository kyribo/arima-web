<script lang="ts">
    import type { Incident } from '$lib/types/risk-event';

    let { 
        editingId, 
        formState,
        incident // Optional: if we want to show Reported By from incident object
    } = $props<{
        editingId: string | null;
        formState: any; 
        incident?: Incident;
    }>();
</script>

<div id="print-container" class="hidden">
	<div class="max-w-[210mm] mx-auto p-8 bg-white text-black font-serif">
		<!-- Header -->
		<div class="border-b-2 border-black pb-4 mb-6 flex justify-between items-end">
			<div>
				<h1 class="text-3xl font-bold uppercase tracking-wider mb-2">Risk Event Report</h1>
				<p class="text-sm">Arima Risk Management System</p>
			</div>
			<div class="text-right">
				<p class="text-xl font-bold">{editingId || 'DRAFT'}</p>
				<p class="text-sm text-gray-600">Generated on: {new Date().toLocaleDateString()}</p>
			</div>
		</div>

		<!-- Meta Grid -->
		<div class="grid grid-cols-2 gap-x-8 gap-y-4 mb-8 text-sm">
			<div class="border-b border-gray-200 pb-2">
				<span class="font-bold block text-gray-500 text-xs uppercase mb-1">Report Title</span>
				<span class="text-lg font-semibold">{formState.reportTitle}</span>
			</div>
			<div class="border-b border-gray-200 pb-2">
				<span class="font-bold block text-gray-500 text-xs uppercase mb-1">Client Code</span>
				<span class="text-lg">{formState.clientCode}</span>
			</div>
			<div class="border-b border-gray-200 pb-2">
				<span class="font-bold block text-gray-500 text-xs uppercase mb-1">Severity</span>
				<span
					class="text-lg uppercase px-2 py-0.5 border border-black rounded inline-block text-xs font-bold"
					>{formState.severity}</span
				>
			</div>
			<div class="border-b border-gray-200 pb-2">
				<span class="font-bold block text-gray-500 text-xs uppercase mb-1">Status</span>
				<span class="text-lg uppercase">{formState.status}</span>
			</div>
		</div>

		<!-- Main Content -->
		<div class="space-y-6 mb-8">
			<div>
				<h3 class="font-bold text-sm uppercase text-gray-500 mb-2 border-b border-gray-200">
					Risk Description
				</h3>
				<p class="leading-relaxed whitespace-pre-wrap">{formState.riskDescription}</p>
			</div>

			<div>
				<h3 class="font-bold text-sm uppercase text-gray-500 mb-2 border-b border-gray-200">
					Impact Assessment
				</h3>
				<p class="leading-relaxed whitespace-pre-wrap">{formState.impact || 'N/A'}</p>
			</div>

			<div>
				<h3 class="font-bold text-sm uppercase text-gray-500 mb-2 border-b border-gray-200">
					Controls / Actions Taken
				</h3>
				<p class="leading-relaxed whitespace-pre-wrap">{formState.actionTaken}</p>
			</div>

			<div>
				<h3 class="font-bold text-sm uppercase text-gray-500 mb-2 border-b border-gray-200">
					Follow-up Plan
				</h3>
				<p class="leading-relaxed whitespace-pre-wrap">{formState.followUpPlan || 'N/A'}</p>
			</div>

			{#if formState.additionalNotes}
				<div>
					<h3 class="font-bold text-sm uppercase text-gray-500 mb-2 border-b border-gray-200">
						Additional Notes
					</h3>
					<p class="leading-relaxed whitespace-pre-wrap">{formState.additionalNotes}</p>
				</div>
			{/if}
		</div>

		<!-- Gallery -->
		{#if formState.images?.length > 0}
			<div class="break-inside-avoid">
				<h3 class="font-bold text-sm uppercase text-gray-500 mb-4 border-b border-black pb-2">
					Evidence / Attachments
				</h3>
				<div class="grid grid-cols-2 gap-4">
					{#each formState.images as img}
						<div class="aspect-video ml-0 border border-gray-300 p-1">
							<img src={img} class="w-full h-full object-contain" alt="Evidence" />
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<!-- Footer / Signature -->
		<div
			class="mt-12 pt-8 border-t-2 border-black flex justify-between text-xs text-gray-500 break-inside-avoid"
		>
			<div>
				<p>Reported By: {incident?.reportedBy || 'User'}</p>
				<p>Date: {incident?.date || new Date().toLocaleDateString()}</p>
			</div>
			<div class="text-right">
				<p>Approved By: __________________________</p>
				<p class="mt-8">Date: __________________________</p>
			</div>
		</div>
	</div>
</div>

<style>
    @media print {
        /* Hide everything by default */
        :global(body > *:not(#print-container)) {
            display: none !important;
        }

        /* Show only our print container */
        #print-container {
            display: block !important;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
        }

        /* Reset page margins and background */
        @page {
            size: A4;
            margin: 2cm;
        }
        
        :global(body) {
            background: white !important;
        }
    }
</style>
