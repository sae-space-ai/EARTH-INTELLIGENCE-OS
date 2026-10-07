import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain, Database, Cpu, TrendingUp, FlaskConical, Rocket,
  History, Shield, Play, Pause, Square, Eye, CheckCircle,
  XCircle, Clock, AlertCircle, BarChart3, GitBranch,
  Layers, Zap, Target, Award, Activity, FileText
} from 'lucide-react';
import {
  demoModelDefinitions,
  demoModelVersions,
  demoDatasets,
  demoTrainingJobs,
  demoEvaluations,
  demoDeployments,
  demoCommands,
  demoApprovals,
} from '../data/ai-demo';
import type { ModelDefinition, TrainingJob, ModelVersion } from '../types/ai';

type AILabTab = 'models' | 'datasets' | 'training' | 'experiments' | 'evaluation' | 'deployments' | 'commands' | 'approvals';

export function AILabPage() {
  const [activeTab, setActiveTab] = useState<AILabTab>('models');
  const [selectedModel, setSelectedModel] = useState<ModelDefinition | null>(null);
  const [selectedTrainingJob, setSelectedTrainingJob] = useState<TrainingJob | null>(null);

  const tabs = [
    { id: 'models', label: 'Models', icon: <Brain size={16} />, count: demoModelDefinitions.length },
    { id: 'datasets', label: 'Datasets', icon: <Database size={16} />, count: demoDatasets.length },
    { id: 'training', label: 'Training', icon: <Cpu size={16} />, count: demoTrainingJobs.length },
    { id: 'evaluation', label: 'Evaluation', icon: <FlaskConical size={16} />, count: demoEvaluations.length },
    { id: 'deployments', label: 'Deployments', icon: <Rocket size={16} />, count: demoDeployments.length },
    { id: 'commands', label: 'Commands', icon: <History size={16} />, count: demoCommands.length },
    { id: 'approvals', label: 'Approvals', icon: <Shield size={16} />, count: demoApprovals.filter(a => a.status === 'PENDING').length },
  ];

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-earth-600/50 bg-earth-800/50 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Brain size={20} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">AI Control Center</h1>
              <p className="text-xs text-earth-400">Model Training • Evaluation • Deployment • Command</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="px-3 py-1.5 rounded-lg bg-earth-700/50 border border-earth-600/50">
              <div className="text-[10px] text-earth-400">Active Jobs</div>
              <div className="text-sm font-bold text-white">{demoTrainingJobs.filter(j => j.status === 'RUNNING').length}</div>
            </div>
            <div className="px-3 py-1.5 rounded-lg bg-earth-700/50 border border-earth-600/50">
              <div className="text-[10px] text-earth-400">Deployed Models</div>
              <div className="text-sm font-bold text-white">{demoDeployments.filter(d => d.status === 'ACTIVE').length}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-earth-600/50 bg-earth-800/30 px-6">
        <div className="flex gap-1">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as AILabTab)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === tab.id
                  ? 'text-neon-blue border-neon-blue'
                  : 'text-earth-400 border-transparent hover:text-white'
              }`}
            >
              {tab.icon}
              {tab.label}
              {tab.count > 0 && (
                <span className="px-1.5 py-0.5 text-[10px] rounded-full bg-earth-700 text-earth-300">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="h-full overflow-y-auto p-6"
          >
            {activeTab === 'models' && (
              <ModelsView
                models={demoModelDefinitions}
                versions={demoModelVersions}
                selectedModel={selectedModel}
                onSelectModel={setSelectedModel}
              />
            )}
            {activeTab === 'datasets' && <DatasetsView datasets={demoDatasets} />}
            {activeTab === 'training' && (
              <TrainingView
                jobs={demoTrainingJobs}
                selectedJob={selectedTrainingJob}
                onSelectJob={setSelectedTrainingJob}
              />
            )}
            {activeTab === 'evaluation' && <EvaluationView evaluations={demoEvaluations} />}
            {activeTab === 'deployments' && <DeploymentsView deployments={demoDeployments} />}
            {activeTab === 'commands' && <CommandsView commands={demoCommands} />}
            {activeTab === 'approvals' && <ApprovalsView approvals={demoApprovals} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

// Models View
function ModelsView({
  models,
  versions,
  selectedModel,
  onSelectModel,
}: {
  models: ModelDefinition[];
  versions: ModelVersion[];
  selectedModel: ModelDefinition | null;
  onSelectModel: (model: ModelDefinition | null) => void;
}) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Model List */}
      <div className="lg:col-span-2 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Model Catalog</h2>
          <button className="px-3 py-1.5 text-xs font-medium rounded-lg bg-neon-blue/20 text-neon-blue border border-neon-blue/30 hover:bg-neon-blue/30 transition-colors">
            + Register Model
          </button>
        </div>
        <div className="space-y-3">
          {models.map(model => (
            <motion.div
              key={model.id}
              whileHover={{ scale: 1.01 }}
              onClick={() => onSelectModel(model)}
              className={`p-4 rounded-lg border cursor-pointer transition-all ${
                selectedModel?.id === model.id
                  ? 'bg-neon-blue/10 border-neon-blue/50'
                  : 'bg-earth-800/50 border-earth-600/50 hover:border-earth-500'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-sm font-semibold text-white">{model.name}</h3>
                    <span className="px-2 py-0.5 text-[10px] rounded-full bg-purple-500/20 text-purple-400 border border-purple-500/30">
                      {model.family.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <p className="text-xs text-earth-400">{model.architecture}</p>
                </div>
                <div className="text-right">
                  <div className="text-xs text-earth-400">Parameters</div>
                  <div className="text-sm font-bold text-white">
                    {model.parameter_count ? `${(model.parameter_count / 1_000_000).toFixed(1)}M` : 'N/A'}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4 text-xs text-earth-400">
                <div className="flex items-center gap-1">
                  <Layers size={12} />
                  <span>{model.modalities.join(', ')}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Target size={12} />
                  <span>{model.task}</span>
                </div>
                {model.edge_compatible && (
                  <div className="flex items-center gap-1 text-neon-green">
                    <Zap size={12} />
                    <span>Edge</span>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Model Details */}
      <div className="lg:col-span-1">
        {selectedModel ? (
          <div className="sticky top-6 space-y-4">
            <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
              <h3 className="text-sm font-semibold text-white mb-3">{selectedModel.name}</h3>
              <div className="space-y-3 text-xs">
                <div>
                  <div className="text-earth-400 mb-1">Task</div>
                  <div className="text-white">{selectedModel.task}</div>
                </div>
                <div>
                  <div className="text-earth-400 mb-1">Modalities</div>
                  <div className="flex flex-wrap gap-1">
                    {selectedModel.modalities.map(mod => (
                      <span key={mod} className="px-2 py-0.5 rounded bg-earth-700 text-earth-300">
                        {mod}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="text-earth-400 mb-1">Capabilities</div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      {selectedModel.training_supported ? (
                        <CheckCircle size={12} className="text-neon-green" />
                      ) : (
                        <XCircle size={12} className="text-neon-red" />
                      )}
                      <span className="text-white">Training</span>
                    </div>
                    <div className="flex items-center gap-2">
                      {selectedModel.inference_supported ? (
                        <CheckCircle size={12} className="text-neon-green" />
                      ) : (
                        <XCircle size={12} className="text-neon-red" />
                      )}
                      <span className="text-white">Inference</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Versions */}
            <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
              <h4 className="text-xs font-semibold text-earth-400 uppercase mb-3">Versions</h4>
              <div className="space-y-2">
                {versions
                  .filter(v => v.model_definition_id === selectedModel.id)
                  .map(version => (
                    <div key={version.id} className="p-2 rounded bg-earth-700/50">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-medium text-white">{version.semantic_version}</span>
                        <span className={`px-1.5 py-0.5 text-[9px] rounded ${
                          version.status === 'DEPLOYED' ? 'bg-neon-green/20 text-neon-green' :
                          version.status === 'VALIDATED' ? 'bg-neon-blue/20 text-neon-blue' :
                          'bg-earth-600 text-earth-400'
                        }`}>
                          {version.status}
                        </span>
                      </div>
                      <div className="text-[10px] text-earth-400">
                        {Object.entries(version.metrics).slice(0, 3).map(([key, value]) => (
                          <span key={key} className="mr-2">
                            {key}: {(value as number).toFixed(3)}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="p-8 rounded-lg border border-earth-600/50 bg-earth-800/30 text-center">
            <Brain size={48} className="mx-auto mb-3 text-earth-600" />
            <p className="text-sm text-earth-400">Select a model to view details</p>
          </div>
        )}
      </div>
    </div>
  );
}

// Datasets View
function DatasetsView({ datasets }: { datasets: typeof demoDatasets }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Dataset Registry</h2>
        <button className="px-3 py-1.5 text-xs font-medium rounded-lg bg-neon-blue/20 text-neon-blue border border-neon-blue/30 hover:bg-neon-blue/30 transition-colors">
          + Create Dataset
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {datasets.map(dataset => (
          <motion.div
            key={dataset.id}
            whileHover={{ scale: 1.01 }}
            className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50"
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-white mb-1">{dataset.name}</h3>
                <p className="text-xs text-earth-400">{dataset.description}</p>
              </div>
              <span className="px-2 py-0.5 text-[10px] rounded-full bg-neon-green/20 text-neon-green border border-neon-green/30">
                {dataset.access_policy}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <div className="text-earth-400 mb-1">Samples</div>
                <div className="text-white font-medium">{dataset.sample_count.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Assets</div>
                <div className="text-white font-medium">{dataset.asset_count.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Modalities</div>
                <div className="flex flex-wrap gap-1">
                  {dataset.modalities.map(mod => (
                    <span key={mod} className="px-1.5 py-0.5 rounded bg-earth-700 text-earth-300 text-[10px]">
                      {mod}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Providers</div>
                <div className="text-white text-[11px]">{dataset.providers.join(', ')}</div>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-earth-600/50">
              <div className="text-[10px] text-earth-400">
                <span className="font-medium">License:</span> {dataset.license}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

// Training View
function TrainingView({
  jobs,
  selectedJob,
  onSelectJob,
}: {
  jobs: TrainingJob[];
  selectedJob: TrainingJob | null;
  onSelectJob: (job: TrainingJob | null) => void;
}) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Job List */}
      <div className="lg:col-span-2 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Training Jobs</h2>
          <button className="px-3 py-1.5 text-xs font-medium rounded-lg bg-neon-blue/20 text-neon-blue border border-neon-blue/30 hover:bg-neon-blue/30 transition-colors">
            + New Training Job
          </button>
        </div>
        <div className="space-y-3">
          {jobs.map(job => (
            <motion.div
              key={job.id}
              whileHover={{ scale: 1.01 }}
              onClick={() => onSelectJob(job)}
              className={`p-4 rounded-lg border cursor-pointer transition-all ${
                selectedJob?.id === job.id
                  ? 'bg-neon-blue/10 border-neon-blue/50'
                  : 'bg-earth-800/50 border-earth-600/50 hover:border-earth-500'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-sm font-semibold text-white">{job.id}</h3>
                    <StatusBadge status={job.status} />
                  </div>
                  <p className="text-xs text-earth-400">
                    {job.model_definition_id} • {job.dataset_version_id}
                  </p>
                </div>
                <div className="text-right text-xs">
                  <div className="text-earth-400">Hardware</div>
                  <div className="text-white font-medium">{job.hardware}</div>
                </div>
              </div>
              {job.metrics.train_loss && job.metrics.train_loss.length > 0 && (
                <div className="mt-3">
                  <div className="text-[10px] text-earth-400 mb-1">Training Progress</div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-2 rounded-full bg-earth-700 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-neon-blue to-neon-green transition-all"
                        style={{
                          width: `${(job.metrics.epoch?.length || 0) / (job.config.epochs || 10) * 100}%`
                        }}
                      />
                    </div>
                    <span className="text-xs text-white font-medium">
                      {job.metrics.epoch?.length || 0}/{job.config.epochs}
                    </span>
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Job Details */}
      <div className="lg:col-span-1">
        {selectedJob ? (
          <div className="sticky top-6 space-y-4">
            {/* Metrics */}
            <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
              <h3 className="text-sm font-semibold text-white mb-3">Training Metrics</h3>
              {selectedJob.metrics.train_loss && (
                <div className="space-y-3">
                  <div>
                    <div className="text-[10px] text-earth-400 mb-1">Train Loss</div>
                    <div className="text-lg font-bold text-white">
                      {selectedJob.metrics.train_loss[selectedJob.metrics.train_loss.length - 1].toFixed(4)}
                    </div>
                  </div>
                  {selectedJob.metrics.validation_loss && (
                    <div>
                      <div className="text-[10px] text-earth-400 mb-1">Validation Loss</div>
                      <div className="text-lg font-bold text-white">
                        {selectedJob.metrics.validation_loss[selectedJob.metrics.validation_loss.length - 1].toFixed(4)}
                      </div>
                    </div>
                  )}
                  {selectedJob.metrics.accuracy && (
                    <div>
                      <div className="text-[10px] text-earth-400 mb-1">Accuracy</div>
                      <div className="text-lg font-bold text-neon-green">
                        {(selectedJob.metrics.accuracy[selectedJob.metrics.accuracy.length - 1] * 100).toFixed(1)}%
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Config */}
            <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
              <h4 className="text-xs font-semibold text-earth-400 uppercase mb-3">Configuration</h4>
              <div className="space-y-2 text-xs">
                {Object.entries(selectedJob.config).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-earth-400">{key}</span>
                    <span className="text-white font-medium">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Controls */}
            {selectedJob.status === 'RUNNING' && (
              <div className="flex gap-2">
                <button className="flex-1 px-3 py-2 text-xs font-medium rounded-lg bg-neon-yellow/20 text-neon-yellow border border-neon-yellow/30 hover:bg-neon-yellow/30 transition-colors flex items-center justify-center gap-1">
                  <Pause size={12} />
                  Pause
                </button>
                <button className="flex-1 px-3 py-2 text-xs font-medium rounded-lg bg-neon-red/20 text-neon-red border border-neon-red/30 hover:bg-neon-red/30 transition-colors flex items-center justify-center gap-1">
                  <Square size={12} />
                  Cancel
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="p-8 rounded-lg border border-earth-600/50 bg-earth-800/30 text-center">
            <Cpu size={48} className="mx-auto mb-3 text-earth-600" />
            <p className="text-sm text-earth-400">Select a training job to view details</p>
          </div>
        )}
      </div>
    </div>
  );
}

// Evaluation View
function EvaluationView({ evaluations }: { evaluations: typeof demoEvaluations }) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-white">Evaluation Results</h2>
      <div className="space-y-3">
        {evaluations.map(eval_ => (
          <div key={eval_.id} className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-white mb-1">{eval_.id}</h3>
                <p className="text-xs text-earth-400">
                  Model: {eval_.model_version_id} • Dataset: {eval_.dataset_version_id}
                </p>
              </div>
              <StatusBadge status={eval_.status} />
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(eval_.metrics).map(([key, value]) => (
                <div key={key} className="p-2 rounded bg-earth-700/50">
                  <div className="text-[10px] text-earth-400 mb-1">{key.replace(/_/g, ' ')}</div>
                  <div className="text-sm font-bold text-white">{(value as number).toFixed(3)}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Deployments View
function DeploymentsView({ deployments }: { deployments: typeof demoDeployments }) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-white">Model Deployments</h2>
      <div className="space-y-3">
        {deployments.map(deployment => (
          <div key={deployment.id} className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-white mb-1">{deployment.id}</h3>
                <p className="text-xs text-earth-400">Model: {deployment.model_version_id}</p>
              </div>
              <StatusBadge status={deployment.status} />
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div>
                <div className="text-earth-400 mb-1">Target</div>
                <div className="text-white font-medium">{deployment.deployment_target.replace(/_/g, ' ')}</div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Runtime</div>
                <div className="text-white font-medium">{deployment.runtime}</div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Device</div>
                <div className="text-white font-medium">{deployment.device}</div>
              </div>
              <div>
                <div className="text-earth-400 mb-1">Precision</div>
                <div className="text-white font-medium">{deployment.precision}</div>
              </div>
            </div>
            {deployment.endpoint && (
              <div className="mt-3 pt-3 border-t border-earth-600/50">
                <div className="text-[10px] text-earth-400 mb-1">Endpoint</div>
                <code className="text-xs text-neon-blue">{deployment.endpoint}</code>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// Commands View
function CommandsView({ commands }: { commands: typeof demoCommands }) {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-white">Command History</h2>
      <div className="space-y-3">
        {commands.map(command => (
          <div key={command.id} className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
            <div className="mb-3">
              <div className="text-xs text-earth-400 mb-1">User Command</div>
              <div className="text-sm text-white font-medium">{command.user_input}</div>
            </div>
            <div className="mb-3">
              <div className="text-xs text-earth-400 mb-1">Interpreted Plan</div>
              <div className="text-xs text-earth-300">{command.interpreted_plan}</div>
            </div>
            <div className="mb-3">
              <div className="text-xs text-earth-400 mb-2">Tools Called ({command.tools_called.length})</div>
              <div className="space-y-2">
                {command.tools_called.map((tool, idx) => (
                  <div key={idx} className="p-2 rounded bg-earth-700/50">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-white">{tool.tool_name}</span>
                      <span className="text-[10px] text-earth-400">{tool.execution_time_ms}ms</span>
                    </div>
                    <div className="text-[10px] text-earth-400 font-mono">
                      {JSON.stringify(tool.arguments).substring(0, 100)}...
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="pt-3 border-t border-earth-600/50">
              <div className="text-xs text-earth-400 mb-1">Response</div>
              <div className="text-sm text-white">{command.final_response}</div>
              {command.confidence && (
                <div className="mt-2 text-[10px] text-earth-400">
                  Confidence: {(command.confidence * 100).toFixed(0)}%
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Approvals View
function ApprovalsView({ approvals }: { approvals: typeof demoApprovals }) {
  const pendingApprovals = approvals.filter(a => a.status === 'PENDING');
  const decidedApprovals = approvals.filter(a => a.status !== 'PENDING');

  return (
    <div className="space-y-6">
      {/* Pending */}
      <div>
        <h2 className="text-lg font-semibold text-white mb-3">Pending Approvals</h2>
        {pendingApprovals.length === 0 ? (
          <div className="p-8 rounded-lg border border-earth-600/50 bg-earth-800/30 text-center">
            <CheckCircle size={48} className="mx-auto mb-3 text-neon-green" />
            <p className="text-sm text-earth-400">No pending approvals</p>
          </div>
        ) : (
          <div className="space-y-3">
            {pendingApprovals.map(approval => (
              <div key={approval.id} className="p-4 rounded-lg border border-neon-yellow/50 bg-neon-yellow/5">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <AlertCircle size={16} className="text-neon-yellow" />
                      <h3 className="text-sm font-semibold text-white">{approval.action}</h3>
                    </div>
                    <p className="text-xs text-earth-300">{approval.summary}</p>
                  </div>
                  <RiskBadge risk={approval.risk_level} />
                </div>
                <div className="text-xs text-earth-400 mb-3">
                  Requested by {approval.requested_by} via {approval.requested_via}
                </div>
                <div className="flex gap-2">
                  <button className="flex-1 px-3 py-2 text-xs font-medium rounded-lg bg-neon-green/20 text-neon-green border border-neon-green/30 hover:bg-neon-green/30 transition-colors">
                    Approve
                  </button>
                  <button className="flex-1 px-3 py-2 text-xs font-medium rounded-lg bg-neon-red/20 text-neon-red border border-neon-red/30 hover:bg-neon-red/30 transition-colors">
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Decided */}
      {decidedApprovals.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-white mb-3">Decision History</h2>
          <div className="space-y-3">
            {decidedApprovals.map(approval => (
              <div key={approval.id} className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="text-sm font-semibold text-white mb-1">{approval.action}</h3>
                    <p className="text-xs text-earth-400">{approval.summary}</p>
                  </div>
                  <StatusBadge status={approval.status} />
                </div>
                {approval.approved_by && (
                  <div className="text-xs text-earth-400 mt-2">
                    {approval.status === 'APPROVED' ? '✓' : '✗'} {approval.approved_by} •{' '}
                    {new Date(approval.decision_time!).toLocaleString()}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Helper Components
function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    RUNNING: 'bg-neon-blue/20 text-neon-blue border-neon-blue/30',
    COMPLETED: 'bg-neon-green/20 text-neon-green border-neon-green/30',
    FAILED: 'bg-neon-red/20 text-neon-red border-neon-red/30',
    QUEUED: 'bg-earth-600/50 text-earth-300 border-earth-500/50',
    VALIDATED: 'bg-neon-blue/20 text-neon-blue border-neon-blue/30',
    DEPLOYED: 'bg-neon-green/20 text-neon-green border-neon-green/30',
    ACTIVE: 'bg-neon-green/20 text-neon-green border-neon-green/30',
    PENDING: 'bg-neon-yellow/20 text-neon-yellow border-neon-yellow/30',
    APPROVED: 'bg-neon-green/20 text-neon-green border-neon-green/30',
    REJECTED: 'bg-neon-red/20 text-neon-red border-neon-red/30',
  };

  return (
    <span className={`px-2 py-0.5 text-[10px] rounded-full border ${colors[status] || colors.QUEUED}`}>
      {status}
    </span>
  );
}

function RiskBadge({ risk }: { risk: string }) {
  const colors: Record<string, string> = {
    READ_ONLY: 'bg-neon-green/20 text-neon-green border-neon-green/30',
    UI_ACTION: 'bg-neon-blue/20 text-neon-blue border-neon-blue/30',
    DATA_MUTATION: 'bg-neon-yellow/20 text-neon-yellow border-neon-yellow/30',
    COMPUTE_JOB: 'bg-neon-orange/20 text-neon-orange border-neon-orange/30',
    MODEL_DEPLOYMENT: 'bg-neon-red/20 text-neon-red border-neon-red/30',
    MISSION_PROPOSAL: 'bg-neon-red/20 text-neon-red border-neon-red/30',
    SPACECRAFT_COMMAND: 'bg-neon-red/30 text-neon-red border-neon-red/50',
  };

  return (
    <span className={`px-2 py-0.5 text-[10px] rounded-full border ${colors[risk] || colors.READ_ONLY}`}>
      {risk.replace(/_/g, ' ')}
    </span>
  );
}
