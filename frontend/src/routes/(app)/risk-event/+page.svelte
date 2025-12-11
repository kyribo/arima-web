<script lang="ts">
	import { fade } from 'svelte/transition';
    import { onMount } from 'svelte';
    
    // Logic Imports
    import type { Incident, IncidentSeverity, IncidentStatus, ApprovalRequest } from '$lib/types/risk-event';
    import { generateMockIncidents } from '$lib/utils/risk-helpers';

    // Components
    import RiskEventCard from '$lib/components/risk-event/RiskEventCard.svelte';
    import FilterSection from '$lib/components/risk-event/FilterSection.svelte';
    import InboxView from '$lib/components/risk-event/InboxView.svelte';
    import RiskEventModal from '$lib/components/risk-event/RiskEventModal.svelte';
    import PrintLayout from '$lib/components/risk-event/PrintLayout.svelte';

	// --- State ---
	let showInbox = $state(false); 
	
	// Date Filters
	let dateFrom = $state('');
	let dateTo = $state('');
    
    // Pagination
    let currentPage = $state(1);
    let itemsPerPage = $state(10);
	
	// Filters
	let filterStatus = $state<'all' | IncidentStatus>('all');
	let filterSeverity = $state<'all' | IncidentSeverity>('all');
    let filterMaker = $state('');
    let isFiltersOpen = $state(false);

	let incidents = $state<Incident[]>(generateMockIncidents());

	// Mock Data: Approval Requests
	let approvalRequests = $state<ApprovalRequest[]>([
		{
			id: 'REQ-002',
			timestamp: new Date().toISOString(),
			action: 'create',
			status: 'pending',
			payload: {
                reportTitle: 'Suspicious Transaction Pattern (High Value) - New Entry',
                clientCode: 'CL-998877',
                riskDescription: 'Detected multiple high value transactions within short timeframe, potential money laundering.',
                severity: 'high',
                impact: 'Compliance risk and potential fines.',
                actionTaken: 'Account frozen temporarily.',
                followUpPlan: 'Conduct enhanced due diligence.',
                additionalNotes: 'Waiting for compliance officer review.',
                images: [],
                status: 'open',
                date: new Date().toISOString().split('T')[0]
            },
			targetIncidentId: '', // New entry doesn't have an ID yet or the payload contains the proposed ID
			requestedBy: 'Risk Analyst',
			note: 'New risk event derived from automated monitoring.'
		},
		{
			id: 'REQ-001',
			timestamp: new Date().toISOString(),
			action: 'delete',
			status: 'pending',
			payload: {},
			targetIncidentId: 'INC-2024-004',
			requestedBy: 'System Admin',
			note: 'Duplicate entry detected during audit.'
		}
	]);

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
		status: 'open' as IncidentStatus,
        date: ''
	});

	// --- Derived ---
	let filteredIncidents = $derived(
		incidents.filter((inc) => {
			const matchStatus = filterStatus === 'all' || inc.status === filterStatus;
			const matchSeverity = filterSeverity === 'all' || inc.severity === filterSeverity;
			const matchDateFrom = !dateFrom || inc.date >= dateFrom;
			const matchDateTo = !dateTo || inc.date <= dateTo;
            const matchMaker = !filterMaker || inc.maker.toLowerCase().includes(filterMaker.toLowerCase());
			return matchStatus && matchSeverity && matchDateFrom && matchDateTo && matchMaker;
		})
	);

    let totalPages = $derived(Math.ceil(filteredIncidents.length / itemsPerPage));
    let paginatedIncidents = $derived(
        filteredIncidents.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
    );
    
    // Reset to page 1 when filters change
    $effect(() => {
        // Track dependencies
        filterStatus; filterSeverity; dateFrom; dateTo; filterMaker;
        // Effect logic
        currentPage = 1;
    });

	let pendingRequests = $derived(approvalRequests.filter(r => r.status === 'pending'));

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
			status: 'open',
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

    function handleSubmit(e: Event) {
        e.preventDefault();
        
        // Validation (simple)
        if (!formState.reportTitle || !formState.clientCode || !formState.riskDescription) {
            alert('Please fill in required fields');
            return;
        }

        if (modalMode === 'create') {
            const newIncident: Incident = {
                id: `INC-NEW-${Date.now()}`,
                date: formState.date || new Date().toISOString().split('T')[0],
                time: new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }),
                reportTitle: formState.reportTitle,
                clientCode: formState.clientCode,
                riskDescription: formState.riskDescription,
                severity: formState.severity,
                impact: formState.impact,
                actionTaken: formState.actionTaken,
                followUpPlan: formState.followUpPlan,
                additionalNotes: formState.additionalNotes,
                images: formState.images,
                status: 'open',
                reportedBy: 'Current User',
                resolvedAt: null,
                maker: 'Current User',
                approver: '-'
            };
            incidents = [newIncident, ...incidents];
        } else if (modalMode === 'edit' && editingId) {
            incidents = incidents.map(inc => {
                if (inc.id === editingId) {
                    return {
                        ...inc,
                        reportTitle: formState.reportTitle,
                        clientCode: formState.clientCode,
                        riskDescription: formState.riskDescription,
                        severity: formState.severity,
                        impact: formState.impact,
                        actionTaken: formState.actionTaken,
                        followUpPlan: formState.followUpPlan,
                        additionalNotes: formState.additionalNotes,
                        images: formState.images,
                        date: formState.date
                    };
                }
                return inc;
            });
        }
        closeModal();
    }

    function handleDelete(id: string) {
		if(confirm('Are you sure you want to request deletion for this incident?')) {
            const request: ApprovalRequest = {
                id: `REQ-${Date.now()}`,
                timestamp: new Date().toISOString(),
                action: 'delete',
                status: 'pending',
                payload: {},
                targetIncidentId: id,
                requestedBy: 'Current User', // TODO: Auth
                note: 'User requested deletion'
            };
            approvalRequests = [request, ...approvalRequests];
            showModal = false;
            alert('Deletion request submitted for approval.');
        }
	}

    function handleApprove(req: ApprovalRequest) {
		if (confirm('Approve this request?')) {
			if (req.action === 'delete') {
				incidents = incidents.filter(i => i.id !== req.targetIncidentId);
			} else if (req.action === 'create' && req.payload) {
                // ... create logic implementation if needed
            } else if (req.action === 'edit' && req.payload) {
                // ... edit logic implementation if needed
            }
            
			approvalRequests = approvalRequests.map(r => 
				r.id === req.id ? { ...r, status: 'approved' } : r
			);
		}
	}

	function handleReject(id: string) {
		if (confirm('Reject this request?')) {
			approvalRequests = approvalRequests.map(r => 
				r.id === id ? { ...r, status: 'rejected' } : r
			);
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
            status: targetData.status || 'open',
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
        const headers = [
            'ID', 'Date', 'Time', 'Title', 'Client', 'Severity', 'Status', 
            'Description', 'Impact', 'Actions', 'Follow Up', 'Notes', 'Maker', 'Approver'
        ];
        
        const rows = filteredIncidents.map(inc => [
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
		class="sticky top-0 z-40 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border-b border-gray-200 dark:border-white/5"
	>
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
			<div>
				<h1 class="text-2xl font-bold text-gray-900 dark:text-white">Risk Events</h1>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5 hidden sm:block">
					Track, analyze, and resolve operational risk events.
				</p>
			</div>
			<div class="flex items-center gap-3">
				<button
					onclick={() => (showInbox = !showInbox)}
					class="relative px-5 py-3 bg-white dark:bg-neutral-800 rounded-xl shadow-sm border border-gray-200 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2"
				>
					Inbox
					{#if pendingRequests.length > 0}
						<span class="w-2 h-2 bg-red-500 rounded-full"></span>
					{/if}
				</button>
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
			</div>
		</div>
	</header>

	<!-- Main Content Area -->
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{#if !showInbox}
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
						Records ({filteredIncidents.length})
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
			<div class="space-y-4 mt-6">
				{#each paginatedIncidents as incident (incident.id)}
					<div in:fade={{ duration: 200, delay: 50 }}>
						<RiskEventCard {incident} onclick={() => openViewModal(incident)} />
					</div>
				{/each}

				{#if filteredIncidents.length === 0}
					<div
						class="col-span-full text-center py-20 bg-gray-50 dark:bg-neutral-800/50 rounded-3xl border border-dashed border-gray-300 dark:border-neutral-700"
					>
						<p class="text-gray-500">No reports found strictly matching criteria.</p>
					</div>
				{/if}
			</div>

			<!-- Pagination Controls -->
			{#if totalPages > 1}
				<div class="flex justify-center gap-2 mt-12 mb-8">
					<button
						disabled={currentPage === 1}
						onclick={() => currentPage--}
						class="px-4 py-2 rounded-lg bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-neutral-700 text-gray-700 dark:text-gray-300 transition-colors"
					>
						Previous
					</button>
					<div class="flex items-center gap-1 font-mono text-sm">
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
					</div>
					<button
						disabled={currentPage === totalPages}
						onclick={() => currentPage++}
						class="px-4 py-2 rounded-lg bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-neutral-700 text-gray-700 dark:text-gray-300 transition-colors"
					>
						Next
					</button>
				</div>
			{/if}
		{:else}
			<!-- Inbox View -->
			<InboxView
				bind:showInbox
				{pendingRequests}
				{handleApprove}
				{handleReject}
				{handleViewDetails}
			/>
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
