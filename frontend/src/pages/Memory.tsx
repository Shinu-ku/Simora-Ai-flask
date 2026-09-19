import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { Brain, Database, Cpu, TrendingUp } from 'lucide-react';

export default function Memory() {
  const [memories, setMemories] = useState<any[]>([]);
  const [calibrations, setCalibrations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get('/memory'),
      api.get('/memory/calibrations')
    ]).then(([memRes, calRes]) => {
      setMemories(memRes.data);
      setCalibrations(calRes.data);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading business memory...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-navy-900 tracking-tight">Business Memory</h1>
          <div className="flex items-center mt-2 space-x-2 text-sm text-slate-500">
            <span className="flex items-center px-2 py-1 bg-slate-100 rounded-md">
              <Database className="w-4 h-4 mr-1" />
              Local Memory Connected
            </span>
            <span>Learning Loop: Active</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center mb-4">
            <Cpu className="w-6 h-6 text-electric-600 mr-2" />
            <h2 className="text-lg font-semibold text-navy-900">Calibration Models</h2>
          </div>
          <p className="text-sm text-slate-500 mb-6">
            SIMORA uses past prediction errors to calibrate future simulations.
          </p>

          <div className="space-y-4">
            {calibrations.map(cal => (
              <div key={cal.action_type} className="border border-slate-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-navy-900 uppercase">{cal.action_type}</h3>
                    <p className="text-xs text-slate-500">v{cal.version} • {cal.sample_count} samples</p>
                  </div>
                  <div className={`px-2 py-1 rounded text-xs font-semibold ${
                    cal.average_error > 0.05 ? 'bg-red-100 text-red-700' :
                    cal.average_error < -0.05 ? 'bg-amber-100 text-amber-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    Err: {(cal.average_error * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="flex items-center justify-between mt-4 p-3 bg-slate-50 rounded">
                  <span className="text-sm font-medium text-slate-700">Calibration Factor</span>
                  <span className="font-mono text-electric-700 font-bold">{cal.calibration_factor.toFixed(3)}x</span>
                </div>
              </div>
            ))}
            {calibrations.length === 0 && (
              <div className="text-center p-8 text-slate-500 border border-dashed border-slate-300 rounded-lg">
                No calibrations built yet. Execute strategies and record outcomes.
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center mb-4">
            <Brain className="w-6 h-6 text-electric-600 mr-2" />
            <h2 className="text-lg font-semibold text-navy-900">Observed Insights</h2>
          </div>
          
          <div className="space-y-4">
            {memories.map(mem => (
              <div key={mem.id} className="p-4 border border-slate-200 rounded-lg">
                <div className="flex items-center mb-2">
                  <TrendingUp className="w-4 h-4 text-electric-500 mr-2" />
                  <span className="text-xs font-semibold text-slate-500">{mem.memory_type}</span>
                  <span className="text-xs text-slate-400 ml-auto">{new Date(mem.created_at).toLocaleDateString()}</span>
                </div>
                <p className="text-sm text-navy-900">{mem.content}</p>
                {mem.metadata_json && mem.metadata_json.error !== undefined && (
                  <div className="mt-2 text-xs text-slate-500 font-mono bg-slate-50 p-2 rounded">
                    Adjusting future predictions by {((mem.metadata_json.new_factor - 1) * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            ))}
            {memories.length === 0 && (
              <div className="text-center p-8 text-slate-500 border border-dashed border-slate-300 rounded-lg">
                Memory is empty.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
