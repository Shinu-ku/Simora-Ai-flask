import React, { useState, useEffect, useRef } from 'react';
import { api } from '../lib/api';
import { Play, TrendingUp, AlertTriangle, Mic, MicOff, Volume2 } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  sku: string;
}

interface SimulationResult {
  projected_units: number;
  projected_revenue: number;
  projected_profit: number;
  projected_margin: number;
  risk_score: number;
  confidence_score: number;
}

interface ComparisonResult {
  baseline: SimulationResult;
  counterfactual: SimulationResult;
}

export default function Simulate() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [discount, setDiscount] = useState('10');
  const [duration, setDuration] = useState('7');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [nlQuery, setNlQuery] = useState('');
  const [isNlMode, setIsNlMode] = useState(true);
  const [creatingDecision, setCreatingDecision] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Generate digital twin first
    api.post('/digital-twin/generate').catch(console.error);
    
    // Fetch products
    api.get('/products').then(res => {
      setProducts(res.data);
      if (res.data.length > 0) {
        setSelectedProduct(res.data[0].id);
      }
    }).catch(console.error);
  }, []);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      let res;
      let finalQuery = nlQuery;
      if (isNlMode) {
        res = await api.post('/simulate/natural-language', {
          query: finalQuery
        });
      } else {
        res = await api.post('/simulate', {
          product_id: selectedProduct,
          action_type: 'discount',
          value: parseFloat(discount) / 100.0,
          duration_days: parseInt(duration)
        });
      }
      setResult(res.data);
      
      // Auto-play explanation via voice
      if (res.data.explanation) {
        playVoice(res.data.explanation);
      }
      
    } catch (error) {
      console.error(error);
      alert('Failed to run simulation. Ensure Digital Twin is built.');
    } finally {
      setLoading(false);
    }
  };

  const playVoice = async (text: string) => {
    try {
      setIsPlaying(true);
      // Try ElevenLabs backend first
      const res = await api.post('/voice/synthesize', { text }, { responseType: 'blob' });
      const url = URL.createObjectURL(res.data);
      if (audioRef.current) {
        audioRef.current.src = url;
        audioRef.current.play();
        audioRef.current.onended = () => setIsPlaying(false);
      }
    } catch (e: any) {
      // Fallback to browser synthesis
      console.log("ElevenLabs not configured, using browser fallback");
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = () => setIsPlaying(false);
        window.speechSynthesis.speak(utterance);
      } else {
        setIsPlaying(false);
      }
    }
  };

  const toggleListen = () => {
    if (isListening) {
      setIsListening(false);
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setNlQuery(transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    
    recognition.start();
  };

  const handleApproveStrategy = async () => {
    if (!result) return;
    setCreatingDecision(true);
    try {
      await api.post('/decisions', {
        product_id: selectedProduct,
        action_type: 'discount',
        value: parseFloat(discount) / 100.0,
        duration_days: parseInt(duration),
        predicted_units: result.counterfactual.projected_units,
        predicted_revenue: result.counterfactual.projected_revenue,
        predicted_profit: result.counterfactual.projected_profit
      });
      navigate('/decisions');
    } catch (err) {
      console.error(err);
      alert('Failed to submit decision.');
    } finally {
      setCreatingDecision(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-navy-900 tracking-tight">Simulation Engine</h1>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-navy-900">Define Scenario</h2>
          <div className="flex items-center space-x-2">
            <span className={`text-sm ${isNlMode ? 'text-electric-600 font-medium' : 'text-slate-500'}`}>Natural Language</span>
            <button 
              onClick={() => setIsNlMode(!isNlMode)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${!isNlMode ? 'bg-electric-600' : 'bg-slate-300'}`}
            >
              <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${!isNlMode ? 'translate-x-6' : 'translate-x-1'}`} />
            </button>
            <span className={`text-sm ${!isNlMode ? 'text-electric-600 font-medium' : 'text-slate-500'}`}>Manual</span>
          </div>
        </div>

        {isNlMode ? (
          <div className="mb-6 relative">
            <label className="block text-sm font-medium text-slate-700 mb-2">Ask SIMORA</label>
            <div className="relative">
              <textarea 
                value={nlQuery}
                onChange={(e) => setNlQuery(e.target.value)}
                placeholder="e.g., What if I give a 10% discount on headphones this weekend?"
                className="w-full h-24 p-3 pr-12 border border-slate-300 rounded-md shadow-sm focus:border-electric-500 focus:ring-electric-500"
              />
              <button 
                onClick={toggleListen}
                className={`absolute right-3 bottom-3 p-2 rounded-full transition ${isListening ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
                title="Use voice input"
              >
                {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Target Product</label>
              <select 
                value={selectedProduct}
                onChange={(e) => setSelectedProduct(e.target.value)}
                className="w-full border-slate-300 rounded-md shadow-sm focus:border-electric-500 focus:ring-electric-500"
              >
                {products.map(p => (
                  <option key={p.id} value={p.id}>{p.name} ({p.sku})</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Discount (%)</label>
              <input 
                type="number" 
                value={discount}
                onChange={(e) => setDiscount(e.target.value)}
                className="w-full border-slate-300 rounded-md shadow-sm focus:border-electric-500 focus:ring-electric-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Duration (Days)</label>
              <input 
                type="number" 
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                className="w-full border-slate-300 rounded-md shadow-sm focus:border-electric-500 focus:ring-electric-500"
              />
            </div>
          </div>
        )}
        
        <div className="mt-2 flex justify-end">
          <button 
            onClick={handleSimulate}
            disabled={loading || (isNlMode && !nlQuery)}
            className="flex items-center px-4 py-2 bg-electric-600 text-white rounded-md hover:bg-electric-700 transition disabled:opacity-50"
          >
            <Play className="w-4 h-4 mr-2" />
            {loading ? 'Simulating...' : 'Run Simulation'}
          </button>
        </div>
      </div>

      {result && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-navy-900 mt-8">Strategy Comparison</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Baseline Card */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-slate-700">Baseline (Do Nothing)</h3>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-slate-500">Projected Revenue</p>
                  <p className="text-2xl font-bold text-navy-900">${result.baseline.projected_revenue.toFixed(2)}</p>
                </div>
                <div className="flex justify-between border-t border-slate-100 pt-3">
                  <div>
                    <p className="text-xs text-slate-500">Units Sold</p>
                    <p className="font-semibold text-slate-700">{result.baseline.projected_units}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Profit</p>
                    <p className="font-semibold text-slate-700">${result.baseline.projected_profit.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Margin</p>
                    <p className="font-semibold text-slate-700">{(result.baseline.projected_margin * 100).toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Counterfactual Card */}
            <div className="bg-electric-50 rounded-xl shadow-sm border border-electric-200 p-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-electric-600 text-white text-xs px-3 py-1 rounded-bl-lg font-medium">
                Recommended
              </div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-electric-900">With {discount}% Discount</h3>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-electric-700">Projected Revenue</p>
                  <div className="flex items-baseline">
                    <p className="text-2xl font-bold text-electric-900">${result.counterfactual.projected_revenue.toFixed(2)}</p>
                    {result.counterfactual.projected_revenue > result.baseline.projected_revenue && (
                      <span className="ml-2 flex items-center text-sm font-medium text-green-600">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        + {((result.counterfactual.projected_revenue / result.baseline.projected_revenue - 1) * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex justify-between border-t border-electric-200/50 pt-3">
                  <div>
                    <p className="text-xs text-electric-700">Units Sold</p>
                    <p className="font-semibold text-electric-900">{result.counterfactual.projected_units}</p>
                  </div>
                  <div>
                    <p className="text-xs text-electric-700">Profit</p>
                    <p className="font-semibold text-electric-900">${result.counterfactual.projected_profit.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-electric-700">Risk Score</p>
                    <p className="font-semibold text-electric-900 flex items-center">
                      {(result.counterfactual.risk_score * 100).toFixed(0)}%
                      {result.counterfactual.risk_score > 0.5 && <AlertTriangle className="w-3 h-3 text-amber-500 ml-1" />}
                    </p>
                  </div>
                </div>
                
                <div className="mt-6 pt-4 border-t border-electric-200">
                  <button 
                    onClick={handleApproveStrategy}
                    disabled={creatingDecision}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-electric-600 hover:bg-electric-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-electric-500 disabled:opacity-50"
                  >
                    {creatingDecision ? 'Submitting...' : 'Approve Strategy & Send to Review'}
                  </button>
                </div>
              </div>
            </div>

          </div>

          {(result as any).explanation && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-navy-900">Why did SIMORA predict this?</h3>
                <button 
                  onClick={() => playVoice((result as any).explanation)}
                  className={`p-1.5 rounded-full ${isPlaying ? 'bg-electric-100 text-electric-600 animate-pulse' : 'text-slate-400 hover:bg-slate-100 hover:text-slate-600'}`}
                >
                  <Volume2 className="w-5 h-5" />
                </button>
              </div>
              <p className="text-slate-700">{(result as any).explanation}</p>
              {(result as any).ai_parsed && (
                <div className="mt-4 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Gemini Parsed
                </div>
              )}
            </div>
          )}
        </div>
      )}
      <audio ref={audioRef} className="hidden" />
    </div>
  );
}
