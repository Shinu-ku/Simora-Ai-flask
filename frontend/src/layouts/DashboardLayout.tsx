import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { 
  LayoutDashboard, 
  LineChart, 
  BrainCircuit, 
  History, 
  Settings, 
  LogOut,
  Menu,
  Box,
  Database
} from 'lucide-react';

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  // Protected route mechanism
  if (user === null) {
    navigate('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Products', href: '/products', icon: Box },
    { name: 'Simulate', href: '/simulate', icon: BrainCircuit },
    { name: 'Analytics', href: '/analytics', icon: LineChart },
    { name: 'Decisions', href: '/decisions', icon: History },
    { name: 'Memory', href: '/memory', icon: Database },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <div className="hidden md:flex w-64 flex-col bg-white border-r border-slate-200">
        <div className="h-16 flex items-center px-6 border-b border-slate-200">
          <h1 className="text-xl font-bold text-navy-900 tracking-tight">SIMORA</h1>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = location.pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-electric-50 text-electric-600' 
                    : 'text-slate-600 hover:bg-slate-50 hover:text-navy-900'
                }`}
              >
                <item.icon className={`mr-3 h-5 w-5 ${isActive ? 'text-electric-600' : 'text-slate-400'}`} />
                {item.name}
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-slate-200">
          <div className="flex items-center mb-4 px-2">
            <div className="h-8 w-8 rounded-full bg-electric-100 flex items-center justify-center text-electric-700 font-bold">
              {user?.email?.charAt(0).toUpperCase()}
            </div>
            <div className="ml-3 truncate">
              <p className="text-sm font-medium text-slate-900 truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex w-full items-center px-3 py-2 text-sm font-medium text-slate-600 rounded-md hover:bg-slate-50 hover:text-red-600 transition-colors"
          >
            <LogOut className="mr-3 h-5 w-5 text-slate-400 group-hover:text-red-500" />
            Sign out
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile header */}
        <div className="md:hidden h-16 flex items-center justify-between px-4 bg-white border-b border-slate-200">
          <h1 className="text-xl font-bold text-navy-900 tracking-tight">SIMORA</h1>
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
            <Menu className="h-6 w-6 text-slate-600" />
          </button>
        </div>
        
        <main className="flex-1 overflow-y-auto bg-slate-50 p-6 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
