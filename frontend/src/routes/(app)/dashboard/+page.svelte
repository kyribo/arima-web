<script lang="ts">
  const stats = [
    { title: 'Total Revenue', value: '$45,231.89', change: '+20.1%', trend: 'up', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
    { title: 'Active Users', value: '+2350', change: '+180.1%', trend: 'up', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
    { title: 'Sales', value: '+12,234', change: '+19%', trend: 'up', icon: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z' },
    { title: 'Active Now', value: '+573', change: '+201', trend: 'up', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
  ];
  
  const recentSetup = [
    { name: 'Server Configuration', status: 'Completed', date: '2h ago', color: 'green' },
    { name: 'Database Migration', status: 'In Progress', date: '4h ago', color: 'blue' },
    { name: 'User Authentication', status: 'Pending', date: '1d ago', color: 'gray' },
    { name: 'API Integration', status: 'Failed', date: '2d ago', color: 'red' },
  ];
</script>

<div class="space-y-8">
	<!-- Welcome Section -->
	<div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
		<div>
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white">Overview</h1>
			<p class="text-gray-500 dark:text-gray-400 mt-1">
				Here's what's happening with your projects today.
			</p>
		</div>
		<div class="flex gap-3">
			<button
				class="px-4 py-2 bg-white dark:bg-neutral-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-white/10 rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors shadow-sm font-medium"
			>
				Download Report
			</button>
			<button
				class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/20 font-medium"
			>
				New Project
			</button>
		</div>
	</div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		{#each stats as stat}
			<div
				class="bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm hover:shadow-md transition-shadow"
			>
				<div class="flex items-center justify-between mb-4">
					<div
						class="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-500/10 flex items-center justify-center text-blue-600 dark:text-blue-400"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-6 h-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={stat.icon} />
						</svg>
					</div>
					<span
						class="text-sm font-medium px-2.5 py-1 rounded-full bg-green-50 dark:bg-green-500/10 text-green-600 dark:text-green-400"
					>
						{stat.change}
					</span>
				</div>
				<h3 class="text-gray-500 dark:text-gray-400 text-sm font-medium">{stat.title}</h3>
				<p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{stat.value}</p>
			</div>
		{/each}
	</div>

	<!-- Content Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
		<!-- Chart Placeholder -->
		<div
			class="lg:col-span-2 bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<div class="flex justify-between items-center mb-6">
				<h3 class="text-lg font-semibold text-gray-900 dark:text-white">Revenue Analytics</h3>
				<select
					class="bg-gray-50 dark:bg-neutral-700 border border-gray-200 dark:border-transparent rounded-lg text-sm px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
				>
					<option>Last 7 days</option>
					<option>Last 30 days</option>
					<option>Last year</option>
				</select>
			</div>
			<div
				class="h-[300px] w-full bg-gradient-to-t from-blue-50 dark:from-blue-500/5 to-transparent rounded-xl border border-dashed border-gray-200 dark:border-white/10 flex items-center justify-center relative overflow-hidden group"
			>
				<div class="absolute inset-0 flex items-end justify-around px-4 opacity-50">
					{#each [40, 70, 45, 90, 65, 80, 55] as height}
						<div
							class="w-1/12 bg-blue-500/20 rounded-t-lg transition-all duration-500 group-hover:bg-blue-500/30"
							style="height: {height}%"
						></div>
					{/each}
				</div>
				<span class="text-gray-400 dark:text-gray-500 relative z-10"
					>Chart Visualization Placeholder</span
				>
			</div>
		</div>

		<!-- Recent Activity -->
		<div
			class="bg-white dark:bg-neutral-800 p-6 rounded-2xl border border-gray-200 dark:border-white/5 shadow-sm"
		>
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Recent Activity</h3>
			<div class="space-y-6">
				{#each recentSetup as item}
					<div class="flex items-start gap-4">
						<div class="w-2 h-2 mt-2 rounded-full bg-blue-500 shrink-0"></div>
						<div class="flex-1 min-w-0">
							<p class="text-sm font-medium text-gray-900 dark:text-white truncate">{item.name}</p>
							<div class="flex items-center gap-2 mt-1">
								<span class="text-xs text-gray-500 dark:text-gray-400">{item.date}</span>
								<span
									class="px-1.5 py-0.5 rounded text-[10px] font-medium
                  {item.status === 'Completed'
										? 'bg-green-100 dark:bg-green-500/10 text-green-700 dark:text-green-400'
										: item.status === 'In Progress'
											? 'bg-blue-100 dark:bg-blue-500/10 text-blue-700 dark:text-blue-400'
											: item.status === 'Failed'
												? 'bg-red-100 dark:bg-red-500/10 text-red-700 dark:text-red-400'
												: 'bg-gray-100 dark:bg-gray-500/10 text-gray-700 dark:text-gray-400'}"
								>
									{item.status}
								</span>
							</div>
						</div>
					</div>
				{/each}
			</div>
			<button
				class="w-full mt-6 py-2.5 text-sm font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-500/10 rounded-lg transition-colors"
			>
				View All History
			</button>
		</div>
	</div>
</div>
