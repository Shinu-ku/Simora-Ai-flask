import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export const useAuth = () => {
  const queryClient = useQueryClient();

  const userQuery = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const token = localStorage.getItem('token');
      if (!token) return null;
      const { data } = await api.get('/auth/me');
      return data;
    },
    retry: false,
  });

  const loginMutation = useMutation({
    mutationFn: async (credentials: any) => {
      const formData = new URLSearchParams();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);
      const { data } = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      return data;
    },
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token);
      queryClient.setQueryData(['user'], data.user);
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (credentials: any) => {
      const { data } = await api.post('/auth/register', credentials);
      return data;
    },
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token);
      queryClient.setQueryData(['user'], data.user);
    },
  });

  const logout = () => {
    localStorage.removeItem('token');
    queryClient.setQueryData(['user'], null);
  };

  return {
    user: userQuery.data,
    isLoading: userQuery.isLoading,
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout,
  };
};
