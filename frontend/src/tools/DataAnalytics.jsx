import { useState, useEffect } from 'react';
import { Database, BarChart3, Trash2, Sparkles, Loader2 } from 'lucide-react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const API_BASE = 'http://localhost:8000';

const DataAnalytics = () => {
    const [activeTab, setActiveTab] = useState('database');
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(false);
    const [models, setModels] = useState([]);

    // Form state for new records
    const [newRecord, setNewRecord] = useState({
        name: '',
        category: '',
        value: '',
        metadata: ''
    });

    // Analysis state
    const [analysisQuery, setAnalysisQuery] = useState('');
    const [selectedModel, setSelectedModel] = useState('llama-3.3-70b-versatile');
    const [analysisResult, setAnalysisResult] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);

    // Fetch records on component mount
    useEffect(() => {
        fetchRecords();
        fetchModels();
    }, []);

    const fetchRecords = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${API_BASE}/api/analytics/records`);
            if (response.data.status === 'success') {
                setRecords(response.data.records);
            }
        } catch (error) {
            console.error('Error fetching records:', error);
            alert('Failed to fetch records');
        } finally {
            setLoading(false);
        }
    };

    const fetchModels = async () => {
        try {
            const response = await axios.get(`${API_BASE}/api/analytics/models`);
            if (response.data.status === 'success') {
                setModels(response.data.models);
            }
        } catch (error) {
            console.error('Error fetching models:', error);
        }
    };

    const handleCreateRecord = async (e) => {
        e.preventDefault();

        if (!newRecord.name || !newRecord.category || !newRecord.value) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            setLoading(true);
            const payload = {
                name: newRecord.name,
                category: newRecord.category,
                value: parseFloat(newRecord.value),
                metadata: newRecord.metadata ? JSON.parse(newRecord.metadata) : null
            };

            const response = await axios.post(`${API_BASE}/api/analytics/records`, payload);

            if (response.data.status === 'success') {
                alert('Record created successfully!');
                setNewRecord({ name: '', category: '', value: '', metadata: '' });
                fetchRecords();
            } else {
                alert(`Error: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error creating record:', error);
            alert('Failed to create record. Check metadata JSON format.');
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteRecord = async (id) => {
        if (!confirm('Are you sure you want to delete this record?')) return;

        try {
            setLoading(true);
            const response = await axios.delete(`${API_BASE}/api/analytics/records/${id}`);

            if (response.data.status === 'success') {
                alert('Record deleted successfully!');
                fetchRecords();
            } else {
                alert(`Error: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error deleting record:', error);
            alert('Failed to delete record');
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyze = async () => {
        if (!analysisQuery.trim()) {
            alert('Please enter an analysis query');
            return;
        }

        try {
            setAnalyzing(true);
            setAnalysisResult(null);

            const response = await axios.post(`${API_BASE}/api/analytics/analyze`, {
                query: analysisQuery,
                model_name: selectedModel
            });

            if (response.data.status === 'success') {
                setAnalysisResult(response.data);
            } else {
                alert(`Error: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error analyzing data:', error);
            alert('Failed to analyze data');
        } finally {
            setAnalyzing(false);
        }
    };

    const handleLoadSampleData = async () => {
        if (!confirm('Load sample analytics data? This will add 17 demonstration records to your database.')) return;

        try {
            setLoading(true);
            const response = await axios.post(`${API_BASE}/api/analytics/seed`);

            if (response.data.status === 'success') {
                alert(`✅ ${response.data.message}`);
                fetchRecords();
            } else {
                alert(`Error: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error loading sample data:', error);
            alert('Failed to load sample data');
        } finally {
            setLoading(false);
        }
    };

    const handleClearAllData = async () => {
        if (!confirm('⚠️ WARNING: This will delete ALL records from the database. This action cannot be undone. Are you sure?')) return;

        try {
            setLoading(true);
            const response = await axios.delete(`${API_BASE}/api/analytics/clear`);

            if (response.data.status === 'success') {
                alert(`🗑️ ${response.data.message}`);
                fetchRecords();
            } else {
                alert(`Error: ${response.data.message}`);
            }
        } catch (error) {
            console.error('Error clearing data:', error);
            alert('Failed to clear data');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 shadow-lg shadow-indigo-500/30 flex items-center justify-center">
                    <BarChart3 className="w-7 h-7 text-white" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Data Analytics Tool</h1>
                    <p className="text-slate-500 mt-1">Manage your data and analyze with AI</p>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 bg-white/70 backdrop-blur-xl p-2 rounded-2xl border border-slate-200 shadow-sm">
                <button
                    onClick={() => setActiveTab('database')}
                    className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${activeTab === 'database'
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/30'
                        : 'text-slate-600 hover:bg-slate-50'
                        }`}
                >
                    <Database className="w-5 h-5" />
                    Database Management
                </button>
                <button
                    onClick={() => setActiveTab('analysis')}
                    className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${activeTab === 'analysis'
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/30'
                        : 'text-slate-600 hover:bg-slate-50'
                        }`}
                >
                    <Sparkles className="w-5 h-5" />
                    LLM Analysis
                </button>
            </div>

            {/* Database Management Tab */}
            {activeTab === 'database' && (
                <div className="space-y-6">
                    {/* Insert Record Form */}
                    <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-slate-200 shadow-xl p-8">
                        <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                            <Database className="w-6 h-6 text-indigo-600" />
                            Insert New Record
                        </h2>

                        <form onSubmit={handleCreateRecord} className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Name *
                                    </label>
                                    <input
                                        type="text"
                                        value={newRecord.name}
                                        onChange={(e) => setNewRecord({ ...newRecord, name: e.target.value })}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                                        placeholder="e.g., Q1 Revenue"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Category *
                                    </label>
                                    <input
                                        type="text"
                                        value={newRecord.category}
                                        onChange={(e) => setNewRecord({ ...newRecord, category: e.target.value })}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                                        placeholder="e.g., Sales, Marketing"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Value *
                                    </label>
                                    <input
                                        type="number"
                                        step="0.01"
                                        value={newRecord.value}
                                        onChange={(e) => setNewRecord({ ...newRecord, value: e.target.value })}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                                        placeholder="e.g., 150000"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Metadata (JSON)
                                    </label>
                                    <input
                                        type="text"
                                        value={newRecord.metadata}
                                        onChange={(e) => setNewRecord({ ...newRecord, metadata: e.target.value })}
                                        className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                                        placeholder='{"region": "North America"}'
                                    />
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-medium shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Creating...
                                    </>
                                ) : (
                                    <>
                                        <Database className="w-5 h-5" />
                                        Insert Record
                                    </>
                                )}
                            </button>
                        </form>
                    </div>

                    {/* Records Table */}
                    <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-slate-200 shadow-xl p-8">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-bold text-slate-900">
                                All Records ({records.length})
                            </h2>

                            {/* Quick Actions */}
                            <div className="flex gap-2">
                                <button
                                    onClick={handleLoadSampleData}
                                    disabled={loading}
                                    className="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg text-sm font-medium hover:bg-indigo-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                                    title="Load demonstration data"
                                >
                                    <Sparkles className="w-4 h-4" />
                                    Load Sample Data
                                </button>

                                {records.length > 0 && (
                                    <button
                                        onClick={handleClearAllData}
                                        disabled={loading}
                                        className="px-4 py-2 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                                        title="Delete all records"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                        Clear All
                                    </button>
                                )}
                            </div>
                        </div>

                        {loading ? (
                            <div className="flex items-center justify-center py-12">
                                <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
                            </div>
                        ) : records.length === 0 ? (
                            <div className="text-center py-12 text-slate-500">
                                No records yet. Create your first record above!
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-slate-200">
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">ID</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Name</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Category</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Value</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Created</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {records.map((record) => (
                                            <tr key={record.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                                <td className="py-3 px-4 text-sm text-slate-600">{record.id}</td>
                                                <td className="py-3 px-4 text-sm font-medium text-slate-900">{record.name}</td>
                                                <td className="py-3 px-4">
                                                    <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-indigo-100 text-indigo-700">
                                                        {record.category}
                                                    </span>
                                                </td>
                                                <td className="py-3 px-4 text-sm font-semibold text-slate-900">
                                                    {record.value.toLocaleString()}
                                                </td>
                                                <td className="py-3 px-4 text-sm text-slate-500">
                                                    {new Date(record.created_at).toLocaleDateString()}
                                                </td>
                                                <td className="py-3 px-4">
                                                    <button
                                                        onClick={() => handleDeleteRecord(record.id)}
                                                        className="p-2 hover:bg-red-50 rounded-lg transition-colors group"
                                                        title="Delete record"
                                                    >
                                                        <Trash2 className="w-4 h-4 text-slate-400 group-hover:text-red-600 transition-colors" />
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* LLM Analysis Tab */}
            {activeTab === 'analysis' && (
                <div className="space-y-6">
                    {/* Analysis Form */}
                    <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-slate-200 shadow-xl p-8">
                        <h2 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                            <Sparkles className="w-6 h-6 text-indigo-600" />
                            AI-Powered Data Analysis
                        </h2>

                        <div className="space-y-4">
                            {/* Model Selector */}
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Select AI Model
                                </label>
                                <select
                                    value={selectedModel}
                                    onChange={(e) => setSelectedModel(e.target.value)}
                                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
                                >
                                    {models.map((model) => (
                                        <option key={model.id} value={model.id}>
                                            {model.name} - {model.description}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {/* Query Input */}
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Analysis Query
                                </label>
                                <textarea
                                    value={analysisQuery}
                                    onChange={(e) => setAnalysisQuery(e.target.value)}
                                    rows={4}
                                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white resize-none"
                                    placeholder="e.g., Analyze all records and identify trends, Summarize data by category, Find the highest performing categories..."
                                />
                            </div>

                            {/* Example Queries */}
                            <div className="flex flex-wrap gap-2">
                                <span className="text-xs text-slate-500 mr-2">Quick examples:</span>
                                {[
                                    'Summarize all records by category',
                                    'What are the trends in the data?',
                                    'Identify anomalies and outliers'
                                ].map((example) => (
                                    <button
                                        key={example}
                                        onClick={() => setAnalysisQuery(example)}
                                        className="text-xs px-3 py-1.5 rounded-lg bg-slate-100 text-slate-600 hover:bg-indigo-100 hover:text-indigo-700 transition-colors"
                                    >
                                        {example}
                                    </button>
                                ))}
                            </div>

                            <button
                                onClick={handleAnalyze}
                                disabled={analyzing || !analysisQuery.trim()}
                                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-medium shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                            >
                                {analyzing ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Sparkles className="w-5 h-5" />
                                        Analyze with AI
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Analysis Results */}
                    {analysisResult && (
                        <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-slate-200 shadow-xl p-8">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-xl font-bold text-slate-900">Analysis Results</h2>
                                <div className="flex items-center gap-4 text-sm text-slate-500">
                                    <span>📊 {analysisResult.records_analyzed} records analyzed</span>
                                    <span>🤖 {models.find(m => m.id === analysisResult.model_used)?.name || selectedModel}</span>
                                </div>
                            </div>

                            <div className="prose prose-slate max-w-none bg-gradient-to-br from-slate-50 to-indigo-50/30 rounded-xl p-6 border border-slate-200">
                                <ReactMarkdown>{analysisResult.analysis}</ReactMarkdown>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default DataAnalytics;
