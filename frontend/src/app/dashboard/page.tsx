"use client";

import { useEffect, useState } from 'react';
import api from '../api/axios';
import Link from 'next/link';
import { Plus, FileText, LogOut, Trash2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import Header from '../../components/Header';

interface Estimate {
    id: number;
    customer_name: string;
    created_at: string;
    total_amount: number;
    total_area: number;
}

export default function Dashboard() {
    const [estimates, setEstimates] = useState<Estimate[]>([]);
    const router = useRouter();

    useEffect(() => {
        const fetchEstimates = async () => {
            try {
                const response = await api.get('/estimates/');
                setEstimates(response.data);
            } catch (error) {
                console.error('Failed to fetch estimates', error);
                router.push('/login');
            }
        };

        fetchEstimates();
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    const handleDeleteEstimate = async (id: number, e: React.MouseEvent) => {
        e.preventDefault(); // Prevent navigation
        if (confirm('Are you sure you want to delete this estimate? This action cannot be undone.')) {
            try {
                await api.delete(`/estimates/${id}`);
                // Refresh list
                setEstimates(estimates.filter(est => est.id !== id));
            } catch (error) {
                console.error('Failed to delete estimate', error);
                alert('Failed to delete estimate');
            }
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <Header />

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div className="px-4 py-6 sm:px-0">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold text-gray-900">Recent Estimates</h2>
                        <Link href="/estimates/new" className="flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                            <Plus className="h-5 w-5 mr-2" />
                            New Estimate
                        </Link>
                    </div>

                    <div className="bg-white shadow overflow-hidden sm:rounded-md">
                        <ul className="divide-y divide-gray-200">
                            {estimates.map((estimate) => (
                                <li key={estimate.id} className="flex items-center hover:bg-gray-50 transition-colors">
                                    <Link href={`/estimates/${estimate.id}`} className="block flex-1 px-4 py-4 sm:px-6">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center">
                                                <FileText className="h-6 w-6 text-gray-400 mr-3" />
                                                <p className="text-sm font-medium text-indigo-600 truncate">
                                                    {estimate.customer_name}
                                                </p>
                                            </div>
                                            <div className="ml-2 shrink-0 flex">
                                                <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                    ₹{estimate.total_amount.toFixed(2)}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="mt-2 sm:flex sm:justify-between">
                                            <div className="sm:flex">
                                                <p className="flex items-center text-sm text-gray-500">
                                                    Area: {estimate.total_area.toFixed(2)} sq.ft
                                                </p>
                                            </div>
                                            <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                                <p>
                                                    {new Date(estimate.created_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                    </Link>
                                    <div className="px-4">
                                        <button
                                            onClick={(e) => handleDeleteEstimate(estimate.id, e)}
                                            className="text-gray-400 hover:text-red-600 transition-colors p-2 rounded-full hover:bg-red-50"
                                            title="Delete Estimate"
                                        >
                                            <Trash2 className="h-5 w-5" />
                                        </button>
                                    </div>
                                </li>
                            ))}
                            {estimates.length === 0 && (
                                <li className="px-4 py-8 text-center text-gray-500">
                                    No estimates found. Create your first one!
                                </li>
                            )}
                        </ul>
                    </div>
                </div>
            </main>
        </div>
    )
}
