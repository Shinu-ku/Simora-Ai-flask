import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import Login from './pages/Login'
import Register from './pages/Register'
import Onboarding from './pages/Onboarding'
import DashboardLayout from './layouts/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Simulate from './pages/Simulate'
import Decisions from './pages/Decisions'
import Memory from './pages/Memory'
import Analytics from './pages/Analytics'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/onboarding" element={<Onboarding />} />
            
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/products" element={<Products />} />
              <Route path="/simulate" element={<Simulate />} />
              <Route path="/decisions" element={<Decisions />} />
              <Route path="/memory" element={<Memory />} />
              <Route path="/analytics" element={<Analytics />} />
              {/* Other pages will go here */}
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App

