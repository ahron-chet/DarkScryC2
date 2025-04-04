"use client";
import { useState, useCallback } from "react";
import useAuthApi from "lib/fetchApiClient";


export default function useTaskRunner() {
    const { authGetApi } = useAuthApi();
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);
  
    const getTaskResults = useCallback(async (taskId: string) => {
      try {
        if (!taskId) throw new Error("Task ID is required");
  
        let attempts = 0;
        const maxAttempts = 30;
        const intervalMs = 2000;
  
        const checkStatus = async (resolve: Function, reject: Function) => {
          attempts++;
          try {
            const statusData = await authGetApi(`/tasks/${taskId}/status`);
            if (statusData.status === "complete") {
              const data = await authGetApi(`/tasks/${taskId}/result`);
              setResult(data);
              return resolve(data.result?.data?.result);
            } else if (statusData.status === "failed") {
              return reject(new Error(`Task ${taskId} failed.`));
            }
  
            if (attempts < maxAttempts) {
              setTimeout(() => checkStatus(resolve, reject), intervalMs);
            } else {
              reject(new Error(`Task not complete after ${maxAttempts} attempts.`));
            }
          } catch (err) {
            reject(err);
          }
        };
  
        return new Promise<any>(checkStatus);
      } catch (err: any) {
        setError(err);
        throw err;
      }
    }, [authGetApi]);
  
    return { getTaskResults, error, result };
  }