"use client";
import { useState, useCallback, useRef } from "react";
import api from "../apiClient";


export default function useTaskRunner() {
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    const authGetApi = useCallback(async (url: string) => {
        const res = await api.get(url);
        return res.data;
    }, []);
    const [error, setError] = useState<any>(null);
    const [result, setResult] = useState<any>(null);
  
    const getTaskResults = useCallback(async (taskId: string, signal?: AbortSignal) => {
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

        const checkStatus = async (resolve: (data: any) => void, reject: (err: any) => void) => {
          if (signal?.aborted) {
            clearTimer();
            return reject(new Error('Task polling cancelled'));
          }

          attempts++;
          try {
            const statusData = await authGetApi(`/tasks/${taskId}/status`);
            if (statusData.status === "complete") {
              const data = await authGetApi(`/tasks/${taskId}/result`);
              setResult(data);
              clearTimer();
              return resolve(data.result?.data?.result);
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

        return new Promise<any>((resolve, reject) => {
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
      } catch (err: any) {
        setError(err);
        throw err;
      }
    }, [authGetApi]);
  
    const runFetchUntilComplete = useCallback(
      async (endpoint: string, signal?: AbortSignal) => {
        try {
          const resp = await authGetApi(endpoint);
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