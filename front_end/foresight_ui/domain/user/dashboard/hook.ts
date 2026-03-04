'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth, User as AuthUser } from '@/domain/auth/authContext';

export function useDashboard() {
  const { user: authUser } = useAuth();

  const { data, isLoading, error } = useQuery<AuthUser | null>({
    queryKey: ['currentUser', authUser?.id],
    queryFn: async () => {
      if (!authUser) return null;
      const res = await fetch('/api/auth/session', { credentials: 'include' });
      if (!res.ok) throw new Error('Failed to fetch user data');
      const json = await res.json();
      return json.user as AuthUser;
    },
    initialData: authUser ?? null, // **use context first**
    enabled: !!authUser,
    refetchOnWindowFocus: false,
  });

  return { user: data, isLoading, error };
}