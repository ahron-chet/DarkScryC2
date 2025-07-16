export interface Agent {
    agent_id: string;
    host_name: string;
    os: string;
    last_time_update?: string;
    onboarded_time?: string;
    is_active?: boolean;
    address?: string;
}