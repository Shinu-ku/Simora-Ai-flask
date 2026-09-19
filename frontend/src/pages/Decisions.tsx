import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { CheckCircle, XCircle, PlayCircle, Clock } from 'lucide-react';

export default function Decisions() {
  const [decisions, setDecisions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [outcomeDecisionId, setOutcomeDecisionId] = useState<string | null>(null);
  const [actualUnits, setActualUnits] = useState('');
  const [actualRevenue, setActualRevenue] = useState('');
  const [actualProfit, setActualProfit] = useState('');

  const fetchDecisions = () => {
    setLoading(true);
    api.get('/decisions')
      .then(res => setDecisions(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  const handleAction = async (id: string, action: 'approve' | 'reject' | 'execute') => {
    try {
      await api.post(`/decisions/${id}/${action}`);
      fetchDecisions();
    } catch (err) {
      console.error(err);
      alert(`Failed to ${action} decision.`);
    }
  };

  const handleRecordOutcome = async () => {
    if (!outcomeDecisionId) return;
    try {
      await api.post(`/decisions/${outcomeDecisionId}/outcome`, {
        actual_units: parseInt(actualUnits),
        actual_revenue: parseFloat(actualRevenue),
        actual_profit: parseFloat(actualProfit)
      });
      setOutcomeDecisionId(null);
      fetchDecisions();
    } catch (err) {
      console.error(err);
      alert('Failed to record outcome.');
    }
  };

  if (loading) return <div className="p-8">Loading decisions...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-navy-900 tracking-tight">Decisions & Approvals</h1>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Strategy</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Projected Lift</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
              <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {decisions.map((decision) => (
              <tr key={decision.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-navy-900">{decision.action_type.toUpperCase()} - {(decision.value * 100).toFixed(0)}%</div>
                  <div className="text-sm text-slate-500">Duration: {decision.duration_days} days</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-semibold text-slate-700">Predicted: ${decision.predicted_revenue.toFixed(2)} / {decision.predicted_units}U</div>
                  {decision.actual_units !== null ? (
                    <div className="text-sm font-semibold mt-1">
                      <span className="text-navy-900">Actual: ${decision.actual_revenue.toFixed(2)} / {decision.actual_units}U</span>
                      {decision.actual_units !== decision.predicted_units && (
                        <span className={`ml-2 ${decision.actual_units > decision.predicted_units ? 'text-green-600' : 'text-red-600'}`}>
                          ({decision.actual_units > decision.predicted_units ? '+' : ''}{Math.round(((decision.actual_units - decision.predicted_units) / decision.predicted_units) * 100)}% err)
                        </span>
                      )}
                    </div>
                  ) : (
                    <div className="text-sm text-slate-400 mt-1">Awaiting outcome...</div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${decision.status === 'PENDING' ? 'bg-amber-100 text-amber-800' : 
                      decision.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                      decision.status === 'EXECUTED' ? 'bg-green-100 text-green-800' : 
                      'bg-red-100 text-red-800'}`}>
                    {decision.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-3">
                  {decision.status === 'PENDING' && (
                    <>
                      <button onClick={() => handleAction(decision.id, 'approve')} className="text-green-600 hover:text-green-900">
                        <CheckCircle className="w-5 h-5 inline" />
                      </button>
                      <button onClick={() => handleAction(decision.id, 'reject')} className="text-red-600 hover:text-red-900">
                        <XCircle className="w-5 h-5 inline" />
                      </button>
                    </>
                  )}
                  {decision.status === 'APPROVED' && (
                    <button 
                      onClick={() => handleAction(decision.id, 'execute')} 
                      className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-electric-600 hover:bg-electric-700"
                    >
                      <PlayCircle className="w-4 h-4 mr-1" />
                      Simulated Execution
                    </button>
                  )}
                  {decision.status === 'EXECUTED' && decision.actual_units === null && (
                    <button 
                      onClick={() => setOutcomeDecisionId(decision.id)}
                      className="inline-flex items-center px-3 py-1 border border-slate-300 text-xs font-medium rounded shadow-sm text-slate-700 bg-white hover:bg-slate-50"
                    >
                      Record Outcome
                    </button>
                  )}
                  {decision.actual_units !== null && (
                    <span className="text-slate-400 inline-flex items-center text-xs">
                      Recorded
                    </span>
                  )}
                </td>
              </tr>
            ))}
            {decisions.length === 0 && (
              <tr>
                <td colSpan={4} className="px-6 py-12 text-center text-slate-500">
                  No decisions found. Run a simulation to create one.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {outcomeDecisionId && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-bold text-navy-900 mb-4">Record Actual Outcome</h3>
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Actual Units Sold</label>
                <input type="number" value={actualUnits} onChange={e => setActualUnits(e.target.value)} className="w-full border-slate-300 rounded-md" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Actual Revenue ($)</label>
                <input type="number" value={actualRevenue} onChange={e => setActualRevenue(e.target.value)} className="w-full border-slate-300 rounded-md" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Actual Profit ($)</label>
                <input type="number" value={actualProfit} onChange={e => setActualProfit(e.target.value)} className="w-full border-slate-300 rounded-md" />
              </div>
            </div>
            <div className="flex justify-end space-x-3">
              <button onClick={() => setOutcomeDecisionId(null)} className="px-4 py-2 border border-slate-300 text-slate-700 rounded-md hover:bg-slate-50">Cancel</button>
              <button onClick={handleRecordOutcome} className="px-4 py-2 bg-electric-600 text-white rounded-md hover:bg-electric-700">Save Outcome</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
