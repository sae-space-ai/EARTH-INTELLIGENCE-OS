# AI Control Center — Earth Intelligence OS

## Overview

The AI Control Center provides a comprehensive interface for managing the complete AI/ML lifecycle in Earth Intelligence OS, from model training and evaluation to deployment and intelligent command execution.

## Architecture

```
AI CONTROL CENTER
│
├── AI TRAINING PLANE
│   ├── Model Catalog
│   ├── Model Registry
│   ├── Dataset Registry
│   ├── Training Jobs
│   ├── Experiments
│   ├── Evaluation
│   └── Deployments
│
├── AI COMMAND PLANE
│   ├── LLM Providers
│   ├── Tool Catalog
│   ├── AI Orchestrator
│   ├── Policy Engine
│   └── Approval Queue
│
└── SHARED INFRASTRUCTURE
    ├── Provenance Tracking
    ├── Audit Logging
    ├── Security Controls
    └── Observability
```

## Features

### 1. Model Management

#### Model Catalog
- **21 Model Families**: From multimodal foundation models to specialized encoders
- **Architecture Registry**: Document model architectures, input/output schemas
- **Capability Tracking**: Training support, inference support, edge compatibility

#### Model Families
- `MULTIMODAL_FOUNDATION_MODEL` — Unified representation across modalities
- `LIDAR_ENCODER` — PointNet++ inspired point cloud processing
- `SAR_ENCODER` — Residual U-Net with transformer fusion
- `OPTICAL_ENCODER` — CNN/ViT for optical imagery
- `HYPERSPECTRAL_ENCODER` — Spectral-aware encoders
- `CHANGE_DETECTION` — Temporal change analysis
- `ANOMALY_DETECTION` — Unsupervised anomaly detection
- `SEMANTIC_SEGMENTATION` — Pixel-level classification
- `OBJECT_DETECTION` — Bounding box prediction
- `LAND_COVER_CLASSIFICATION` — Land use/land cover mapping
- `FIRE_DETECTION` — Active fire identification
- `WEATHER_MODEL` — Meteorological prediction
- `TEMPORAL_FORECAST_MODEL` — Time series forecasting
- `WORLD_MODEL` — Earth state prediction
- `EMBEDDING_MODEL` — Vector representation
- `RERANKER` — Result reordering
- `LLM` — Large language models
- `VISION_LANGUAGE_MODEL` — Multimodal reasoning
- `SMALL_EDGE_MODEL` — Lightweight edge deployment
- `OTHER` — Custom architectures

#### Model Registry
- **Version Control**: Semantic versioning with git commit tracking
- **Checkpoint Management**: SHA-256 verified model artifacts
- **Lifecycle States**: REGISTERED → TRAINING → VALIDATING → VALIDATED → PROMOTED → DEPLOYED → RETIRED
- **Metrics Tracking**: Task-specific metrics (accuracy, IoU, F1, etc.)

### 2. Dataset Management

#### Dataset Registry
- **Immutable Versions**: Each dataset version is immutable and checksummed
- **Multi-Modal Support**: Optical, SAR, LiDAR, hyperspectral, weather
- **Provenance Tracking**: Source providers, licenses, access policies
- **Schema Definition**: Input/output schemas with normalization parameters

#### Dataset Builder
- **Provider Integration**: Copernicus CDSE, ESA, EUMETSAT, Destination Earth
- **Spatial/Temporal Filtering**: AOI and time range selection
- **Manifest Generation**: JSON manifests with asset references
- **License Compliance**: Automatic license verification and access policy enforcement

### 3. Training Infrastructure

#### Training Jobs
- **PyTorch 2.x Backend**: Full PyTorch ecosystem support
- **Hardware Support**: CPU, CUDA, multi-GPU (DDP)
- **Precision Support**: FP32, FP16, BF16
- **Optimization**: AdamW, cosine scheduling, gradient accumulation
- **Checkpointing**: Automatic checkpointing with resume capability
- **Experiment Tracking**: Optional WandB integration

#### Training Executors
- **LocalTrainingExecutor**: Local CPU/GPU training
- **KubernetesTrainingExecutor**: (Future) K8s job orchestration
- **GPUClusterTrainingExecutor**: (Future) Multi-node training

#### Training Metrics
- **Generic Metrics**: train_loss, validation_loss, learning_rate, epoch, step
- **Task-Specific Metrics**: accuracy, F1, IoU, Chamfer distance, reconstruction loss
- **Real-Time Visualization**: Live loss curves and metric tracking

### 4. Evaluation & Promotion

#### Evaluation Jobs
- **Automated Evaluation**: Run evaluation on test datasets
- **Metric Computation**: Task-specific metrics with confidence intervals
- **Artifact Generation**: Confusion matrices, ROC curves, sample predictions

#### Promotion Gate
```
TRAINED → VALIDATION → EVALUATION → POLICY CHECK → APPROVAL → PROMOTED → DEPLOYED
```
- **Validation**: Automated validation checks
- **Evaluation**: Performance benchmarking
- **Policy Check**: Compliance with deployment policies
- **Human Approval**: Optional human-in-the-loop approval
- **Promotion**: Model version promotion to production

### 5. Deployment Management

#### Deployment Targets
- `GROUND_CPU` — CPU-based ground deployment
- `GROUND_GPU` — GPU-accelerated ground deployment
- `EDGE_SIMULATION` — Edge device simulation
- `FUTURE_SPACECRAFT` — (Future) Orbital deployment

#### Deployment Features
- **Runtime Selection**: PyTorch, TorchScript, ONNX
- **Device Configuration**: CPU, CUDA, edge devices
- **Precision Selection**: FP32, FP16, INT8 quantization
- **Endpoint Management**: REST API endpoint provisioning
- **Health Monitoring**: Deployment health checks and monitoring

### 6. AI Command Center

#### Natural Language Interface
- **Intent Recognition**: Parse user commands into structured plans
- **Tool Selection**: Automatically select appropriate tools
- **Execution Orchestration**: Coordinate multi-tool workflows
- **Result Synthesis**: Combine tool outputs into coherent responses

#### Canonical Tool Catalog
**Map Tools**
- `fly_to` — Navigate to location
- `reset_view` — Reset camera view
- `set_basemap` — Change basemap

**Live World Tools**
- `list_aircraft` — List live aircraft
- `track_aircraft` — Track specific aircraft
- `list_vessels` — List live vessels
- `list_satellites` — List satellites
- `next_satellite_pass` — Predict satellite pass
- `list_earthquakes` — List earthquakes
- `list_active_fires` — List active fires

**Space Tools**
- `search_european_imagery` — Search European Space Federation
- `list_missions` — List space missions
- `list_collections` — List data collections

**AI Training Tools**
- `list_model_definitions` — List available models
- `create_training_job` — Start training job
- `get_training_status` — Check training progress
- `evaluate_model` — Run model evaluation
- `deploy_model` — Deploy validated model

**System Tools**
- `get_provider_status` — Check provider health
- `get_system_health` — System health check

#### Security & Policy

##### Action Risk Levels
- `READ_ONLY` — Query operations (auto-approved)
- `UI_ACTION` — UI interactions (auto-approved)
- `DATA_MUTATION` — Data modifications (requires role)
- `COMPUTE_JOB` — Training/inference jobs (requires approval)
- `MODEL_DEPLOYMENT` — Model deployment (requires approval)
- `MISSION_PROPOSAL` — Mission proposals (requires approval)
- `SPACECRAFT_COMMAND` — Spacecraft commands (HARD BLOCK)

##### Policy Engine
- **Role-Based Access**: User roles and permissions
- **Resource Quotas**: GPU, CPU, memory, runtime limits
- **Approval Workflows**: Human-in-the-loop for critical actions
- **Audit Trail**: Complete action logging with trace IDs

##### Spacecraft Command Boundary
```
AI → Mission Proposal → Mission Planner → Digital Twin → Policy Engine → Human Approval → Flight Ops → Uplink
```
**CRITICAL**: Generative AI CANNOT directly command spacecraft. All commands must flow through the full authorization chain.

### 7. LLM Provider Integration

#### Provider-Agnostic Interface
- **Qwen**: Alibaba Qwen models
- **OpenAI**: GPT-4, GPT-3.5
- **OpenAI-Compatible**: Local servers (Ollama, vLLM, llama.cpp)
- **Future Providers**: Extensible provider interface

#### Configuration
```typescript
{
  provider: 'qwen' | 'openai' | 'openai_compatible' | 'local',
  endpoint: string,
  model: string,
  context_length: number,
  temperature: number,
  max_tokens: number,
  tool_support: boolean
}
```

#### Fallback Strategy
- **No LLM Required**: System fully functional without LLM
- **Manual Mode**: Direct tool invocation without natural language
- **Graceful Degradation**: Clear "LLM NOT CONFIGURED" messages

### 8. Observability & Audit

#### Audit Logging
- **Complete Trace**: Every AI action logged with trace ID
- **Tool Execution**: Tool calls, arguments, results, timing
- **Approval Records**: Approval requests and decisions
- **Model Provenance**: Training data, config, checkpoints, evaluations

#### Prompt Injection Defense
- **Data Separation**: Clear separation between instructions and data
- **Untrusted Content**: External data marked as untrusted
- **Policy Isolation**: Retrieved content cannot modify system policies

## Demo Mode

### Demo Training
- **Tiny Dataset**: 1000 synthetic samples
- **Tiny Model**: 50K parameter classifier
- **CPU Training**: 10 epochs, ~2 minutes
- **Real Metrics**: Actual loss curves and accuracy
- **Checkpoint Storage**: Real checkpoint with SHA-256

### Demo Workflow
1. Open AI Lab
2. Select "Demo Tiny Classifier"
3. Start training job
4. Watch real loss curves update
5. Training completes
6. Checkpoint stored
7. Evaluation runs
8. Model validated
9. Deploy to CPU
10. Run inference

## API Endpoints

### Model Management
```
GET    /api/v1/ai/models              # List model definitions
GET    /api/v1/ai/models/{id}         # Get model definition
GET    /api/v1/ai/model-versions      # List model versions
POST   /api/v1/ai/model-versions      # Register model version
```

### Dataset Management
```
GET    /api/v1/ai/datasets            # List datasets
POST   /api/v1/ai/datasets            # Create dataset
GET    /api/v1/ai/datasets/{id}       # Get dataset
```

### Training
```
GET    /api/v1/ai/training-jobs       # List training jobs
POST   /api/v1/ai/training-jobs       # Create training job
GET    /api/v1/ai/training-jobs/{id}  # Get training job
POST   /api/v1/ai/training-jobs/{id}/cancel  # Cancel job
```

### Evaluation
```
GET    /api/v1/ai/evaluations         # List evaluations
POST   /api/v1/ai/evaluations         # Create evaluation
GET    /api/v1/ai/evaluations/{id}    # Get evaluation
```

### Deployment
```
GET    /api/v1/ai/deployments         # List deployments
POST   /api/v1/ai/deployments         # Create deployment
GET    /api/v1/ai/deployments/{id}    # Get deployment
```

### Inference
```
POST   /api/v1/ai/inference           # Run inference
```

### Command
```
POST   /api/v1/ai/command             # Execute AI command
```

### Approvals
```
GET    /api/v1/ai/approvals           # List approvals
POST   /api/v1/ai/approvals/{id}/approve  # Approve request
POST   /api/v1/ai/approvals/{id}/reject   # Reject request
```

## Security

### Credential Management
- **No Hardcoded Secrets**: All credentials in environment variables
- **Server-Side Only**: LLM API keys never exposed to frontend
- **Vault Integration**: (Future) Secrets management

### Access Control
- **Role-Based**: User, ML Engineer, Admin roles
- **Resource Quotas**: Prevent resource exhaustion
- **Approval Workflows**: Human oversight for critical actions

### Prompt Injection Defense
- **Data/Instruction Separation**: Clear boundaries
- **Sandboxed Execution**: Tools run in isolated contexts
- **Audit Trail**: Complete action logging

## Performance

### Optimization
- **Lazy Loading**: Load data on demand
- **Caching**: Cache frequent queries
- **Pagination**: Large result sets paginated
- **Streaming**: Real-time training metrics

### Resource Management
- **GPU Detection**: Automatic CUDA detection
- **Memory Limits**: Configurable memory limits
- **Job Queuing**: Prevent resource contention

## Testing

### Unit Tests
- Model definitions validation
- Dataset immutability
- Training job lifecycle
- Evaluation metrics
- Promotion gate logic
- Policy enforcement

### Integration Tests
- Training job execution
- Checkpoint storage
- Evaluation pipeline
- Deployment workflow
- AI command execution

### Security Tests
- Prompt injection attempts
- Authorization bypass attempts
- Spacecraft command denial
- Credential exposure checks

## Future Enhancements

### Phase 1
- [ ] Kubernetes training executor
- [ ] Distributed training (DDP)
- [ ] Model quantization (INT8)
- [ ] ONNX export
- [ ] TorchScript export

### Phase 2
- [ ] Federated learning
- [ ] Active learning
- [ ] Continual learning
- [ ] Model compression

### Phase 3
- [ ] Orbital edge deployment
- [ ] On-board inference
- [ ] Autonomous observation planning
- [ ] Self-improving models

## Documentation

- [AI Lab User Guide](./AI_LAB_GUIDE.md)
- [AI Command User Guide](./AI_COMMAND_GUIDE.md)
- [Model Development Guide](./MODEL_DEVELOPMENT.md)
- [Security Policy](./SECURITY_POLICY.md)
- [API Reference](./API_REFERENCE.md)

## License

Proprietary — Earth Intelligence OS

## Support

For issues and questions:
- GitHub Issues: [Repository Issues]
- Documentation: [Docs Site]
- Email: support@earth-intelligence.os
