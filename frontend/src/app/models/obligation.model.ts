export interface Obligation {
  id: number;
  name: string;
  description?: string;
  due_date?: string;
  jurisdiction_level: string;
  jurisdiction?: string;
  state?: string;
  county?: string;
  city?: string;
  category?: string;
  frequency?: string;
  sources: string[];
}

export interface ObligationsResponse {
  federal: Obligation[];
  state: Obligation[];
  county: Obligation[];
  municipality: Obligation[];
}
