export type IncidentSeverity = 'critical' | 'high' | 'medium' | 'low';
export type IncidentStatus = 'open' | 'resolved' | 'closed';

export interface Incident {
    id: string;
    date: string;
    time: string;

    // New Schema Fields
    reportTitle: string; // Was topic
    clientCode: string;
    // relatedRegulation removed
    riskDescription: string; // Was problem
    severity: IncidentSeverity;
    impact: string; // New
    actionTaken: string; // Was solution, Controls or Actions Taken
    followUpPlan: string; // New
    additionalNotes: string; // New

    images: string[]; // Base64 strings
    status: IncidentStatus;
    reportedBy: string;
    resolvedAt: string | null;
    maker: string;
    approver: string;
}

export type ActionType = 'create' | 'edit' | 'delete';
export type ApprovalStatus = 'pending' | 'approved' | 'rejected';

export interface ApprovalRequest {
    id: string;
    timestamp: string;
    action: ActionType;
    status: ApprovalStatus;
    payload: Partial<Incident>;
    targetIncidentId?: string;
    requestedBy: string;
    note?: string;
}
