"use client";

import Header from '../../components/Header';
import PriceManager from '../../components/PriceManager';

export default function SettingsPage() {
    return (
        <div className="min-h-screen bg-gray-50">
            <Header />

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div className="px-4 py-6 sm:px-0">
                    <h1 className="text-2xl font-bold text-gray-900 mb-6">Material Rates Settings</h1>
                    <div className="bg-white shadow rounded-lg p-6">
                        <PriceManager />
                    </div>
                </div>
            </main>
        </div>
    );
}
