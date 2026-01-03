<script lang="ts">
    import { flip } from 'svelte/animate';
    import { fade, fly } from 'svelte/transition';
    import { toast } from '$lib/stores/toast';

    function getIcon(type: string) {
        switch (type) {
            case 'success':
                return '<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>';
            case 'error':
                return '<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>';
            case 'warning':
                return '<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>';
            default:
                return '<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>';
        }
    }

    function getColor(type: string) {
        switch (type) {
            case 'success': return 'bg-white border-l-4 border-green-500 text-gray-800 dark:bg-neutral-800 dark:text-white';
            case 'error': return 'bg-white border-l-4 border-red-500 text-gray-800 dark:bg-neutral-800 dark:text-white';
            case 'warning': return 'bg-white border-l-4 border-yellow-500 text-gray-800 dark:bg-neutral-800 dark:text-white';
            default: return 'bg-white border-l-4 border-blue-500 text-gray-800 dark:bg-neutral-800 dark:text-white';
        }
    }
</script>

<div class="fixed bottom-6 right-6 z-[60] flex flex-col gap-3 pointer-events-none">
	{#each $toast as t (t.id)}
		<div
			animate:flip
			in:fly={{ x: 20, duration: 300 }}
			out:fade={{ duration: 200 }}
			class="{getColor(
				t.type
			)} p-4 rounded-lg shadow-lg pointer-events-auto min-w-[300px] flex items-start gap-3"
			role="alert"
		>
			<div
				class={t.type === 'success'
					? 'text-green-500'
					: t.type === 'error'
						? 'text-red-500'
						: t.type === 'warning'
							? 'text-yellow-500'
							: 'text-blue-500'}
			>
				{@html getIcon(t.type)}
			</div>
			<div class="flex-1 text-sm font-medium">
				{t.message}
			</div>
			<button
				onclick={() => toast.dismiss(t.id)}
				aria-label="Dismiss notification"
				class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
			>
				<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					/>
				</svg>
			</button>
		</div>
	{/each}
</div>
