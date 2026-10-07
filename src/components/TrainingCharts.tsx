import { useMemo } from 'react';
import type { TrainingJob } from '../types/ai';

interface TrainingChartsProps {
  job: TrainingJob;
}

export function TrainingCharts({ job }: TrainingChartsProps) {
  const metrics = job.metrics;

  // Prepare chart data
  const chartData = useMemo(() => {
    const epochs = metrics.epoch || [];
    const trainLoss = metrics.train_loss || [];
    const valLoss = metrics.validation_loss || [];
    const learningRate = metrics.learning_rate || [];

    return {
      epochs,
      trainLoss,
      valLoss,
      learningRate,
    };
  }, [metrics]);

  if (chartData.epochs.length === 0) {
    return (
      <div className="p-8 rounded-lg border border-earth-600/50 bg-earth-800/30 text-center">
        <p className="text-sm text-earth-400">No training data available yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Loss Chart */}
      <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
        <h3 className="text-sm font-semibold text-white mb-4">Loss Curves</h3>
        <div className="h-64 relative">
          <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
            {/* Grid lines */}
            {[0, 1, 2, 3, 4].map(i => (
              <line
                key={i}
                x1="0"
                y1={i * 50}
                x2="400"
                y2={i * 50}
                stroke="rgba(255,255,255,0.05)"
                strokeWidth="1"
              />
            ))}

            {/* Train Loss Line */}
            {chartData.trainLoss.length > 1 && (
              <polyline
                points={chartData.trainLoss
                  .map((loss, i) => {
                    const x = (i / (chartData.trainLoss.length - 1)) * 400;
                    const maxLoss = Math.max(...chartData.trainLoss, ...chartData.valLoss);
                    const y = 200 - (loss / maxLoss) * 200;
                    return `${x},${y}`;
                  })
                  .join(' ')}
                fill="none"
                stroke="#00d4ff"
                strokeWidth="2"
              />
            )}

            {/* Validation Loss Line */}
            {chartData.valLoss.length > 1 && (
              <polyline
                points={chartData.valLoss
                  .map((loss, i) => {
                    const x = (i / (chartData.valLoss.length - 1)) * 400;
                    const maxLoss = Math.max(...chartData.trainLoss, ...chartData.valLoss);
                    const y = 200 - (loss / maxLoss) * 200;
                    return `${x},${y}`;
                  })
                  .join(' ')}
                fill="none"
                stroke="#a855f7"
                strokeWidth="2"
              />
            )}
          </svg>

          {/* Legend */}
          <div className="absolute top-0 right-0 flex gap-4 text-xs">
            <div className="flex items-center gap-1">
              <div className="w-3 h-0.5 bg-neon-blue" />
              <span className="text-earth-400">Train Loss</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-0.5 bg-neon-purple" />
              <span className="text-earth-400">Validation Loss</span>
            </div>
          </div>
        </div>

        {/* Current Values */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="p-3 rounded bg-earth-700/50">
            <div className="text-[10px] text-earth-400 mb-1">Current Train Loss</div>
            <div className="text-lg font-bold text-neon-blue">
              {chartData.trainLoss[chartData.trainLoss.length - 1]?.toFixed(4) || 'N/A'}
            </div>
          </div>
          <div className="p-3 rounded bg-earth-700/50">
            <div className="text-[10px] text-earth-400 mb-1">Current Val Loss</div>
            <div className="text-lg font-bold text-neon-purple">
              {chartData.valLoss[chartData.valLoss.length - 1]?.toFixed(4) || 'N/A'}
            </div>
          </div>
        </div>
      </div>

      {/* Learning Rate Chart */}
      {chartData.learningRate.length > 0 && (
        <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
          <h3 className="text-sm font-semibold text-white mb-4">Learning Rate Schedule</h3>
          <div className="h-32 relative">
            <svg className="w-full h-full" viewBox="0 0 400 100" preserveAspectRatio="none">
              {/* Grid lines */}
              {[0, 1, 2].map(i => (
                <line
                  key={i}
                  x1="0"
                  y1={i * 50}
                  x2="400"
                  y2={i * 50}
                  stroke="rgba(255,255,255,0.05)"
                  strokeWidth="1"
                />
              ))}

              {/* Learning Rate Line */}
              {chartData.learningRate.length > 1 && (
                <polyline
                  points={chartData.learningRate
                    .map((lr, i) => {
                      const x = (i / (chartData.learningRate.length - 1)) * 400;
                      const maxLR = Math.max(...chartData.learningRate);
                      const y = 100 - (lr / maxLR) * 100;
                      return `${x},${y}`;
                    })
                    .join(' ')}
                  fill="none"
                  stroke="#00ff88"
                  strokeWidth="2"
                />
              )}
            </svg>
          </div>
          <div className="mt-3 p-3 rounded bg-earth-700/50">
            <div className="text-[10px] text-earth-400 mb-1">Current Learning Rate</div>
            <div className="text-lg font-bold text-neon-green">
              {chartData.learningRate[chartData.learningRate.length - 1]?.toExponential(2) || 'N/A'}
            </div>
          </div>
        </div>
      )}

      {/* Additional Metrics */}
      {metrics.accuracy && metrics.accuracy.length > 0 && (
        <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
          <h3 className="text-sm font-semibold text-white mb-4">Accuracy</h3>
          <div className="h-32 relative">
            <svg className="w-full h-full" viewBox="0 0 400 100" preserveAspectRatio="none">
              {/* Grid lines */}
              {[0, 1, 2].map(i => (
                <line
                  key={i}
                  x1="0"
                  y1={i * 50}
                  x2="400"
                  y2={i * 50}
                  stroke="rgba(255,255,255,0.05)"
                  strokeWidth="1"
                />
              ))}

              {/* Accuracy Line */}
              {metrics.accuracy && metrics.accuracy.length > 1 && (
                <polyline
                  points={metrics.accuracy
                    .map((acc: number, i: number) => {
                      const x = (i / (metrics.accuracy!.length - 1)) * 400;
                      const y = 100 - acc * 100;
                      return `${x},${y}`;
                    })
                    .join(' ')}
                  fill="none"
                  stroke="#ffd700"
                  strokeWidth="2"
                />
              )}
            </svg>
          </div>
          <div className="mt-3 p-3 rounded bg-earth-700/50">
            <div className="text-[10px] text-earth-400 mb-1">Current Accuracy</div>
            <div className="text-lg font-bold text-neon-yellow">
              {((metrics.accuracy[metrics.accuracy.length - 1] || 0) * 100).toFixed(1)}%
            </div>
          </div>
        </div>
      )}

      {/* Training Summary */}
      <div className="p-4 rounded-lg border border-earth-600/50 bg-earth-800/50">
        <h3 className="text-sm font-semibold text-white mb-4">Training Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div className="text-[10px] text-earth-400 mb-1">Epochs Completed</div>
            <div className="text-lg font-bold text-white">
              {chartData.epochs.length} / {job.config.epochs}
            </div>
          </div>
          <div>
            <div className="text-[10px] text-earth-400 mb-1">Best Val Loss</div>
            <div className="text-lg font-bold text-neon-green">
              {chartData.valLoss.length > 0
                ? Math.min(...chartData.valLoss).toFixed(4)
                : 'N/A'}
            </div>
          </div>
          <div>
            <div className="text-[10px] text-earth-400 mb-1">Hardware</div>
            <div className="text-lg font-bold text-white">{job.hardware}</div>
          </div>
          <div>
            <div className="text-[10px] text-earth-400 mb-1">Status</div>
            <div className={`text-lg font-bold ${
              job.status === 'COMPLETED' ? 'text-neon-green' :
              job.status === 'RUNNING' ? 'text-neon-blue' :
              job.status === 'FAILED' ? 'text-neon-red' :
              'text-earth-400'
            }`}>
              {job.status}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
