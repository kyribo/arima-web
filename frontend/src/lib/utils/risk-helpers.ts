import type { Incident, IncidentSeverity, IncidentStatus } from '../types/risk-event';

export const generateMockIncidents = (): Incident[] => {
    const severities: IncidentSeverity[] = ['critical', 'high', 'medium', 'low'];
    const statuses: IncidentStatus[] = ['Waiting for Approval', 'Published'];
    const titles = ['System Timeout', 'Data Sync Error', 'API Latency', 'Login Failure', 'Report Delay', 'Unauthorized Access', 'Connectivity Loss', 'Database Deadlock', 'File Corruption', 'Memory Leak'];
    const makers = ['John Doe', 'Jane Smith', 'Mike Ross', 'Rachel Green', 'Harvey Specter'];
    const approvers = ['Jessica Pearson', 'Louis Litt', 'Donna Paulsen', '-'];

    const manualIncidents: Incident[] = [
        {
            id: 'INC-2024-001',
            date: '2024-12-06',
            time: '09:15',
            reportTitle: 'Market Data Feed Latency',
            clientCode: 'MKT-001',
            riskDescription: 'Observed 500ms latency in spot price updates from primary vendor during market open.',
            severity: 'critical',
            impact: 'Potential arbitrage risk and delayed execution for high-frequency trading clients.',
            actionTaken: 'Switched to secondary feed provider immediately. Logged ticket with vendor.',
            followUpPlan: 'Review vendor SLA performance and conduct failover drill next week.',
            additionalNotes: 'Latency normalized at 09:45.',
            status: 'Published',
            reportedBy: 'Ops Team',
            resolvedAt: '09:45',
            images: [],
            maker: 'Mike Ross',
            approver: 'Jessica Pearson'
        },
        {
            id: 'INC-2024-002',
            date: '2024-12-06',
            time: '11:30',
            reportTitle: 'Unauthorized API Access Attempt',
            clientCode: 'SEC-002',
            riskDescription: 'Detection of multiple failed authentication attempts from unknown IP range targeting the trading API.',
            severity: 'high',
            impact: 'Security integrity risk; potential for data breach if not blocked.',
            actionTaken: 'IP range blocked at firewall level. Account temporarily locked.',
            followUpPlan: 'Analyze access logs for pattern and enhance rate limiting rules.',
            additionalNotes: 'No successful data exfiltration detected.',
            status: 'Waiting for Approval',
            reportedBy: 'Security SOC',
            resolvedAt: null,
            images: [],
            maker: 'Jane Smith',
            approver: '-'
        },
        {
            id: 'INC-2024-003',
            date: '2024-12-06',
            time: '14:20',
            reportTitle: 'Settlement Reconciliation Discrepancy',
            clientCode: 'OPS-003',
            riskDescription: 'Mismatch of $50,000 in end-of-day settlement reports for Client A.',
            severity: 'medium',
            impact: 'Financial reporting inaccuracy and potential regulatory breach if not fixed T+1.',
            actionTaken: 'Manual trace of transaction logs initiated.',
            followUpPlan: 'Update reconciliation script to handle edge case in currency conversion.',
            additionalNotes: 'Likely due to rounding error in new forex module.',
            status: 'Waiting for Approval',
            reportedBy: 'Back Office',
            resolvedAt: null,
            images: [],
            maker: 'Rachel Green',
            approver: '-'
        },
        {
            id: 'INC-2024-004',
            date: '2024-12-05',
            time: '16:45',
            reportTitle: 'Exchange Connectivity Fluctuation',
            clientCode: 'CON-004',
            riskDescription: 'Intermittent packet loss (2%) to Exchange B connection.',
            severity: 'low',
            impact: 'Minor execution delays for non-critical orders.',
            actionTaken: 'Network team monitored the line; provider performed maintenance.',
            followUpPlan: 'Review dedicated line stability report.',
            additionalNotes: 'Resolved automatically after provider maintenance.',
            status: 'Published',
            reportedBy: 'NetOps',
            resolvedAt: '17:30',
            images: [],
            maker: 'John Doe',
            approver: 'Louis Litt'
        }
    ];

    const generated: Incident[] = Array.from({ length: 56 }).map((_, i) => {
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(i / 5)); // Spread dates back in time
        const sev = severities[i % 4];
        const stat = statuses[i % statuses.length];
        const title = titles[i % titles.length];
        return {
            id: `INC-AUTO-${100 + i}`,
            date: date.toISOString().split('T')[0],
            time: `${10 + (i % 8)}:${String(i % 60).padStart(2, '0')}`,
            reportTitle: `${title} - Batch ${Math.floor(i / 10)}`,
            clientCode: `CLI-${String(i + 10).padStart(3, '0')}`,
            riskDescription: `Automated testing entry for ${title}. Simulating various operational risks.`,
            severity: sev,
            impact: `Impact analysis for ${title} on client operations.`,
            actionTaken: 'Automated remediation script executed.',
            followUpPlan: 'Standard post-incident review.',
            additionalNotes: 'Generated mock data.',
            status: stat,
            reportedBy: 'AutoBot',
            resolvedAt: stat === 'Waiting for Approval' ? null : '18:00',
            images: [],
            maker: makers[i % makers.length],
            approver: stat === 'Waiting for Approval' ? '-' : approvers[i % approvers.length]
        };
    });

    return [...manualIncidents, ...generated];
};

export function formatDateID(dateStr: string) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).format(date);
}

export function getSeverityStyles(severity: string) {
    switch (severity) {
        case 'critical': return { bg: 'bg-red-500', text: 'text-red-700', badge: 'bg-red-50 text-red-700 border-red-200' };
        case 'high': return { bg: 'bg-orange-500', text: 'text-orange-700', badge: 'bg-orange-50 text-orange-700 border-orange-200' };
        case 'medium': return { bg: 'bg-yellow-500', text: 'text-yellow-700', badge: 'bg-yellow-50 text-yellow-700 border-yellow-200' };
        case 'low': return { bg: 'bg-blue-500', text: 'text-blue-700', badge: 'bg-blue-50 text-blue-700 border-blue-200' };
        default: return { bg: 'bg-gray-500', text: 'text-gray-700', badge: 'bg-gray-50 text-gray-700 border-gray-200' };
    }
}

export function getStatusColor(status: string) {
    switch (status) {
        case 'Waiting for Approval': return 'bg-yellow-50 text-yellow-700 border-yellow-200';
        case 'Published': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
        default: return 'bg-gray-50 text-gray-700 border-gray-200';
    }
}
