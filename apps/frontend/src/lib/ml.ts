export type PredictFromFeatures = {
  attendance_pct: number;
  assignments_pct: number;
  quizzes_pct: number;
  exams_pct: number;
  gpa: number;
};

export type PredictionRequest = {
  academic_record_id?: string | null;
  student_user_id?: string | null;
  features?: PredictFromFeatures | null;
  threshold?: number;
};

export type PredictionResponse = {
  classification: string;
  risk_probability: number;
  confidence: number;
  threshold: number;
  model_version: string;
};

export type ExplainRequest = {
  academic_record_id?: string | null;
  student_user_id?: string | null;
  features?: PredictFromFeatures | null;
  top_k?: number;
};

export type FactorPublic = {
  feature_key: string;
  feature_label: string;
  value: number;
  impact: number;
  direction: string;
  unit?: string | null;
};

export type ExplainResponse = {
  model_version: string;
  factors: FactorPublic[];
};

export type ModelInfo = {
  model_version: string;
  created_at: string;
  metrics: Record<string, number>;
  feature_names: string[];
  notes: string;
};

export type TrainRequest = {
  notes?: string;
  min_rows?: number;
};

export type TrainResponse = {
  trained: boolean;
  model: ModelInfo;
};

export type ModelListResponse = {
  latest_version: string | null;
  items: ModelInfo[];
};

export type PromoteResponse = {
  latest_version: string;
  model: ModelInfo;
};
