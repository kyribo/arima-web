<script lang="ts">
	import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
    
    // Logic Imports
    import type { Incident, IncidentSeverity, IncidentStatus, ApprovalRequest } from '$lib/types/risk-event';
    import { api } from '$lib/api';
    import { user } from '$lib/stores/user';
    import { hasPermission, PERMISSIONS } from '$lib/utils/permissions';
    import { toast } from '$lib/stores/toast';

    // Components
    import RiskEventCard from '$lib/components/risk-event/RiskEventCard.svelte';
    import FilterSection from '$lib/components/risk-event/FilterSection.svelte';
    import InboxView from '$lib/components/risk-event/InboxView.svelte';
    import MyRequestsView from '$lib/components/risk-event/MyRequestsView.svelte';
    import RiskEventModal from '$lib/components/risk-event/RiskEventModal.svelte';
    import PrintLayout from '$lib/components/risk-event/PrintLayout.svelte';

	// --- State ---
	let showInbox = $state(false); 
    let showHistory = $state(false);
	
	// Date Filters
	let dateFrom = $state('');
	let dateTo = $state('');
    
    // Pagination
    let currentPage = $state(1);
    let itemsPerPage = $state(10);
    let totalPages = $state(1);
    let totalRecords = $state(0);
	
	// Filters
	let filterStatus = $state<'all' | IncidentStatus>('all');
	let filterSeverity = $state<'all' | IncidentSeverity>('all');
    let filterMaker = $state('');
    let isFiltersOpen = $state(false);

	let incidents = $state<Incident[]>([]);

	// Approval Requests
	let approvalRequests = $state<ApprovalRequest[]>([]);
    let myRequests = $state<ApprovalRequest[]>([]);
    let isLoading = $state(false);

	// Modal State
	let showModal = $state(false);
	let modalMode = $state<'create' | 'edit' | 'view'>('create');
	let editingId = $state<string | null>(null);
	
	let formState = $state({
		reportTitle: '',
		clientCode: '',
		riskDescription: '',
		severity: 'medium' as IncidentSeverity,
		impact: '',
		actionTaken: '',
		followUpPlan: '',
		additionalNotes: '',
		images: [] as string[],
		status: 'Waiting for Approval' as IncidentStatus,
        date: ''
	});

	// --- Derived ---
    
    // Reset to page 1 when filters change
    $effect(() => {
        // Track filters
        filterStatus; filterSeverity; dateFrom; dateTo; filterMaker;
        currentPage = 1; 
    });

    // Reload when page or filters change (debounced effect or explicit call)
    $effect(() => {
        // Dependencies to trigger reload
        currentPage; filterStatus; filterSeverity; dateFrom; dateTo; filterMaker;
        loadIncidents();
    });

	let pendingRequests = $derived(approvalRequests.filter(r => r.status === 'pending'));

    function toggleInbox() {
        showInbox = !showInbox;
        if (showInbox) showHistory = false;
    }

    function toggleHistory() {
        showHistory = !showHistory;
        if (showHistory) {
            showInbox = false;
            loadMyRequests();
        }
    }

    async function loadIncidents() {
        isLoading = true;
        try {
            const res = await api.get('/risk-events/', {
                 params: {
                     status: filterStatus === 'all' ? undefined : filterStatus,
                     severity: filterSeverity === 'all' ? undefined : filterSeverity,
                     maker: filterMaker || undefined,
                     date_from: dateFrom || undefined,
                     date_to: dateTo || undefined,
                     page: currentPage,
                     limit: itemsPerPage
                 }
            });
            
            // Server now returns { items, total, page, pages }
            const items = res.items || [];
            totalPages = res.pages || 1;
            totalRecords = res.total || 0;
            
            incidents = items.map((i: any) => ({
                id: i.id,
                reportTitle: i.report_title,
                clientCode: i.client_code,
                riskDescription: i.risk_description,
                severity: i.severity,
                impact: i.impact,
                actionTaken: i.action_taken,
                followUpPlan: i.follow_up_plan,
                additionalNotes: i.additional_notes,
                images: i.images,
                status: i.status,
                date: i.date,
                time: i.time,
                maker: i.maker,
                approver: i.approver,
                reportedBy: i.maker,
                resolvedAt: i.resolved_at
            }));

            // If page is out of bounds (e.g. after filtering), reset to 1
            if (currentPage > totalPages && totalPages > 0) {
                currentPage = 1;
            }

        } catch (e) {
            console.error(e);
            toast.error('Failed to load risk events');
        } finally {
            isLoading = false;
        }
    }

    async function loadPendingRequests() {
        try {
            const res = await api.get('/risk-events/approvals/pending');
            approvalRequests = res.map((r: any) => ({
                id: r.id,
                timestamp: r.timestamp,
                action: r.action,
                status: r.status,
                payload: r.payload,
                targetIncidentId: r.target_incident_id,
                requestedBy: r.requested_by_id, 
                note: r.note
            }));
        } catch (e) {
            console.error(e);
        }
    }

    async function loadMyRequests() {
        try {
            const res = await api.get('/risk-events/requests/mine');
            myRequests = res.map((r: any) => ({
                id: r.id,
                timestamp: r.timestamp,
                action: r.action,
                status: r.status,
                payload: r.payload,
                targetIncidentId: r.target_incident_id,
                requestedBy: r.requested_by_id, 
                note: r.note
            }));
        } catch (e) {
            console.error(e);
        }
    }

    onMount(() => {
        loadIncidents();
        loadPendingRequests();
    });

    // Permission Checks
    let canCreate = $derived(hasPermission($user, PERMISSIONS.RISK_EVENT.CREATE));
    let canApprove = $derived(hasPermission($user, PERMISSIONS.RISK_EVENT.APPROVE));

	// --- Actions ---
	function openCreateModal() {
		modalMode = 'create';
		formState = {
			reportTitle: '',
			clientCode: '',
			riskDescription: '',
			severity: 'medium',
			impact: '',
			actionTaken: '',
			followUpPlan: '',
			additionalNotes: '',
			images: [],
			status: 'Waiting for Approval',
            date: new Date().toISOString().split('T')[0]
		};
		showModal = true;
	}

	function openEditModal(incident: Incident) {
		modalMode = 'edit';
		editingId = incident.id;
		formState = {
			reportTitle: incident.reportTitle,
			clientCode: incident.clientCode,
			riskDescription: incident.riskDescription,
			severity: incident.severity,
			impact: incident.impact,
			actionTaken: incident.actionTaken,
			followUpPlan: incident.followUpPlan,
			additionalNotes: incident.additionalNotes,
			images: [...incident.images],
			status: incident.status,
            date: incident.date
		};
		showModal = true;
	}

    function openViewModal(incident: Incident) {
        modalMode = 'view';
        editingId = incident.id;
        formState = {
            reportTitle: incident.reportTitle,
            clientCode: incident.clientCode,
            riskDescription: incident.riskDescription,
            severity: incident.severity,
            impact: incident.impact,
            actionTaken: incident.actionTaken,
            followUpPlan: incident.followUpPlan,
            additionalNotes: incident.additionalNotes,
            images: [...incident.images],
            status: incident.status,
            date: incident.date
        };
        showModal = true;
    }

	function closeModal() {
		showModal = false;
		editingId = null;
	}

    async function handleSubmit(e: Event) {
        e.preventDefault();
        
        // Validation (simple)
        if (!formState.date || !formState.reportTitle || !formState.clientCode || !formState.riskDescription || !formState.actionTaken) {
            toast.warning('Please fill in required fields');
            return;
        }

        const payload = {
             action: modalMode === 'create' ? 'create' : 'edit',
             target_incident_id: modalMode === 'edit' ? editingId : undefined,
             payload: {
                reportTitle: formState.reportTitle,
                clientCode: formState.clientCode,
                riskDescription: formState.riskDescription,
                severity: formState.severity,
                impact: formState.impact,
                actionTaken: formState.actionTaken,
                followUpPlan: formState.followUpPlan,
                additionalNotes: formState.additionalNotes,
                images: formState.images,
                status: formState.status,
                date: formState.date
             },
             note: 'User submission via UI'
        };

        try {
            await api.post('/risk-events/request', payload);
            toast.success('Request submitted for approval');
            closeModal();
            loadPendingRequests();
            if (showHistory) loadMyRequests();
        } catch (e) {
            console.error(e);
            toast.error('Failed to submit request');
        }
    }

    async function handleDelete(id: string) {
		if(confirm('Are you sure you want to request deletion for this incident?')) {
            try {
                await api.post('/risk-events/request', {
                    action: 'delete',
                    target_incident_id: id,
                    payload: {},
                    note: 'User requested deletion via UI'
                });
                toast.success('Deletion request submitted for approval');
                closeModal();
                loadPendingRequests();
                if (showHistory) loadMyRequests();
            } catch (e) {
                console.error(e);
                toast.error('Failed to submit deletion request');
            }
        }
	}

    async function handleApprove(req: ApprovalRequest) {
		if (confirm('Approve this request?')) {
            try {
    			await api.post(`/risk-events/approvals/${req.id}/approve`, {});
                toast.success('Request approved');
                loadPendingRequests();
                loadIncidents(); 
                if (showHistory) loadMyRequests();
            } catch (e: any) {
                console.error(e);
                toast.error('Failed to approve request');
            }
		}
	}

	async function handleReject(id: string) {
		if (confirm('Reject this request?')) {
            try {
    			await api.post(`/risk-events/approvals/${id}/reject`, {});
                toast.success('Request rejected');
                loadPendingRequests();
                if (showHistory) loadMyRequests();
            } catch (e: any) {
                console.error(e);
                toast.error('Failed to reject request');
            }
		}
	}

    function handleViewDetails(req: ApprovalRequest) {
        modalMode = 'view';
        editingId = req.targetIncidentId || null;
        
        let targetData: any = {};

        if (req.action === 'create' || req.action === 'edit') {
            targetData = req.payload;
        } else if (req.action === 'delete') {
            const existing = incidents.find(i => i.id === req.targetIncidentId);
            if (existing) targetData = existing;
        }

        formState = {
            reportTitle: targetData.reportTitle || '',
            clientCode: targetData.clientCode || '',
            riskDescription: targetData.riskDescription || '',
            severity: targetData.severity || 'medium',
            impact: targetData.impact || '',
            actionTaken: targetData.actionTaken || '',
            followUpPlan: targetData.followUpPlan || '',
            additionalNotes: targetData.additionalNotes || '',
            images: targetData.images || [],
            status: targetData.status || 'Waiting for Approval',
            date: targetData.date || new Date().toISOString().split('T')[0]
        };
        
        showModal = true;
    }

    function handlePrint() {
		// Wait for print layout to render data
		setTimeout(() => {
			window.print();
		}, 100);
	}

    function exportToCSV() {
        // Export current page only (or filtered set if we implement full export later)
        const headers = [
            'ID', 'Date', 'Time', 'Report Title', 'Client Code', 'Severity', 'Status',
            'Risk Description', 'Impact', 'Action Taken', 'Follow Up Plan', 'Additional Notes',
            'Maker', 'Approver'
        ];
        const rows = incidents.map(inc => [
            inc.id, inc.date, inc.time, `"${inc.reportTitle}"`, inc.clientCode, inc.severity, inc.status,
            `"${inc.riskDescription?.replace(/"/g, '""')}"`,
            `"${inc.impact?.replace(/"/g, '""')}"`,
            `"${inc.actionTaken?.replace(/"/g, '""')}"`,
            `"${inc.followUpPlan?.replace(/"/g, '""')}"`,
            `"${inc.additionalNotes?.replace(/"/g, '""')}"`,
            inc.maker, inc.approver
        ]);

        const csvContent = [
            headers.join(','),
            ...rows.map(r => r.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `risk_events_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
    }
</script>

<div class="min-h-screen bg-gray-50 dark:bg-neutral-900 transition-colors duration-300">
	<!-- Header -->
	<header
		class="sticky top-16 z-30 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border-b border-gray-200 dark:border-white/5 transition-all duration-300"
	>
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
			<div>
				<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Risk Events</h1>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5 hidden sm:block">
					Track, analyze, and resolve operational risk events.
				</p>
			</div>
			<div class="flex items-center gap-3">
				{#if canApprove}
					<button
						onclick={toggleInbox}
						class="relative px-5 py-3 {showInbox
							? 'bg-blue-600 text-white'
							: 'bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-300 scale-95 hover:scale-100'} rounded-xl shadow-sm border border-gray-200 dark:border-white/5 transition-all font-semibold flex items-center gap-2"
					>
						Inbox
						{#if pendingRequests.length > 0}
							<span class="w-2 h-2 bg-red-500 rounded-full"></span>
						{/if}
					</button>
				{/if}

				<button
					onclick={toggleHistory}
					class="relative px-5 py-3 {showHistory
						? 'bg-blue-600 text-white'
						: 'bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-300 scale-95 hover:scale-100'} rounded-xl shadow-sm border border-gray-200 dark:border-white/5 transition-all font-semibold flex items-center gap-2"
				>
					My Requests
				</button>

				{#if canCreate}
					<button
						onclick={openCreateModal}
						class="px-5 py-3 bg-blue-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-600/20 hover:bg-blue-700 hover:scale-105 active:scale-95 transition-all flex items-center gap-2"
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
						New Entry
					</button>
				{/if}
			</div>
		</div>
	</header>

	<!-- Main Content Area -->
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{#if !showInbox && !showHistory}
			<!-- Filter Section -->
			<FilterSection
				bind:isFiltersOpen
				bind:dateFrom
				bind:dateTo
				bind:filterStatus
				bind:filterSeverity
				bind:filterMaker
			/>

			<!-- Stats & Export Bar -->
			<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mt-6">
				<div>
					<h2 class="text-lg font-bold text-gray-900 dark:text-white">
						Records ({totalRecords})
					</h2>
					<p class="text-sm text-gray-500">
						Page {currentPage} of {totalPages || 1}
					</p>
				</div>
				<button
					onclick={exportToCSV}
					class="px-4 py-2 bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 text-sm font-bold flex items-center gap-2"
				>
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
							d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
						/>
					</svg>
					Export CSV
				</button>
			</div>

			<!-- Card Grid -->
			<div class="space-y-4 mt-6 min-h-[400px]">
				{#if isLoading}
					<!-- Loading Skeletons -->
					{#each Array(3) as _}
						<div
							class="bg-white dark:bg-neutral-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-white/5 animate-pulse"
						>
							<div class="flex items-start justify-between">
								<div class="flex items-center gap-4">
									<div class="w-2 h-16 rounded-full bg-gray-200 dark:bg-neutral-700"></div>
									<div class="space-y-3">
										<div class="h-4 w-24 bg-gray-200 dark:bg-neutral-700 rounded"></div>
										<div class="h-6 w-48 bg-gray-200 dark:bg-neutral-700 rounded"></div>
										<div class="h-4 w-32 bg-gray-200 dark:bg-neutral-700 rounded"></div>
									</div>
								</div>
							</div>
						</div>
					{/each}
				{:else}
					{#each incidents as incident (incident.id)}
						<div in:fade={{ duration: 200, delay: 50 }}>
							<RiskEventCard {incident} onclick={() => openViewModal(incident)} />
						</div>
					{/each}

					{#if incidents.length === 0}
						<div
							class="col-span-full text-center py-20 bg-gray-50 dark:bg-neutral-800/50 rounded-3xl border border-dashed border-gray-300 dark:border-neutral-700 flex flex-col items-center justify-center gap-4"
						>
							<p class="text-gray-500">No reports found matching criteria.</p>
							{#if filterStatus !== 'all' || filterSeverity !== 'all' || filterMaker || dateFrom || dateTo}
								<button
									onclick={() => {
										filterStatus = 'all';
										filterSeverity = 'all';
										filterMaker = '';
										dateFrom = '';
										dateTo = '';
										currentPage = 1;
									}}
									class="text-blue-600 font-medium hover:underline text-sm"
								>
									Clear all filters
								</button>
							{/if}
						</div>
					{/if}
				{/if}
			</div>

			<!-- Pagination Controls -->
			{#if totalPages > 1}
				<div class="flex justify-center gap-2 mt-12 mb-8 items-center">
					<button
						disabled={currentPage === 1 || isLoading}
						onclick={() => currentPage--}
						class="px-4 py-2 rounded-lg bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-neutral-700 text-gray-700 dark:text-gray-300 transition-colors"
					>
						Previous
					</button>

					<!-- Smart Pagination -->
					<div class="flex items-center gap-1 font-mono text-sm">
						{#if totalPages <= 7}
							{#each Array(totalPages) as _, i}
								<button
									onclick={() => (currentPage = i + 1)}
									class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors {currentPage ===
									i + 1
										? 'bg-blue-600 text-white font-bold'
										: 'hover:bg-gray-100 dark:hover:bg-neutral-800 text-gray-600 dark:text-gray-400'}"
								>
									{i + 1}
								</button>
							{/each}
						{:else}
							<button
								onclick={() => (currentPage = 1)}
								class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors {currentPage ===
								1
									? 'bg-blue-600 text-white font-bold'
									: 'hover:bg-gray-100 dark:hover:bg-neutral-800 text-gray-600 dark:text-gray-400'}"
								>1</button
							>

							{#if currentPage > 3}
								<span class="w-8 h-8 flex items-center justify-center text-gray-400">...</span>
							{/if}

							{#each Array(totalPages) as _, i}
								{#if i + 1 !== 1 && i + 1 !== totalPages && Math.abs(currentPage - (i + 1)) <= 1}
									<button
										onclick={() => (currentPage = i + 1)}
										class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors {currentPage ===
										i + 1
											? 'bg-blue-600 text-white font-bold'
											: 'hover:bg-gray-100 dark:hover:bg-neutral-800 text-gray-600 dark:text-gray-400'}"
									>
										{i + 1}
									</button>
								{/if}
							{/each}

							{#if currentPage < totalPages - 2}
								<span class="w-8 h-8 flex items-center justify-center text-gray-400">...</span>
							{/if}

							<button
								onclick={() => (currentPage = totalPages)}
								class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors {currentPage ===
								totalPages
									? 'bg-blue-600 text-white font-bold'
									: 'hover:bg-gray-100 dark:hover:bg-neutral-800 text-gray-600 dark:text-gray-400'}"
								>{totalPages}</button
							>
						{/if}
					</div>

					<button
						disabled={currentPage === totalPages || isLoading}
						onclick={() => currentPage++}
						class="px-4 py-2 rounded-lg bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-neutral-700 text-gray-700 dark:text-gray-300 transition-colors"
					>
						Next
					</button>
				</div>
			{/if}
		{:else if showInbox}
			<!-- Inbox View -->
			<InboxView
				bind:showInbox
				{pendingRequests}
				{handleApprove}
				{handleReject}
				{handleViewDetails}
				{canApprove}
			/>
		{:else if showHistory}
			<!-- My Requests View -->
			<MyRequestsView bind:showView={showHistory} requests={myRequests} {handleViewDetails} />
		{/if}
	</main>

	<!-- Modal -->
	<RiskEventModal
		bind:showModal
		bind:formState
		{modalMode}
		{incidents}
		{editingId}
		{handleSubmit}
		{handleDelete}
		{handlePrint}
		onClose={closeModal}
		onEdit={openEditModal}
		allowPrint={!showInbox}
	/>

	<!-- Print Layout -->
	<PrintLayout {editingId} {formState} incident={incidents.find((i) => i.id === editingId)} />
</div>
