import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { BarChart3, TrendingUp, DollarSign, Package, PieChart } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export default function Analytics() {
  const [timeframe, setTimeframe] = useState('30D');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get(`/analytics?timeframe=${timeframe}`)
      .then(res => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [timeframe]);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-navy-900 tracking-tight">Business Analytics</h1>
        <div className="flex bg-slate-100 p-1 rounded-lg">
          {['7D', '30D', '90D', '6M'].map(t => (
            <button
              key={t}
              onClick={() => setTimeframe(t)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition ${
                timeframe === t 
                  ? 'bg-white text-navy-900 shadow-sm' 
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {loading || !data ? (
        <div className="p-8 text-center text-slate-500">Loading analytics...</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-slate-500">Revenue</h3>
                <DollarSign className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">${data.summary.revenue.toFixed(2)}</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-slate-500">Profit</h3>
                <TrendingUp className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">${data.summary.profit.toFixed(2)}</p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-slate-500">Units Sold</h3>
                <Package className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">{data.summary.units}</p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-slate-500">AOV</h3>
                <BarChart3 className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">${data.summary.aov.toFixed(2)}</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-slate-500">Margin</h3>
                <PieChart className="w-5 h-5 text-electric-500" />
              </div>
              <p className="text-2xl font-bold text-navy-900">{(data.summary.margin * 100).toFixed(1)}%</p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mt-6">
            <h2 className="text-lg font-semibold text-navy-900 mb-6">Revenue vs Profit ({timeframe})</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.chart}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dx={-10} tickFormatter={(val) => `$${val}`} />
                  <Tooltip 
                    contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                    formatter={(value: number) => [`$${value.toFixed(2)}`]}
                  />
                  <Line type="monotone" dataKey="revenue" name="Revenue" stroke="#0ea5e9" strokeWidth={3} dot={false} activeDot={{r: 6}} />
                  <Line type="monotone" dataKey="profit" name="Profit" stroke="#10b981" strokeWidth={3} dot={false} activeDot={{r: 6}} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
