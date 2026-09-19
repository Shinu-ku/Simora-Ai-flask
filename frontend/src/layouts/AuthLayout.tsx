import React from 'react';
import { Outlet } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-slate-50">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-sm border border-slate-100">
        <div className="flex justify-center mb-8">
          <h1 className="text-3xl font-bold text-navy-900 tracking-tight">SIMORA</h1>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
