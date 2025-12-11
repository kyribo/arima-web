<script lang="ts">
    import { page } from '$app/stores';
    import { fade, fly } from 'svelte/transition';

    let type = $derived($page.params.type);
    
    const pageInfo: Record<string, { title: string, description: string, template: string }> = {
        'due-date': {
            title: 'Upload Due Date Data',
            description: 'Upload CSV/Excel containing Account Number and New Due Date.',
            template: 'template_due_date_v1.xlsx'
        },
        'basic-limit': {
            title: 'Upload Basic Limit Data',
            description: 'Upload CSV/Excel to update Basic Limits for accounts.',
            template: 'template_basic_limit_v1.xlsx'
        },
        'reguler-limit': {
            title: 'Upload Regular Limit Data',
            description: 'Upload CSV/Excel to update Regular Limits for accounts.',
            template: 'template_reguler_limit_v1.xlsx'
        }
    };

    let info = $derived(pageInfo[type as string] || { 
        title: 'Upload Data', 
        description: 'Upload system data files.', 
        template: 'template_generic.xlsx' 
    });

    let isDragging = $state(false);
    let files = $state<File[]>([]);
    let uploadStatus = $state<'idle' | 'uploading' | 'success' | 'error'>('idle');
    let uploadProgress = $state(0);

    // Mock History
    let history = $state([
        { id: 1, filename: 'data_2023_10.csv', user: 'Rizky Hasan', date: '2023-10-25 14:00', status: 'Success', size: '2.5 MB' },
        { id: 2, filename: 'limits_v2.xlsx', user: 'Sarah Johnson', date: '2023-10-24 09:00', status: 'Success', size: '1.8 MB' },
    ]);

    function handleDragOver(e: DragEvent) {
        e.preventDefault();
        isDragging = true;
    }

    function handleDragLeave() {
        isDragging = false;
    }

    function handleDrop(e: DragEvent) {
        e.preventDefault();
        isDragging = false;
        if (e.dataTransfer?.files) {
            handleFiles(e.dataTransfer.files);
        }
    }

    function handleFileInput(e: Event) {
        const target = e.target as HTMLInputElement;
        if (target.files) {
            handleFiles(target.files);
        }
    }

    function handleFiles(fileList: FileList) {
        files = Array.from(fileList);
        uploadStatus = 'idle';
        uploadProgress = 0;
    }

    function uploadFiles() {
        if (files.length === 0) return;

        uploadStatus = 'uploading';
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            uploadProgress = progress;
            if (progress >= 100) {
                clearInterval(interval);
                uploadStatus = 'success';
                
                // Add to mock history
                history = [{
                    id: history.length + 1,
                    filename: files[0].name,
                    user: 'Rizky Hasan', // Mock user
                    date: new Date().toLocaleString(),
                    status: 'Success',
                    size: (files[0].size / 1024 / 1024).toFixed(2) + ' MB'
                }, ...history];

                setTimeout(() => {
                    files = [];
                    uploadStatus = 'idle';
                    uploadProgress = 0;
                }, 3000);
            }
        }, 200);
    }
    let activeTab = $state<'upload' | 'manual'>('upload');

    // Manual Input State
    let manualForm = $state({
        date: new Date().toISOString().split('T')[0],
        tplus: [
            createTPlusRow()
        ],
        margin: [
            createMarginRow()
        ],
        tplusRatio: [
            createTPlusRatioRow()
        ]
    });

    function createTPlusRow() {
        return {
            branch: '', sales: '', clientCode: '', clientName: '',
            t6: '', t5: '', t4: '', t3: '', t2: ''
        };
    }

    function createMarginRow() {
        return {
            branch: '', sales: '', clientCode: '', clientName: '',
            mcSequent: '', ratio: ''
        };
    }

    function createTPlusRatioRow() {
        return {
            branch: '', sales: '', clientCode: '', ratio: ''
        };
    }

    function addRow(section: 'tplus' | 'margin' | 'tplusRatio') {
        if (section === 'tplus') {
            manualForm.tplus.push(createTPlusRow());
        } else if (section === 'margin') {
            manualForm.margin.push(createMarginRow());
        } else {
            manualForm.tplusRatio.push(createTPlusRatioRow());
        }
    }

    function removeRow(section: 'tplus' | 'margin' | 'tplusRatio', index: number) {
        if (section === 'tplus') {
            if (manualForm.tplus.length > 1) {
                manualForm.tplus.splice(index, 1);
            }
        } else if (section === 'margin') {
            if (manualForm.margin.length > 1) {
                manualForm.margin.splice(index, 1);
            }
        } else {
            if (manualForm.tplusRatio.length > 1) {
                manualForm.tplusRatio.splice(index, 1);
            }
        }
    }

    let isSubmitting = $state(false);

    function handleManualSubmit() {
        isSubmitting = true;
        setTimeout(() => {
            isSubmitting = false;
            const tplusCount = manualForm.tplus.filter(r => r.clientCode).length;
            const marginCount = manualForm.margin.filter(r => r.clientCode).length;
            const tplusRatioCount = manualForm.tplusRatio.filter(r => r.clientCode).length;
            
            if (tplusCount === 0 && marginCount === 0 && tplusRatioCount === 0) {
                 alert('Please fill at least one row with Client Code.');
                 return;
            }

            alert(`Data saved!\nTPlus Rows: ${tplusCount}\nMargin Rows: ${marginCount}\nTPlus Ratio Rows: ${tplusRatioCount}`);
            
            // Reset to initial state
            manualForm.tplus = [createTPlusRow()];
            manualForm.margin = [createMarginRow()];
            manualForm.tplusRatio = [createTPlusRatioRow()];
        }, 1500);
    }
</script>

<svelte:head>
	<title>{info.title} | Arima</title>
</svelte:head>

<div in:fade class="space-y-6">
	<div class="flex justify-between items-start">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white">{info.title}</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">
				{info.description}
			</p>
		</div>
		<button
			class="px-4 py-2 bg-white dark:bg-neutral-800 border border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-200 rounded-xl text-sm font-medium hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors flex items-center gap-2"
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
					d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4-4m0 0l-4-4m4 4v12"
				/>
			</svg>
			Download {info.template}
		</button>
	</div>

	<!-- Tabs -->
	<div class="flex gap-4 border-b border-gray-200 dark:border-white/10">
		<button
			onclick={() => (activeTab = 'upload')}
			class="pb-3 px-1 text-sm font-medium transition-colors relative {activeTab === 'upload'
				? 'text-blue-600 dark:text-blue-400'
				: 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
		>
			File Upload
			{#if activeTab === 'upload'}
				<div
					class="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 dark:bg-blue-400"
					in:fade
				></div>
			{/if}
		</button>
		{#if type === 'due-date'}
			<button
				onclick={() => (activeTab = 'manual')}
				class="pb-3 px-1 text-sm font-medium transition-colors relative {activeTab === 'manual'
					? 'text-blue-600 dark:text-blue-400'
					: 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'}"
			>
				Manual Input
				{#if activeTab === 'manual'}
					<div
						class="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 dark:bg-blue-400"
						in:fade
					></div>
				{/if}
			</button>
		{/if}
	</div>

	{#if activeTab === 'upload'}
		<!-- Upload Area -->
		<div
			in:fade
			class="border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center text-center transition-all duration-200
            {isDragging
				? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10'
				: 'border-gray-200 dark:border-white/10 bg-white dark:bg-neutral-800'}"
			ondragover={handleDragOver}
			ondragleave={handleDragLeave}
			ondrop={handleDrop}
			role="button"
			tabindex="0"
		>
			{#if files.length > 0}
				<!-- ... existing file list ... -->
				<div
					class="w-full max-w-md bg-gray-50 dark:bg-neutral-900/50 p-4 rounded-xl flex items-center gap-4"
				>
					<div
						class="p-3 bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 rounded-lg"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-6 h-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
							/>
						</svg>
					</div>
					<div class="flex-1 text-left min-w-0">
						<p class="font-medium text-gray-900 dark:text-white truncate">{files[0].name}</p>
						<p class="text-sm text-gray-500 dark:text-gray-400">
							{(files[0].size / 1024 / 1024).toFixed(2)} MB
						</p>
					</div>
					<button
						onclick={() => (files = [])}
						class="p-2 text-gray-400 hover:text-red-500 transition-colors"
						aria-label="Remove file"
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
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
					</button>
				</div>

				{#if uploadStatus === 'uploading'}
					<div class="w-full max-w-md mt-4 space-y-2">
						<div class="flex justify-between text-sm">
							<span class="text-gray-600 dark:text-gray-400">Uploading...</span>
							<span class="font-medium text-blue-600 dark:text-blue-400">{uploadProgress}%</span>
						</div>
						<div class="w-full h-2 bg-gray-100 dark:bg-neutral-700 rounded-full overflow-hidden">
							<div
								class="h-full bg-blue-600 transition-all duration-200"
								style="width: {uploadProgress}%"
							></div>
						</div>
					</div>
				{:else if uploadStatus === 'success'}
					<div class="flex items-center gap-2 mt-4 text-green-600 dark:text-green-400 font-medium">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-5 h-5"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
								clip-rule="evenodd"
							/>
						</svg>
						Upload Complete!
					</div>
				{:else}
					<button
						onclick={uploadFiles}
						class="mt-6 px-8 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg shadow-blue-500/20 font-medium transition-all"
					>
						Start Upload
					</button>
				{/if}
			{:else}
				<div class="p-4 bg-gray-50 dark:bg-neutral-900/50 rounded-full mb-4">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="w-8 h-8 text-gray-400"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
						/>
					</svg>
				</div>
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white">
					Click to upload or drag and drop
				</h3>
				<p class="text-gray-500 dark:text-gray-400 mt-1 max-w-xs">
					SVG, PNG, JPG or GIF (max. 800x400px)
				</p>
				<input
					type="file"
					class="hidden"
					id="file-upload"
					onchange={handleFileInput}
					accept=".csv, .xlsx, .xls"
				/>
				<label
					for="file-upload"
					class="mt-6 px-6 py-2.5 border border-gray-200 dark:border-white/10 rounded-xl text-gray-700 dark:text-gray-300 font-medium hover:bg-gray-50 dark:hover:bg-neutral-800 transition-colors cursor-pointer"
				>
					Browse Files
				</label>
			{/if}
		</div>
	{:else}
		<!-- Manual Input Form -->
		<div
			in:fade
			class="bg-white dark:bg-neutral-800 p-8 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm space-y-6"
		>
			<h2
				class="text-lg font-semibold text-gray-900 dark:text-white border-b border-gray-100 dark:border-white/5 pb-4"
			>
				Manual Data Entry
			</h2>

			<!-- Global Date Field -->
			<div class="mb-6">
				<label
					for="global_date"
					class="block text-sm font-medium text-gray-700 dark:text-neutral-300 mb-2">Date</label
				>
				<input
					bind:value={manualForm.date}
					type="date"
					id="global_date"
					class="w-full md:w-auto bg-gray-50 dark:bg-neutral-900/50 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
				/>
			</div>

			<div class="space-y-8 overflow-x-auto">
				<!-- Section 1: TPlus Data Table -->
				<div>
					<div
						class="border-b border-gray-100 dark:border-white/5 pb-4 mb-4 flex justify-between items-end"
					>
						<h3 class="font-medium text-gray-900 dark:text-white flex items-center gap-2">
							<span
								class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-bold"
								>1</span
							>
							TPlus Data
						</h3>
						<button
							onclick={() => addRow('tplus')}
							class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Add Row</button
						>
					</div>
					<table class="w-full text-sm text-left">
						<thead
							class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-neutral-900/50 dark:text-gray-400"
						>
							<tr>
								<th class="px-3 py-3 min-w-[60px]">Branch</th>
								<th class="px-3 py-3 min-w-[60px]">Sales</th>
								<th class="px-3 py-3 min-w-[90px]">Client Code</th>
								<th class="px-3 py-3 min-w-[150px]">Client Name</th>
								<th class="px-3 py-3 w-20">T+6</th>
								<th class="px-3 py-3 w-20">T+5</th>
								<th class="px-3 py-3 w-20">T+4</th>
								<th class="px-3 py-3 w-20">T+3</th>
								<th class="px-3 py-3 w-20">T+2</th>
								<th class="px-3 py-3 w-10"></th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-100 dark:divide-white/5">
							{#each manualForm.tplus as row, i}
								<tr
									class="bg-white dark:bg-neutral-800 hover:bg-gray-50 dark:hover:bg-neutral-700/30"
								>
									<td class="p-2"
										><input
											bind:value={row.branch}
											type="text"
											placeholder="Branch"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.sales}
											type="text"
											placeholder="Sales"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.clientCode}
											type="text"
											placeholder="Code"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.clientName}
											type="text"
											placeholder="Name"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.t6}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.t5}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.t4}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.t3}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.t2}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2 text-center">
										{#if manualForm.tplus.length > 1}
											<button
												onclick={() => removeRow('tplus', i)}
												class="text-red-500 hover:text-red-700">×</button
											>
										{/if}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

				<!-- Section 2: Margin Data Table -->
				<div>
					<div
						class="border-b border-gray-100 dark:border-white/5 pb-4 mb-4 mt-8 flex justify-between items-end"
					>
						<h3 class="font-medium text-gray-900 dark:text-white flex items-center gap-2">
							<span
								class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-bold"
								>2</span
							>
							Margin Data
						</h3>
						<button
							onclick={() => addRow('margin')}
							class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Add Row</button
						>
					</div>
					<table class="w-full text-sm text-left">
						<thead
							class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-neutral-900/50 dark:text-gray-400"
						>
							<tr>
								<th class="px-3 py-3 min-w-[60px]">Branch</th>
								<th class="px-3 py-3 min-w-[60px]">Sales</th>
								<th class="px-3 py-3 min-w-[90px]">Client Code</th>
								<th class="px-3 py-3 min-w-[150px]">Client Name</th>
								<th class="px-3 py-3 min-w-[100px]">MC Sequent</th>
								<th class="px-3 py-3 min-w-[100px]">Ratio (%)</th>
								<th class="px-3 py-3 w-10"></th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-100 dark:divide-white/5">
							{#each manualForm.margin as row, i}
								<tr
									class="bg-white dark:bg-neutral-800 hover:bg-gray-50 dark:hover:bg-neutral-700/30"
								>
									<td class="p-2"
										><input
											bind:value={row.branch}
											type="text"
											placeholder="Branch"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.sales}
											type="text"
											placeholder="Sales"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.clientCode}
											type="text"
											placeholder="Code"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.clientName}
											type="text"
											placeholder="Name"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.mcSequent}
											type="number"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2"
										><input
											bind:value={row.ratio}
											type="number"
											step="0.01"
											class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
										/></td
									>
									<td class="p-2 text-center">
										{#if manualForm.margin.length > 1}
											<button
												onclick={() => removeRow('margin', i)}
												class="text-red-500 hover:text-red-700">×</button
											>
										{/if}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>

			<!-- Section 3: TPlus Ratio Table -->
			<div>
				<div
					class="border-b border-gray-100 dark:border-white/5 pb-4 mb-4 mt-8 flex justify-between items-end"
				>
					<h3 class="font-medium text-gray-900 dark:text-white flex items-center gap-2">
						<span
							class="flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-bold"
							>3</span
						>
						TPlus Ratio
					</h3>
					<button
						onclick={() => addRow('tplusRatio')}
						class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Add Row</button
					>
				</div>
				<table class="w-full text-sm text-left">
					<thead
						class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-neutral-900/50 dark:text-gray-400"
					>
						<tr>
							<th class="px-3 py-3 min-w-[60px]">Branch</th>
							<th class="px-3 py-3 min-w-[60px]">Sales</th>
							<th class="px-3 py-3 min-w-[90px]">Client Code</th>
							<th class="px-3 py-3 min-w-[100px]">Ratio (%)</th>
							<th class="px-3 py-3 w-10"></th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-100 dark:divide-white/5">
						{#each manualForm.tplusRatio as row, i}
							<tr
								class="bg-white dark:bg-neutral-800 hover:bg-gray-50 dark:hover:bg-neutral-700/30"
							>
								<td class="p-2"
									><input
										bind:value={row.branch}
										type="text"
										placeholder="Branch"
										class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
									/></td
								>
								<td class="p-2"
									><input
										bind:value={row.sales}
										type="text"
										placeholder="Sales"
										class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
									/></td
								>
								<td class="p-2"
									><input
										bind:value={row.clientCode}
										type="text"
										placeholder="Code"
										class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
									/></td
								>
								<td class="p-2"
									><input
										bind:value={row.ratio}
										type="number"
										step="0.01"
										class="w-full bg-transparent border-none focus:ring-0 text-sm p-0"
									/></td
								>
								<td class="p-2 text-center">
									{#if manualForm.tplusRatio.length > 1}
										<button
											onclick={() => removeRow('tplusRatio', i)}
											class="text-red-500 hover:text-red-700">×</button
										>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div class="flex justify-end pt-4 border-t border-gray-100 dark:border-white/5">
				<button
					onclick={handleManualSubmit}
					disabled={isSubmitting}
					class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg shadow-blue-500/20 font-medium disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2 transition-all"
				>
					{#if isSubmitting}
						<div
							class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
						></div>
						Saving...
					{:else}
						Submit Data
					{/if}
				</button>
			</div>
		</div>
	{/if}

	<!-- Upload History -->
	<div
		class="bg-white dark:bg-neutral-800 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm overflow-hidden"
	>
		<div class="px-6 py-4 border-b border-gray-100 dark:border-white/5">
			<h2 class="font-semibold text-gray-900 dark:text-white">Upload History</h2>
		</div>
		<div class="overflow-x-auto">
			<table class="w-full text-left">
				<thead
					class="bg-gray-50 dark:bg-neutral-900/30 border-b border-gray-200 dark:border-white/5"
				>
					<tr>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Filename</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white"
							>Uploaded By</th
						>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Date</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white">Size</th>
						<th class="px-6 py-4 text-sm font-semibold text-gray-900 dark:text-white text-right"
							>Status</th
						>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 dark:divide-white/5">
					{#each history as item}
						<tr class="hover:bg-gray-50 dark:hover:bg-neutral-700/30 transition-colors">
							<td
								class="px-6 py-4 font-medium text-gray-900 dark:text-white flex items-center gap-2"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-4 h-4 text-gray-400"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
									/>
								</svg>
								{item.filename}
							</td>
							<td class="px-6 py-4 text-gray-500 dark:text-gray-400">{item.user}</td>
							<td class="px-6 py-4 text-gray-500 dark:text-gray-400 text-sm">{item.date}</td>
							<td class="px-6 py-4 text-gray-500 dark:text-gray-400 text-sm">{item.size}</td>
							<td class="px-6 py-4 text-right">
								<span
									class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-500/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-500/20"
								>
									<span class="w-1.5 h-1.5 rounded-full bg-green-600 dark:bg-green-400"></span>
									{item.status}
								</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
