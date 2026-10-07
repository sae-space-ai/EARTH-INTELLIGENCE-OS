// AI Subsystem Types for Earth Intelligence OS

export type ModelFamily =
  | 'MULTIMODAL_FOUNDATION_MODEL'
  | 'LIDAR_ENCODER'
  | 'SAR_ENCODER'
  | 'OPTICAL_ENCODER'
  | 'HYPERSPECTRAL_ENCODER'
  | 'MULTIMODAL_FUSION'
  | 'CHANGE_DETECTION'
  | 'ANOMALY_DETECTION'
  | 'SEMANTIC_SEGMENTATION'
  | 'OBJECT_DETECTION'
  | 'LAND_COVER_CLASSIFICATION'
  | 'FIRE_DETECTION'
  | 'WEATHER_MODEL'
  | 'TEMPORAL_FORECAST_MODEL'
  | 'WORLD_MODEL'
  | 'EMBEDDING_MODEL'
  | 'RERANKER'
  | 'LLM'
  | 'VISION_LANGUAGE_MODEL'
  | 'SMALL_EDGE_MODEL'
  | 'OTHER';

export type ModelStatus =
  | 'REGISTERED'
  | 'TRAINING'
  | 'VALIDATING'
  | 'VALIDATED'
  | 'REJECTED'
  | 'PROMOTED'
  | 'DEPLOYED'
  | 'RETIRED';

export type TrainingJobStatus =
  | 'QUEUED'
  | 'PREPARING'
  | 'RUNNING'
  | 'VALIDATING'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED';

export type DeploymentTarget =
  | 'GROUND_CPU'
  | 'GROUND_GPU'
  | 'EDGE_SIMULATION'
  | 'FUTURE_SPACECRAFT';

export type ActionRiskLevel =
  | 'READ_ONLY'
  | 'UI_ACTION'
  | 'DATA_MUTATION'
  | 'COMPUTE_JOB'
  | 'MODEL_DEPLOYMENT'
  | 'MISSION_PROPOSAL'
  | 'SPACECRAFT_COMMAND';

export type ApprovalStatus =
  | 'PENDING'
  | 'APPROVED'
  | 'REJECTED'
  | 'EXPIRED'
  | 'CANCELLED';

export interface ModelDefinition {
  id: string;
  name: string;
  family: ModelFamily;
  architecture: string;
  task: string;
  modalities: string[];
  framework: string;
  input_schema: Record<string, any>;
  output_schema: Record<string, any>;
  default_config: Record<string, any>;
  parameter_count?: number;
  training_supported: boolean;
  inference_supported: boolean;
  edge_compatible: boolean;
  metadata: Record<string, any>;
  created_at: string;
}

export interface ModelVersion {
  id: string;
  model_definition_id: string;
  semantic_version: string;
  git_commit: string;
  checkpoint_uri: string;
  checkpoint_sha256: string;
  training_dataset_version: string;
  config_hash: string;
  metrics: Record<string, number>;
  parameter_count: number;
  framework: string;
  precision: string;
  status: ModelStatus;
  created_at: string;
}

export interface DatasetDefinition {
  id: string;
  name: string;
  description: string;
  modalities: string[];
  providers: string[];
  spatial_extent?: {
    type: string;
    coordinates: number[][][];
  };
  temporal_extent?: {
    start: string;
    end: string;
  };
  sample_count: number;
  asset_count: number;
  schema: Record<string, any>;
  normalization: Record<string, any>;
  license: string;
  access_policy: string;
  manifest_uri: string;
  manifest_sha256: string;
  created_at: string;
}

export interface TrainingJob {
  id: string;
  model_definition_id: string;
  dataset_version_id: string;
  config: Record<string, any>;
  requested_by: string;
  created_at: string;
  started_at?: string;
  finished_at?: string;
  status: TrainingJobStatus;
  hardware: string;
  precision: string;
  distributed_config?: Record<string, any>;
  output_checkpoint?: string;
  metrics: {
    train_loss?: number[];
    validation_loss?: number[];
    learning_rate?: number[];
    epoch?: number[];
    step?: number[];
    [key: string]: any;
  };
  logs_uri?: string;
  error?: string;
  trace_id: string;
}

export interface EvaluationJob {
  id: string;
  model_version_id: string;
  dataset_version_id: string;
  task: string;
  metrics: Record<string, number>;
  result: Record<string, any>;
  artifacts: string[];
  status: 'RUNNING' | 'COMPLETED' | 'FAILED';
  created_at: string;
  finished_at?: string;
}

export interface Deployment {
  id: string;
  model_version_id: string;
  deployment_target: DeploymentTarget;
  runtime: string;
  device: string;
  precision: string;
  status: 'PENDING' | 'ACTIVE' | 'STOPPED' | 'FAILED';
  endpoint?: string;
  created_at: string;
}

export interface ApprovalRequest {
  id: string;
  action: string;
  risk_level: ActionRiskLevel;
  requested_by: string;
  requested_via: string;
  tool_name: string;
  arguments_hash: string;
  summary: string;
  created_at: string;
  expires_at: string;
  status: ApprovalStatus;
  approved_by?: string;
  decision_time?: string;
  trace_id: string;
}

export interface AICommand {
  id: string;
  user_input: string;
  interpreted_plan: string;
  tools_called: Array<{
    tool_name: string;
    arguments: Record<string, any>;
    result: any;
    execution_time_ms: number;
  }>;
  approval_requests: ApprovalRequest[];
  final_response: string;
  sources: string[];
  confidence?: number;
  trace_id: string;
  created_at: string;
}

export interface LLMProvider {
  id: string;
  name: string;
  type: 'qwen' | 'openai' | 'openai_compatible' | 'local';
  endpoint?: string;
  model: string;
  context_length: number;
  temperature: number;
  max_tokens: number;
  tool_support: boolean;
  configured: boolean;
}

export interface ToolDefinition {
  name: string;
  description: string;
  category: string;
  risk_level: ActionRiskLevel;
  required_role: string;
  approval_required: boolean;
  rate_limit?: number;
  timeout_ms: number;
  parameters: Record<string, any>;
}

export interface InferenceResult {
  task: string;
  model_version_id: string;
  output: any;
  confidence?: number;
  uncertainty?: number;
  provenance: {
    input_data: string[];
    preprocessing: string[];
    postprocessing: string[];
  };
  execution_time_ms: number;
  trace_id: string;
}
