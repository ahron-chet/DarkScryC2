"use client";
import { useState, useCallback, useRef } from "react";
import api from "../apiClient";

interface TaskStatus {
  status: string;
}

interface TaskResultOut {
  success: boolean;
  result: unknown;
  start_time: string;
  finish_time: string;
  action: string | null;
  job_id: string;
}


export default function useTaskRunner() {
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const authGetApi = useCallback(async <T = any>(url: string): Promise<T> => {
        const res = await api.get<T>(url);
        return res.data;
    }, []);
  const [error, setError] = useState<unknown>(null);
  const [result, setResult] = useState<TaskResultOut | null>(null);
  
  const getTaskResults = useCallback(async <T = any>(taskId: string, signal?: AbortSignal): Promise<T> => {
      try {
        if (!taskId) throw new Error("Task ID is required");

        let attempts = 0;
        const maxAttempts = 30;
        const intervalMs = 2000;

        const clearTimer = () => {
          if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
            timeoutRef.current = null;
          }
        };

        const checkStatus = async (resolve: (data: T) => void, reject: (err: unknown) => void) => {
          if (signal?.aborted) {
            clearTimer();
            return reject(new Error('Task polling cancelled'));
          }

          attempts++;
          try {
            const statusData = await authGetApi<TaskStatus>(`/tasks/${taskId}/status`);
            if (statusData.status === "complete") {
              const data = await authGetApi<TaskResultOut>(`/tasks/${taskId}/result`);
              setResult(data);
              clearTimer();
              return resolve((data.result as { data?: { result?: T } } | undefined)?.data?.result as T);
            } else if (statusData.status === "failed") {
              clearTimer();
              return reject(new Error(`Task ${taskId} failed.`));
            }

            if (attempts < maxAttempts) {
              timeoutRef.current = setTimeout(() => checkStatus(resolve, reject), intervalMs);
            } else {
              clearTimer();
              reject(new Error(`Task not complete after ${maxAttempts} attempts.`));
            }
          } catch (err) {
            clearTimer();
            reject(err);
          }
        };

        return new Promise<T>((resolve, reject) => {
          const abortListener = () => {
            clearTimer();
            reject(new Error('Task polling cancelled'));
          };
          if (signal) {
            if (signal.aborted) return abortListener();
            signal.addEventListener('abort', abortListener, { once: true });
          }
          checkStatus(resolve, reject);
        });
      } catch (err: unknown) {
        setError(err);
        throw err;
      }
    }, [authGetApi]);
  
    const runFetchUntilComplete = useCallback(
      async (endpoint: string, signal?: AbortSignal) => {
        try {
          const resp = await authGetApi<{ task_id?: string }>(endpoint);
          const taskId = resp?.task_id;
          if (!taskId) throw new Error('No task_id returned');
          return await getTaskResults(taskId, signal);
        } catch (err) {
          setError(err);
          throw err;
        }
      },
      [authGetApi, getTaskResults]
    );

    return { getTaskResults, runFetchUntilComplete, error, result };
  }