import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { Activity, Package, TrendingUp, AlertCircle, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [twin, setTwin] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/digital-twin/latest')
      .then(res => {
        setTwin(res.data);
      })
      .catch(err => {
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-navy-900 tracking-tight">Business Overview</h1>
        <button 
          onClick={() => navigate('/simulate')}
          className="flex items-center px-4 py-2 bg-electric-600 text-white rounded-md hover:bg-electric-700 transition"
        >
          <Play className="w-4 h-4 mr-2" />
          Run Simulation
        </button>
      </div>

      {!twin ? (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 flex flex-col items-center justify-center text-center">
          <AlertCircle className="w-12 h-12 text-amber-500 mb-4" />
          <h2 className="text-lg font-semibold text-amber-900 mb-2">Digital Twin Not Found</h2>
          <p className="text-amber-700 max-w-md mb-6">
            SIMORA requires a Digital Twin to run simulations. Please import historical sales data to generate your initial twin.
          </p>
          <button 
            onClick={() => api.post('/digital-twin/generate').then(() => window.location.reload())}
            className="px-4 py-2 bg-amber-600 text-white rounded-md hover:bg-amber-700 transition"
          >
            Generate Digital Twin
          </button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-slate-500">Twin Version</h3>
                <Activity className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">{twin.model_version}</p>
              <p className="text-xs text-slate-500 mt-2">Active simulation model</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-slate-500">Products Tracked</h3>
                <Package className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">{Object.keys(twin.features.products || {}).length}</p>
              <p className="text-xs text-slate-500 mt-2">With sufficient data</p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-slate-500">Confidence Score</h3>
                <TrendingUp className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">{(twin.confidence * 100).toFixed(0)}%</p>
              <p className="text-xs text-slate-500 mt-2">Based on historical density</p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-slate-500">Data Quality</h3>
                <div className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  twin.data_quality === 'High' ? 'bg-green-100 text-green-700' :
                  twin.data_quality === 'Medium' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'
                }`}>
                  {twin.data_quality}
                </div>
              </div>
              <p className="text-sm text-navy-900 font-medium">Last updated:</p>
              <p className="text-xs text-slate-500 mt-1">{new Date(twin.generated_at).toLocaleString()}</p>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6">
             <h2 className="text-lg font-semibold text-navy-900 mb-4">Recent Simulations</h2>
             <div className="text-center py-12 text-slate-500">
               <p>No recent simulations found.</p>
               <button 
                 onClick={() => navigate('/simulate')}
                 className="mt-4 text-electric-600 hover:text-electric-700 font-medium"
               >
                 Run your first simulation &rarr;
               </button>
             </div>
          </div>
        </>
      )}
    </div>
  );
}
