import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { api } from '../lib/api';
import { Building2 } from 'lucide-react';

export default function Onboarding() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    business_type: 'Retail',
    industry: 'Electronics',
    currency: 'USD'
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // If user somehow reaches here without being logged in
  if (user === null) {
    navigate('/login');
    return null;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await api.post('/business/', formData);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create business profile.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-xl w-full space-y-8 bg-white p-10 rounded-xl shadow-sm border border-slate-200">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 bg-navy-900 rounded-lg flex items-center justify-center">
            <Building2 className="h-6 w-6 text-white" />
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-navy-900">Set up your business</h2>
          <p className="mt-2 text-sm text-slate-600">
            Tell us about your company to get the most accurate digital twin predictions.
          </p>
        </div>
        
        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm text-center">
            {error}
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-slate-700">Business Name</label>
              <input
                type="text"
                name="name"
                required
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-slate-300 placeholder-slate-400 text-slate-900 rounded-md focus:outline-none focus:ring-electric-500 focus:border-electric-500 sm:text-sm"
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g. Rajesh Electronics"
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">Business Type</label>
                <select
                  name="business_type"
                  className="mt-1 block w-full px-3 py-2 border border-slate-300 bg-white rounded-md focus:outline-none focus:ring-electric-500 focus:border-electric-500 sm:text-sm"
                  value={formData.business_type}
                  onChange={handleChange}
                >
                  <option value="Retail">Retail</option>
                  <option value="E-commerce">E-commerce</option>
                  <option value="Wholesale">Wholesale</option>
                  <option value="Services">Services</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Industry</label>
                <select
                  name="industry"
                  className="mt-1 block w-full px-3 py-2 border border-slate-300 bg-white rounded-md focus:outline-none focus:ring-electric-500 focus:border-electric-500 sm:text-sm"
                  value={formData.industry}
                  onChange={handleChange}
                >
                  <option value="Electronics">Electronics</option>
                  <option value="Apparel">Apparel</option>
                  <option value="Home & Garden">Home & Garden</option>
                  <option value="Health & Beauty">Health & Beauty</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700">Primary Currency</label>
              <select
                name="currency"
                className="mt-1 block w-full px-3 py-2 border border-slate-300 bg-white rounded-md focus:outline-none focus:ring-electric-500 focus:border-electric-500 sm:text-sm"
                value={formData.currency}
                onChange={handleChange}
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="INR">INR (₹)</option>
              </select>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2.5 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-navy-900 hover:bg-navy-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-navy-900 transition-colors disabled:opacity-70"
            >
              {isLoading ? 'Creating...' : 'Continue to Dashboard'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
