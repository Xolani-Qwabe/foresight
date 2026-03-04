'use client';

import React from 'react';
import { useDashboard } from '@/domain/user/dashboard/hook';






const Dashboard: React.FC = () => {
  const { user, isLoading, error } = useDashboard();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {(error as Error).message}</div>;
  if (!user) return <div>No user data available.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div>
        <p>
          <strong>Username:</strong> {user.username}
        </p>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <p>
          <strong>Credits:</strong> {user.credits}
        </p>
      </div>
    </div>
  );
};

export default Dashboard;