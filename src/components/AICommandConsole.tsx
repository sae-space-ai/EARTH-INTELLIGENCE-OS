import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Brain, Zap, CheckCircle, AlertCircle, Clock, Eye, ChevronDown, ChevronUp } from 'lucide-react';
import { demoTools, demoCommands } from '../data/ai-demo';
import type { AICommand, ToolDefinition } from '../types/ai';

export function AICommandConsole() {
  const [input, setInput] = useState('');
  const [commands, setCommands] = useState<AICommand[]>(demoCommands);
  const [isProcessing, setIsProcessing] = useState(false);
  const [expandedCommands, setExpandedCommands] = useState<Set<string>>(new Set());
  const [showTrace, setShowTrace] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    setIsProcessing(true);
    
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Create mock command response
    const newCommand: AICommand = {
      id: `cmd-${Date.now()}`,
      user_input: input,
      interpreted_plan: 'Processing your request...',
      tools_called: [
        {
          tool_name: 'list_aircraft',
          arguments: { bbox: [-10, 35, 10, 55], limit: 100 },
          result: { count: 23, aircraft: ['IBS2774', 'RYR105', 'EZY8821'] },
          execution_time_ms: 890,
        },
      ],
      approval_requests: [],
      final_response: `Found 23 aircraft in the specified region.`,
      sources: ['OpenSky Network'],
      confidence: 0.95,
      trace_id: `trace-${Date.now()}`,
      created_at: new Date().toISOString(),
    };

    setCommands([newCommand, ...commands]);
    setInput('');
    setIsProcessing(false);
    setExpandedCommands(new Set([newCommand.id]));
  };

  const toggleExpanded = (commandId: string) => {
    const newExpanded = new Set(expandedCommands);
    if (newExpanded.has(commandId)) {
      newExpanded.delete(commandId);
    } else {
      newExpanded.add(commandId);
    }
    setExpandedCommands(newExpanded);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-earth-600/50 bg-earth-800/50 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-blue to-neon-purple flex items-center justify-center">
              <Brain size={20} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">AI Command Center</h1>
              <p className="text-xs text-earth-400">Natural Language Interface • Tool Orchestration</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowTrace(!showTrace)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors ${
                showTrace
                  ? 'bg-neon-blue/20 text-neon-blue border-neon-blue/30'
                  : 'bg-earth-700/50 text-earth-400 border-earth-600/50'
              }`}
            >
              <Eye size={12} className="inline mr-1" />
              Show Trace
            </button>
          </div>
        </div>
      </div>

      {/* Command History */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <AnimatePresence>
          {commands.map(command => (
            <motion.div
              key={command.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="rounded-lg border border-earth-600/50 bg-earth-800/50 overflow-hidden"
            >
              {/* User Input */}
              <div className="p-4 border-b border-earth-600/50 bg-earth-700/30">
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-full bg-neon-blue/20 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-bold text-neon-blue">U</span>
                  </div>
                  <div className="flex-1">
                    <div className="text-xs text-earth-400 mb-1">You</div>
                    <div className="text-sm text-white">{command.user_input}</div>
                  </div>
                </div>
              </div>

              {/* AI Response */}
              <div className="p-4">
                <div className="flex items-start gap-3 mb-3">
                  <div className="w-8 h-8 rounded-full bg-neon-purple/20 flex items-center justify-center flex-shrink-0">
                    <Brain size={16} className="text-neon-purple" />
                  </div>
                  <div className="flex-1">
                    <div className="text-xs text-earth-400 mb-1">AI Assistant</div>
                    <div className="text-sm text-white mb-2">{command.final_response}</div>
                    
                    {/* Confidence */}
                    {command.confidence && (
                      <div className="flex items-center gap-2 text-xs">
                        <div className="flex items-center gap-1 text-neon-green">
                          <CheckCircle size={12} />
                          <span>Confidence: {(command.confidence * 100).toFixed(0)}%</span>
                        </div>
                        {command.sources.length > 0 && (
                          <div className="text-earth-400">
                            Sources: {command.sources.join(', ')}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Execution Trace */}
                {showTrace && (
                  <div className="mt-4">
                    <button
                      onClick={() => toggleExpanded(command.id)}
                      className="flex items-center gap-2 text-xs text-earth-400 hover:text-white transition-colors mb-2"
                    >
                      {expandedCommands.has(command.id) ? (
                        <ChevronUp size={12} />
                      ) : (
                        <ChevronDown size={12} />
                      )}
                      <span>Execution Trace ({command.tools_called.length} tools)</span>
                    </button>

                    <AnimatePresence>
                      {expandedCommands.has(command.id) && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          {/* Interpreted Plan */}
                          <div className="mb-3 p-3 rounded bg-earth-700/30 border border-earth-600/30">
                            <div className="text-[10px] text-earth-400 mb-1">Interpreted Plan</div>
                            <div className="text-xs text-earth-300">{command.interpreted_plan}</div>
                          </div>

                          {/* Tools Called */}
                          <div className="space-y-2">
                            {command.tools_called.map((tool, idx) => (
                              <div key={idx} className="p-3 rounded bg-earth-700/50 border border-earth-600/30">
                                <div className="flex items-center justify-between mb-2">
                                  <div className="flex items-center gap-2">
                                    <Zap size={12} className="text-neon-yellow" />
                                    <span className="text-xs font-medium text-white">{tool.tool_name}</span>
                                  </div>
                                  <div className="flex items-center gap-2 text-[10px] text-earth-400">
                                    <Clock size={10} />
                                    <span>{tool.execution_time_ms}ms</span>
                                  </div>
                                </div>
                                <div className="text-[10px] text-earth-400 mb-1">Arguments</div>
                                <pre className="text-[10px] text-earth-300 bg-earth-800/50 p-2 rounded overflow-x-auto">
                                  {JSON.stringify(tool.arguments, null, 2)}
                                </pre>
                                <div className="text-[10px] text-earth-400 mt-2 mb-1">Result</div>
                                <pre className="text-[10px] text-neon-green bg-earth-800/50 p-2 rounded overflow-x-auto">
                                  {JSON.stringify(tool.result, null, 2)}
                                </pre>
                              </div>
                            ))}
                          </div>

                          {/* Approval Requests */}
                          {command.approval_requests.length > 0 && (
                            <div className="mt-3">
                              <div className="text-[10px] text-earth-400 mb-2">Approval Requests</div>
                              <div className="space-y-2">
                                {command.approval_requests.map(approval => (
                                  <div
                                    key={approval.id}
                                    className={`p-2 rounded border ${
                                      approval.status === 'APPROVED'
                                        ? 'bg-neon-green/10 border-neon-green/30'
                                        : approval.status === 'PENDING'
                                        ? 'bg-neon-yellow/10 border-neon-yellow/30'
                                        : 'bg-neon-red/10 border-neon-red/30'
                                    }`}
                                  >
                                    <div className="flex items-center justify-between mb-1">
                                      <span className="text-xs font-medium text-white">{approval.action}</span>
                                      <span className={`text-[10px] px-2 py-0.5 rounded ${
                                        approval.status === 'APPROVED'
                                          ? 'bg-neon-green/20 text-neon-green'
                                          : approval.status === 'PENDING'
                                          ? 'bg-neon-yellow/20 text-neon-yellow'
                                          : 'bg-neon-red/20 text-neon-red'
                                      }`}>
                                        {approval.status}
                                      </span>
                                    </div>
                                    <div className="text-[10px] text-earth-400">{approval.summary}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Processing Indicator */}
        <AnimatePresence>
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="rounded-lg border border-neon-blue/50 bg-neon-blue/10 p-4"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-neon-blue/20 flex items-center justify-center">
                  <Brain size={16} className="text-neon-blue animate-pulse" />
                </div>
                <div className="flex-1">
                  <div className="text-sm text-white">Processing your command...</div>
                  <div className="text-xs text-earth-400">Analyzing intent and selecting tools</div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input Form */}
      <div className="border-t border-earth-600/50 bg-earth-800/50 p-6">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter a command... (e.g., 'Show me all satellites over Spain')"
              className="w-full px-4 py-3 rounded-lg bg-earth-700/50 border border-earth-600/50 text-white placeholder-earth-500 focus:outline-none focus:border-neon-blue/50 transition-colors"
              disabled={isProcessing}
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="px-6 py-3 rounded-lg bg-neon-blue text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-neon-blue/80 transition-colors flex items-center gap-2"
          >
            <Send size={16} />
            Send
          </button>
        </form>

        {/* Quick Actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          {[
            'Show me all satellites over Spain',
            'Track the nearest aircraft',
            'Show active fires in this region',
            'Find recent Sentinel-2 imagery',
          ].map(suggestion => (
            <button
              key={suggestion}
              onClick={() => setInput(suggestion)}
              className="px-3 py-1.5 text-xs rounded-lg bg-earth-700/50 border border-earth-600/50 text-earth-300 hover:text-white hover:border-earth-500 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
