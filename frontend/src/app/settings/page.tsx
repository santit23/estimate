"use client";

import { useEffect, useState } from 'react';
import api from '../api/axios';
import Header from '../../components/Header';
import { Save, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface MaterialRate {
    id?: number;
    series: string;
    quality: string;
    material_name: string;
    rate: number;
}

export default function SettingsPage() {
    const [rates, setRates] = useState<MaterialRate[]>([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchRates = async () => {
            try {
                const response = await api.get('/rates/');
                // Sort rates for consistent display
                const sortedRates = response.data.sort((a: MaterialRate, b: MaterialRate) => {
                    if (a.series !== b.series) return a.series.localeCompare(b.series);
                    if (a.quality !== b.quality) return a.quality.localeCompare(b.quality);
                    return a.material_name.localeCompare(b.material_name);
                });
                setRates(sortedRates);
            } catch (err) {
                console.error('Failed to fetch rates', err);
                setError('Failed to load rates. Please try again.');
            } finally {
                setLoading(false);
            }
        };

        fetchRates();
    }, []);

    const handleRateChange = (index: number, value: string) => {
        const newRates = [...rates];
        newRates[index].rate = parseFloat(value) || 0;
        setRates(newRates);
    };

    const handleSave = async () => {
        setSaving(true);
        setError('');
        setSuccess('');
        try {
            await api.post('/rates/', rates);
            setSuccess('Rates updated successfully!');
            setTimeout(() => setSuccess(''), 3000);
        } catch (err) {
            console.error('Failed to update rates', err);
            setError('Failed to save rates. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50">
                <Header />
                <div className="flex items-center justify-center h-64">
                    <div className="text-gray-500">Loading rates...</div>
                </div>
            </div>
        );
    }

    // Group rates by Series -> Quality for better UI
    const groupedRates: { [key: string]: MaterialRate[] } = {};
    rates.forEach(rate => {
        const key = `${rate.series} - ${rate.quality}`;
        if (!groupedRates[key]) {
            groupedRates[key] = [];
        }
        groupedRates[key].push(rate);
    });

    return (
        <div className="min-h-screen bg-gray-50">
            <Header />

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div className="px-4 py-6 sm:px-0">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl font-bold text-gray-900">Material Rates Settings</h1>
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white ${saving ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                                }`}
                        >
                            <Save className="h-4 w-4 mr-2" />
                            {saving ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>

                    {error && (
                        <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <AlertCircle className="h-5 w-5 text-red-400" />
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm text-red-700">{error}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {success && (
                        <div className="mb-4 bg-green-50 border-l-4 border-green-400 p-4">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <Save className="h-5 w-5 text-green-400" />
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm text-green-700">{success}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="space-y-6">
                        {Object.entries(groupedRates).map(([groupName, groupRates]) => (
                            <div key={groupName} className="bg-white shadow sm:rounded-lg overflow-hidden">
                                <div className="px-4 py-5 sm:px-6 bg-gray-50 border-b border-gray-200">
                                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                                        {groupName} Series
                                    </h3>
                                </div>
                                <div className="px-4 py-5 sm:p-6">
                                    <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2 lg:grid-cols-3">
                                        {groupRates.map((rate) => {
                                            // Find the index in the original rates array to update
                                            const index = rates.findIndex(r =>
                                                r.series === rate.series &&
                                                r.quality === rate.quality &&
                                                r.material_name === rate.material_name
                                            );

                                            // Format material name for display
                                            const displayName = rate.material_name
                                                .replace(/_/g, ' ')
                                                .replace(/\b\w/g, l => l.toUpperCase());

                                            return (
                                                <div key={`${rate.series}-${rate.quality}-${rate.material_name}`}>
                                                    <label className="block text-sm font-medium text-gray-700">
                                                        {displayName}
                                                    </label>
                                                    <div className="mt-1 relative rounded-md shadow-sm">
                                                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                                            <span className="text-gray-500 sm:text-sm">₹</span>
                                                        </div>
                                                        <input
                                                            type="number"
                                                            step="0.01"
                                                            value={rate.rate}
                                                            onChange={(e) => handleRateChange(index, e.target.value)}
                                                            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md text-gray-900"
                                                        />
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}
